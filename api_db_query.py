import mysql.connector
import json,os
from dotenv import load_dotenv
from mysql.connector import pooling
import pandas as pd
import numpy as np 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import  timedelta

load_dotenv()



def user_select(**kargs):
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql=f'select * from users where '
    for i in kargs:
        sql+=f'{i} = \'{kargs[i]}\' and '
    sql=sql[:-5]
    print(sql)
    cursor.execute(sql)
    user=cursor.fetchone()

    if user:
        userdata=(dict(zip(cursor.column_names,user)))
        cursor.close()
        return userdata
    else:
        return None
   

def user_insert(**kargs):
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql=f'insert into users '
    column = '('
    value = '('
    for i in kargs:
        column += i + ','
        value += f"\'{kargs[i]}\',"
    column = column[:-1] + ')'
    value = value[:-1] + ')'
    sql += column + ' VALUES ' + value
    print(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def select_nav(**kwargs):
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql=f"select * from nav where "
    for i in kwargs:
        sql+=f'{i} = \'{kwargs[i]}\' and '
    sql=sql[:-5]
    query=(sql.split("date "))
    # print(sql)
    new_sql=query[0]+"date >"+query[1]+';'
    print(new_sql)

    cursor.execute(new_sql)
    nav=cursor.fetchall()

    if len(nav)>0:
        cursor.close()
        return nav
    else:
         return None
    

def select_benchmark(**kwargs):
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql=f"select * from benchmark where "
    for i in kwargs:
        sql+=f'{i} = \'{kwargs[i]}\' and '
    sql=sql[:-5]
    query=(sql.split("date "))
    new_sql=query[0]+"date >"+query[1]+';'
    print(new_sql)

    cursor.execute(new_sql)
    nav=cursor.fetchall()

    if len(nav)>0:
        cursor.close()
        return nav
    else:
         return None


def select_strategy():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql=f"select distinct(graphname) from nav"
    cursor.execute(sql)
    strategy_list=cursor.fetchall()
    dropdownlist=[]
    for i in (strategy_list):
        dropdownlist.append(i[0])

    print(dropdownlist)
    return dropdownlist


def select_coppock_data():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql="select * from coppock where category='{}' order by date Desc;".format('coppock_value')
    cursor.execute(sql)
    my_data=cursor.fetchall()

    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Convert the data to a list of dictionaries (rows as dicts with column names as keys)
    result = [dict(zip(column_names, row)) for row in my_data]

    # Convert the result to JSON in str
    json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # Load the JSON data
    data = json.loads(json_data)


    max_date=pd.to_datetime(pd.DataFrame(data)["date"].max())

    # Print or return the JSON data
    # today = datetime.today()
    new_date = max_date - relativedelta(months=3)
    new_date=new_date+timedelta(days=1)
    new_date=new_date.strftime("%Y-%m-%d")
    print(max_date,new_date)

    # Filter the data where the 'date' is greater than the reference date
    filtered_data = [entry for entry in data if entry['date'] > new_date]
    date_list=[]
    ticker_list=[]
    for i in filtered_data:
        if (pd.to_datetime(i['date'])>=pd.to_datetime(new_date)):
            if i['date'] not in date_list:
                date_list.append(i['date'])
            if i['ticker'] not in ticker_list:
                ticker_list.append(i['ticker'])

    nested_json={}

    tmps=(pd.DataFrame(filtered_data))
    for month in  date_list:
        m=(month)
        tmp=tmps.loc[tmps["date"]==month]
        sysdate=(tmp["sysdate"].values[0])
        
        # print(tmp)
        row_value=[]
        for row in range(len(tmp)):
            t=(tmp.iloc[row]["ticker"])
            v=(tmp.iloc[row]["value"])
            row_value.append(v)
            nested_json[m]=row_value
                # print(m,t,v)
    print(nested_json)
    return nested_json


def select_coppock_ratio():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql="select * from coppock where category='{}' order by date Desc;".format('coppock_ratio')
    cursor.execute(sql)
    my_data=cursor.fetchall()
    # Get the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    # Convert the data to a list of dictionaries (rows as dicts with column names as keys)
    result = [dict(zip(column_names, row)) for row in my_data]
    # Convert the result to JSON in str
    json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # Load the JSON data
    data = json.loads(json_data)

    # print( max(data.keys()))
    # Print or return the JSON data
    today = datetime.today()
    new_date = today - relativedelta(months=3)
    new_date=new_date.strftime("%Y-%m-%d")
    # Filter the data where the 'date' is greater than the reference date
    filtered_data = [entry for entry in data if entry['date'] > new_date]
    date_list=[]
    ticker_list=[]
    for i in filtered_data:
        if (pd.to_datetime(i['date'])>=pd.to_datetime(new_date)):
            if i['date'] not in date_list:
                date_list.append(i['date'])
            if i['ticker'] not in ticker_list:
                ticker_list.append(i['ticker'])

    nested_json={}

    tmps=(pd.DataFrame(filtered_data))
    for month in  date_list:
        m=(month)
        tmp=tmps.loc[tmps["date"]==month]
        sysdate=(tmp["sysdate"].values[0])
        
        # print(tmp)
        row_value=[]
        for row in range(len(tmp)):
            t=(tmp.iloc[row]["ticker"])
            v=(tmp.iloc[row]["value"])
            row_value.append(v)
            nested_json[m]=row_value
                # print(m,t,v)

    print(nested_json)
    return nested_json


def select_daily_performance():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql="select * from daily_performance"
    cursor.execute(sql)
    my_data=cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    result = [dict(zip(column_names, row)) for row in my_data]
    # Convert the result to JSON in str
    json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # Load the JSON data
    data = json.loads(json_data)

    return data


def select_iv_delta():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql = """ SELECT * FROM iv_delta ORDER BY date DESC LIMIT 100 """
    cursor.execute(sql)
    my_data=cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    result = [dict(zip(column_names, row)) for row in my_data]
    records=(pd.DataFrame(result).sort_values("date")).to_dict(orient='records')
    # Convert the result to JSON in str
    # json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # # Load the JSON data
    json_data = json.dumps(records,default=str)
    data = json.loads(json_data)

    return data





def select_daily_performance():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql="select * from daily_performance"
    cursor.execute(sql)
    my_data=cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    result = [dict(zip(column_names, row)) for row in my_data]
    # Convert the result to JSON in str
    json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # Load the JSON data
    data = json.loads(json_data)

    return data


def select_spy_gex_wall():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql = """ SELECT * FROM spy_gex_wall """
    cursor.execute(sql)
    my_data=cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    result = [dict(zip(column_names, row)) for row in my_data]
    records=(pd.DataFrame(result).sort_values("date")).to_dict(orient='records')
    # Convert the result to JSON in str
    # json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # # Load the JSON data

    records = pd.DataFrame(result).sort_values("price").to_dict(orient='records')

    json_data = json.dumps(records,default=str)
    data = json.loads(json_data)
    return data


def select_spy_net_gex():
    conn=mysql.connector.connect(
        host = os.getenv("SERVER_HOST"),user=os.getenv("SERVER_USER"),
        password=os.getenv("SERVER_PASSWORD"),database = "dashboard",
        charset = "utf8",auth_plugin='caching_sha2_password'
    )
    cursor = conn.cursor()
    sql = """ SELECT * FROM spy_net_gex order by date DESC LIMIT 100 """

    cursor.execute(sql)
    my_data=cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    result = [dict(zip(column_names, row)) for row in my_data]
    records=(pd.DataFrame(result).sort_values("date")).to_dict(orient='records')
    # Convert the result to JSON in str
    # json_data = json.dumps(result, default=str)  # Use default=str to handle non-serializable objects like datetime
    # # Load the JSON data
    json_data = json.dumps(records,default=str)
    data = json.loads(json_data)
    return data

