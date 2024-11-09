from flask import *
from getpass import getpass
import platform
import os
from flask import Flask, jsonify, request
from flask import *
import redis
import gunicorn
from dotenv import load_dotenv

load_dotenv()

# Configure Redis
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),  # Redis server hosts
    port=6379,         # Redis server port
    db=0,
    decode_responses=True
)

from api.user_api import appUser
from api.nav_api import appNav
from api.coppock_api import appCoppock
from api.watchlist_api import appDaily
from api.iv_delta_api import appIvdelta
from api.gex_api import appGex

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"] = False
app.config['JWT_SECRET_KEY'] = 'pass'  # Change this to a strong secret key
app.secret_key="hello"

app.register_blueprint(appNav, url_prefix='/api')
app.register_blueprint(appUser, url_prefix='/api')
app.register_blueprint(appCoppock, url_prefix='/api')
app.register_blueprint(appDaily, url_prefix='/api')
app.register_blueprint(appIvdelta, url_prefix='/api')
app.register_blueprint(appGex, url_prefix='/api')

# Pages
@app.route("/")
def index():
	# return render_template("index.html")
      
    # Retrieve user email from session
    user_email = session.get('user', {}).get('email')
    # Retrieve the token from Redis
    if not user_email:
        return  render_template("index.html")
	
    token = redis_client.get(user_email)
    if not token:
        print({"error": "Token not found in Redis"})
        return render_template("index.html")
    

    # Prepare response and include token in headers
    # render template with header attched with auth
    response = make_response(render_template("index.html"))
    response.headers['Authorization'] = 'Bearer ' + token


    return  response


@app.route("/member")
def member():
    
    user_email = session.get('user', {}).get('email')
    if not user_email:
        return  render_template("index.html")
	
    token = redis_client.get(user_email)
    if not token:
        print({"error": "Token not found in Redis"})
        return render_template("index.html")
    
    # Retrieve user email from session
    user_email = session.get('user', {}).get('email')
    name=session.get('user', {}).get('name')
    print(session,user_email,name)
    
    response = make_response(render_template("member.html",name=name,email=user_email))
    response.headers['Authorization'] = 'Bearer ' + token

    return response




@app.route("/data")
def datatable():
    
    user_email = session.get('user', {}).get('email')
    if not user_email:
        return  render_template("index.html")
	
    token = redis_client.get(user_email)
    if not token:
        print({"error": "Token not found in Redis"})
        return render_template("index.html")
    

    # Retrieve user email from session
    user_email = session.get('user', {}).get('email')
    name=session.get('user', {}).get('name')
    print(session,user_email,name)
    
    response = make_response(render_template("data.html"))
    response.headers['Authorization'] = 'Bearer ' + token

    return response




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)



