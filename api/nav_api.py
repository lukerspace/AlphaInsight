import sys, os, datetime, json   # ← 加上 json，避免後面 json.dumps NameError
sys.path.append("./")
from dotenv import load_dotenv
from flask import *
from database import select_nav, select_benchmark   # ← 改用 SQLite 版本
import pandas as pd
import redis
import os
import lib.utilities
from redis_clients import get_redis_client


# api路由
appNav = Blueprint('appNav', __name__)

## 資料庫敏感性資料
load_dotenv()
# Redis connection
# redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=6379, db=0)
redis_client = get_redis_client()


# Helper function to fetch token from Redis
def fetch_token_from_redis(user_email):
    print(redis_client)
    token = redis_client.get(user_email)
    if not token:
        print({"error": "Token not found in Redis~"})
    return token

# Modularized function for selecting data
def process_data(graphname, filter_date):
    data_tuples = select_nav(graphname=graphname, date=filter_date)
    benchmark_tuples = select_benchmark(date=filter_date)

    
    date_list_strategy=(pd.DataFrame(data_tuples))["Date"].to_list()
    val_strategy_list=(pd.DataFrame(data_tuples))["Nav"].to_list()
    
    date_list_benchmark=(pd.DataFrame(benchmark_tuples))["Date"].to_list()
    val_benchmark_list=(pd.DataFrame(benchmark_tuples))["Price"].to_list()

    strategy_df = pd.DataFrame({"date": pd.to_datetime(date_list_strategy), "strategy": val_strategy_list})
    benchmark_df = pd.DataFrame({"date": pd.to_datetime(date_list_benchmark), "benchmark": val_benchmark_list})


    return strategy_df, benchmark_df

@appNav.route('/nav', methods=['GET'])
def get_equity_curve():
    try:
        # Get the user's email from the session
        user_email = session.get('user', {}).get('email')
    except Exception as e:
        return render_template("index.html")
    
    if not user_email:
        return render_template("index.html")

    # Fetch token from Redis
    token = fetch_token_from_redis(user_email)
    if not token:
        return render_template("index.html")

    # Dynamic query parameters
    graphname = request.args.get('graphname')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not graphname or not year or not month:
        return jsonify({"error": "Missing required parameters"}), 400
    
    # try:
    filter_date = datetime.datetime(year, month, 1).strftime("%Y-%m-%d")
    strategy_df, benchmark_df = process_data(graphname, filter_date)

    # Merging the strategy and benchmark DataFrames
    combined_df = pd.merge(strategy_df, benchmark_df, on="date", how="inner").set_index("date")

    # Initial and final values for calculation
    first_val_strategy = combined_df["strategy"][0]
    first_val_benchmark = combined_df["benchmark"][0]
    last_val_strategy = combined_df["strategy"][-1]
    last_val_benchmark = combined_df["benchmark"][-1]

    combined_df.index = combined_df.index.strftime('%Y-%m-%d')

    # Calculate returns
    combined_df["benchmark_r"] = round(100 * combined_df["benchmark"] / first_val_benchmark - 100, 3)
    combined_df["strategy_r"] = round(100 * combined_df["strategy"] / first_val_strategy - 100, 3)
    combined_df["benchmark_bh"] = round(100 * last_val_benchmark / combined_df["benchmark"] - 100, 3)
    combined_df["strategy_bh"] = round(100 * last_val_strategy / combined_df["strategy"] - 100, 3)
    
    # Prepare response
    response_data = {
        "Date": combined_df.index.to_list(),
        "Benchmarkvalue": combined_df["benchmark_r"].to_list(),
        "Strategyvalue": combined_df["strategy_r"].to_list(),
        "BenchmarkvalueHold": combined_df["benchmark_bh"].to_list(),
        "StrategyvalueHold": combined_df["strategy_bh"].to_list()
    }

    combined_df["metic_benchmark_r"]=combined_df["benchmark_r"]+100
    combined_df["metic_strategy_r"]=combined_df["strategy_r"]+100
    metric_df=combined_df.copy()
    metric_df.index=pd.to_datetime(metric_df.index)

    metric_dic={"strategy":lib.utilities.gen_stats_from_equity(metric_df["metic_strategy_r"]),\
                "benchmark":lib.utilities.gen_stats_from_equity(metric_df["metic_benchmark_r"])}

    combined_response = {
        "data": response_data,
        "metrics": metric_dic
    }


    # Convert the combined dictionary to a JSON string
    json_response = json.dumps(combined_response, sort_keys=False)
    
    # Return the response as JSON
    return Response(json_response, mimetype='application/json')

