import sys,os,datetime
sys.path.append("./")
from dotenv import load_dotenv
from flask import *
from api_db_query import select_coppock_data, select_coppock_ratio
import pandas as pd
import redis
import os
# from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# api路由
appCoppock = Blueprint('appCoppock', __name__)

## 資料庫敏感性資料
load_dotenv()


@appCoppock.route('/coppock_data', methods=['GET'])
def get_coppock_value():
    try:
        user_email = session.get('user', {}).get('email')
    except:
        return  render_template("index.html")

    if not user_email:
        return  render_template("index.html")
    
    nested_json=select_coppock_data()

    return  jsonify(nested_json)


@appCoppock.route('/coppock_ratio', methods=['GET'])
def get_coppock_ratio():
    try:
        user_email = session.get('user', {}).get('email')
    except:
        return  render_template("index.html")

    if not user_email:
        return  render_template("index.html")
    
    nested_json=select_coppock_ratio()

    return  jsonify(nested_json)

