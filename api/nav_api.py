import sys,os,datetime
sys.path.append("./")
from dotenv import load_dotenv
from flask import *
import mysql.connector
from api_db_query import select_nav,select_benchmark
import pandas as pd
import redis
import os
# from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# api路由
appNav = Blueprint('appNav', __name__)

## 資料庫敏感性資料
load_dotenv()
# Redis connection
redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=6379, db=0)
# r = redis.Redis(host='localhost', port=6379, db=0)



@appNav.route('/nav', methods=['GET'])
def get_equity_curve():
    try:
        user_email = session.get('user', {}).get('email')
    except:
        return  render_template("index.html")

    if not user_email:
        return  render_template("index.html")
    

    
    # Retrieve the token from Redis
    token = redis_client.get(user_email)
    if not token:
        print({"error": "Token not found in Redis"})
        return render_template("index.html")


    graphname=request.args.get('graphname')
    year=int(request.args.get('year'))
    month=int(request.args.get('month'))
    filter_date = datetime.datetime(year, month, 1).strftime("%Y-%m-%d")
    data_tuples = select_nav(graphname=graphname,date=filter_date)
    benchmark_tuples = select_benchmark(date=filter_date)
    

    date_list_benmark=[]
    date_list_strategy=[]
    val_benchmark_list=[]
    val_strategy_list=[]



    for tup1 in data_tuples:
        val_strategy_list.append(tup1[1])
        # if tup[0] >= datetime.datetime(year, month, 1):
        date_list_strategy.append(tup1[0].strftime("%Y-%m-%d"))

    tmp1=pd.DataFrame()
    tmp1["date"]=date_list_strategy
    tmp1["strategy"]=val_strategy_list
    tmp1["date"]=pd.to_datetime(tmp1["date"])
    
    
    for tup2 in benchmark_tuples:
        val_benchmark_list.append(tup2[1])
        # if tup[0] >= datetime.datetime(year, month, 1):
        date_list_benmark.append(tup2[0].strftime("%Y-%m-%d"))

    tmp2=pd.DataFrame()
    tmp2["date"]=date_list_benmark
    tmp2["benchmark"]=val_benchmark_list
    tmp2["date"]=pd.to_datetime(tmp2["date"])

    tmp = pd.merge(tmp1, tmp2, on="date", how="inner").set_index("date")
    first_val_strategy=tmp["strategy"][0]
    first_val_benchmark=tmp["benchmark"][0]
    print(first_val_strategy,first_val_benchmark)
    tmp=tmp.sort_index()
    tmp.index=tmp.index.strftime('%Y-%m-%d')
    result=tmp.copy()
    print(tmp)
    # tmp = tmp / tmp.iloc[0]
    # tmp["benchmark"]=round(tmp["benchmark"]*100-100,3)
    # tmp["strategy"]=round(tmp["strategy"]*100-100,3)
    result["benchmark"]=round(100*result["benchmark"]/first_val_benchmark-100,3)
    result["strategy"]=round(100*result["strategy"]/first_val_strategy-100,3)
    print(result)


    
    try:

        return jsonify( {"Date": result.index.to_list(),\
                        "Benchmarkvalue":result["benchmark"].to_list(),\
                        "Strategyvalue":result["strategy"].to_list()}),200
    
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤，資料數量不一致"
        }
        return jsonify(data), 500
    
    
    