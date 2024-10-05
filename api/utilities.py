
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pandas_ta as ta
import plotly.express as px



def cal_cagr(timeseries, since=None):
    if not since:
        idx = 0
    else:
        idx = timeseries.index.get_indexer([since], method='bfill')[0]

    time_diff = timeseries.index[-1] - timeseries.index[idx]
    years = time_diff.days / 365
    start, end = timeseries.iloc[idx], timeseries.iloc[-1]
    return ((end / start) ** (1 / years)) - 1

def cal_mdd(timeseries):
    drawdown = ta.drawdown(timeseries)
    return drawdown['DD_PCT'].max()

def cal_sharpe(timeseries, risk_free_return=0):
    daily_return = timeseries / timeseries.shift(1) - 1 - risk_free_return
    return np.sqrt(252) * np.mean(daily_return) / np.std(daily_return)

def cal_calmar_ratio(timeseries, risk_free_return=0):
    annual_return = cal_cagr(timeseries)
    mdd = cal_mdd(timeseries)

    return (annual_return - risk_free_return) / mdd

def gen_stats_from_equity(equity_series, p_sharpe=None):
    
    drawdown = ta.drawdown(equity_series)

    Summary = {}
    Summary['Return %'] = round((equity_series.iloc[-1] / equity_series.iloc[0] - 1) * 100, 2)
    Summary['Comp. Annual Return'] = round(cal_cagr(equity_series) * 100, 2)
    Summary['Max Drawdown %'] = round(drawdown['DD_PCT'].max() * 100, 2)
    Summary['Max Drawdown % Date'] = drawdown['DD_PCT'].idxmax()
    Summary['Return%/Max Drawdown%'] = round(Summary['Return %'] / Summary['Max Drawdown %'], 4)
    Summary['Std'] = round(np.std(equity_series.pct_change(1))*(252**(0.5)), 4)
    if p_sharpe:
        Summary['Sharpe Ratio'] = round(cal_sharpe(equity_series.iloc[-p_sharpe:]), 2)
    else: 
        Summary['Sharpe Ratio'] = round(cal_sharpe(equity_series), 2)
    Summary['Calmar Ratio'] = round(cal_calmar_ratio(equity_series), 2)
    return Summary





