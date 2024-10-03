
import pandas as pd 
import mysql.connector
import datetime ,os
import yfinance as yf
from dotenv import load_dotenv
import sys
# sys.path.append("./")
sys.path.append("..")
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta
import math,datetime
import warnings


load_dotenv()
print(os.getenv("SERVER_HOST"))

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

def cal_coppock_curve(price):
    roc_short = ((price / price.shift(11)) - 1) * 100
    roc_long = ((price / price.shift(14)) - 1) * 100
    return round(ta.wma(roc_short + roc_long, 10),2)

def shift_index(date,df1):
    while date not in df1.index:
        date += timedelta(days=1)
    return date


def generate_coppock():
    reference = yf.download("SPY")["Adj Close"].resample("M").last()[:]
    reference_daily = yf.download("SPY")["Adj Close"]
    reference_monthly = reference_daily.resample("M").last()
    reference_coppock = cal_coppock_curve(reference_monthly)
    reference_coppock = reference_coppock.rename("Ref Coppock")

    symbols = ["XLK","XLY","XLI","XLP", "XLF", "XLE","XLU","XLRE","XLC","XLV", "XLB"]
    # symbols = ["XLK","XLY","XLI","XLP", "XLF", "XLE","XLU","XLV", "XLB"]
    result=pd.DataFrame()
    for ticker in symbols:
        # Prepare price data
        daily_adj_close = yf.download(ticker, progress=False)["Adj Close"]
        monthly_adj_close = daily_adj_close.resample("M").last()
        monthly_adj_close = monthly_adj_close[:]
        reference_den = reference.loc[(reference.index >= monthly_adj_close.index[0]) & (reference.index <= monthly_adj_close.index[-1])]
        relative_price = (monthly_adj_close / reference_den).dropna()
        coppock_value = cal_coppock_curve(relative_price)
        data = pd.DataFrame()
        data[ticker+" Rel Price"] = relative_price
        data[ticker+" Coppock"] = list(coppock_value)
        data = pd.merge(data, reference_coppock, left_index=True, right_index=True, how="left")
        result=pd.concat([result,data[[ticker+" Coppock"]]],axis=1)
    result=pd.concat([result,data["Ref Coppock"]],axis=1)

    signals=result.dropna()
    signals=signals.loc[signals.index<=datetime.datetime.now()]
    signals.columns=[i.split(" ")[0] for i in signals.columns]
    signals=signals.rename(columns={"Ref":"SPY"})

    weight=float(str(1/(len(signals.columns)-1))[:6])
    allocation=signals.copy()
    allocation["TLT"]=0
    allocation.loc[allocation["SPY"]==0,"TLT"]=0.5
    for sym in symbols:
        allocation.loc[allocation[sym]<0,sym]=0
        allocation.loc[allocation[sym]>0,sym]=weight
    allocation["SPY"]=0
    allocation.loc[allocation["TLT"]==0,"SPY"]=1.0-allocation.sum(axis=1)

    price=yf.download(list(allocation.columns),start=allocation.index[0])["Adj Close"]
    price["YM"]=price.index.strftime("%Y%m")
    # allocation.index=(price.drop_duplicates(subset="YM",keep="first").index[:])
    return signals,allocation


signals,allocation=generate_coppock()





conn=mysql.connector.connect(
host = os.getenv("SERVER_HOST"),\
user=os.getenv("SERVER_USER"),\
password=os.getenv("SERVER_PASSWORD"),\
database = "dashboard",charset = "utf8",\
auth_plugin='caching_sha2_password')
cursor = conn.cursor()


dfs=[signals,allocation]
for num in range(len(dfs)):

    if num==0:
        category="coppock_value"
    else:
        category="coppock_ratio"
    
    dataset=dfs[num]
    ticker_list=list(dataset.columns)
    for index, row in dataset.iterrows():
        dt=(str(row.name)[:10])
        for myticker in ticker_list:
            tk=(myticker)
            # print(row[myticker])
            val=(round(row[myticker],4))
            row_data_tuple=(tuple((dt,tk,val,category)))
            
            check_sql="SELECT COUNT(*) FROM coppock WHERE date='{}' and ticker='{}' and category='{}';".format(dt,tk,category)
            cursor.execute(check_sql)
            result=cursor.fetchone()
            # print(result)
            if result[0]==0:
                insert_sql = '''
                    INSERT INTO coppock (date, ticker, value, category)
                    VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(insert_sql, row_data_tuple)
                conn.commit()
                print("INSERT ",row_data_tuple)
            else:
                print(" Data Exist .." )







