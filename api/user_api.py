import sys,os,mysql.connector,datetime
sys.path.append("..")
from dotenv import load_dotenv
from flask import *
from flask import session
from api_db_query import  user_select, user_insert, select_strategy
import jwt
import redis

# api路由
appUser = Blueprint('appUser', __name__)


## 資料庫敏感性資料
load_dotenv()

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),  # Update with your Redis server host
    port=6379,         # Update with your Redis server port
    db=0,
    decode_responses=True
)

@appUser.route('/user', methods=['GET'])
def get_userdata():
    # 登入成功
    if "user" in session:
        user = session['user']
        data = {
            "data":user
        }
        return jsonify(data)

    # 登入失敗
    data = {"data": None}
    return jsonify(data)


@appUser.route('/user', methods=['POST'])
def signup():
    try:
        conn = conn=mysql.connector.connect(
            host = os.getenv("SERVER_HOST"),\
            user=os.getenv("SERVER_USER"),\
            password=os.getenv("SERVER_PASSWORD"),\
            database = "dashboard",charset = "utf8",\
            auth_plugin='caching_sha2_password')
        
        conn.reconnect(attempts=1, delay=0)
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']
        exist_user = user_select(email=email)
        # 註冊成功
        created_at=datetime.datetime.now()
        if not exist_user:
            user_insert(name=name, email=email, password=password,created_at=created_at)
            data = {"ok": True}
            return jsonify(data), 200

        # 如果已經有人使用過該email，回應錯誤訊息
        else:
            data = {
                "error": True,
                "message": "註冊失敗，該email已經被註冊過了"
            }
            return jsonify(data), 400

    # 伺服器錯誤
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500


@appUser.route('/user', methods=['PATCH'])
def signin():
    # try:
        conn =mysql.connector.connect(host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),password=os.getenv("SERVER_PASSWORD"), database = "dashboard",charset = "utf8",auth_plugin='caching_sha2_password')
        conn.reconnect(attempts=1, delay=0)
        data = request.json
        email = data['email']
        password = data['password']
        
        user = user_select(email=email, password=password)
        # 登入成功
        if user:
            session['user'] = {"id": user["id"],"name": user["name"],"email": user["email"]}
            print(session)
            try:
            # Clear any existing token in Redis for this user
                redis_client.delete(user["email"])
                print("delete the old token in redis ", user["email"])
            except:
                print(user["email"] , " never log in before")
            expire_time=datetime.datetime.now() + datetime.timedelta(seconds=60*10)
            # Convert expiration time to Unix timestamp (seconds since epoch)
            expire_timestamp = expire_time.timestamp()

            # Convert to milliseconds
            expire_milliseconds = int(expire_timestamp * 1000)
            print(expire_milliseconds)
            token = jwt.encode({
                    'email': email,
                    'exp': expire_time  # Token expiration time
                }, "pass", algorithm='HS256')
            print("++++++>>>",token)
            # Store JWT token in Redis with user email as key and set the expiration time to 1 minute
            redis_client.set(user["email"], token)
            redis_client.expire(user["email"], 60*10)
            
            # # Prepare response
            data = {"ok": True, "token": token,"expired":expire_milliseconds}
            response = make_response(jsonify(data))
   
            return response

        # 登入失敗
        else:
            data = {
                "error": True,
            }
            return jsonify(data), 200

    # 伺服器錯誤
    # except:
    #     data = {
    #         "error": True,
    #         "message": "伺服器內部錯誤"
    #     }
    #     return jsonify(data), 500


@appUser.route('/user', methods=['DELETE'])
def singout():
    # 登出
    print(session)
    if "user" in session:
        data = {"ok": True}
        session.pop('user')
        print("successsful logout...",session)
        
        return jsonify(data)
    else:
        data = {"ok": False}
        return jsonify(data)


@appUser.route("/user/strategy",methods=["GET"])
def dailynav():
    if "user" in session:
        daily_nav=select_strategy()
        return jsonify({"dropdown_list":daily_nav})
    else:
        data = {
            "error": True,
            "message": "No session"
        }
        return jsonify(data)
