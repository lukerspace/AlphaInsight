import sys,os,datetime
sys.path.append("./")
from dotenv import load_dotenv
from flask import *
from api_db_query import select_spy_net_gex, select_spy_gex_wall
import pandas as pd
import redis
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# api路由
appGex = Blueprint('appGex', __name__)

## 資料庫敏感性資料
load_dotenv()


@appGex.route('/spy_gex_wall', methods=['GET'])
def get_gex_wall():
    try:
        user_email = session.get('user', {}).get('email')
    except:
        return  render_template("index.html")

    if not user_email:
        return  render_template("index.html")
    
    nested_json=select_spy_gex_wall()

    return  jsonify(nested_json)




@appGex.route('/spy_net_gex', methods=['GET'])
def get_net_gex():
    try:
        user_email = session.get('user', {}).get('email')
    except:
        return  render_template("index.html")

    if not user_email:
        return  render_template("index.html")
    
    nested_json=select_spy_net_gex()

    return  jsonify(nested_json)

