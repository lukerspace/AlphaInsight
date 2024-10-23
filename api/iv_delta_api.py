import sys,os,datetime
sys.path.append("./")
from dotenv import load_dotenv
from flask import *
from api_db_query import select_iv_delta
import pandas as pd
import redis
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
appIvdelta = Blueprint('appIvdelta', __name__)

load_dotenv()

redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

# Helper function to fetch token from Redis
def fetch_token_from_redis(user_email):
    token = redis_client.get(user_email)
    if not token:
        print({"error": "Token not found in Redis"})
    return token


@appIvdelta.route('/ivdelta', methods=['GET'])
def get_iv_delta():
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
    
    data=select_iv_delta()
    return data

