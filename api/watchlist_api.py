import sys,os,datetime
sys.path.append("./")
from dotenv import load_dotenv
from flask import *
import mysql.connector
from api_db_query import select_daily_performance
import pandas as pd
import redis
import os
# from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# api路由
appDaily = Blueprint('appDaily', __name__)

## 資料庫敏感性資料
load_dotenv()


@appDaily.route('/daily',methods=["GET"])
def get_daily_perf():
    try:
        user_email = session.get('user', {}).get('email')
    except:
        return  render_template("index.html")

    if not user_email:
        return  render_template("index.html")
    
    data=select_daily_performance()
    return data
