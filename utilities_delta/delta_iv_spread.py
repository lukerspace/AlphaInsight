import os
import sys
import math
import time
import warnings
import numpy as np
import pandas as pd
import mysql.connector
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from dotenv import load_dotenv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup



load_dotenv()
print(os.getenv("SERVER_HOST"))


def conncection_database():
    conn=mysql.connector.connect(
    host = os.getenv("SERVER_HOST"),\
    user=os.getenv("SERVER_USER"),\
    password=os.getenv("SERVER_PASSWORD"),\
    database = "dashboard",charset = "utf8",\
    auth_plugin='caching_sha2_password')
    cursor = conn.cursor()
    return cursor,conn

def iv_spread_scarp_25(ticker):
    option = Options()
    # option.add_argument('--headless')
    driver = webdriver.Chrome(options=option)
    
    ticker=ticker.upper()
    url="https://marketchameleon.com/Overview/{}/VolatilitySkew/".format(ticker)
    driver.get(url)

    time.sleep(5)
    updated_html = driver.page_source
    soup = BeautifulSoup(updated_html, "html.parser")
    tables=pd.read_html(str(soup))

    df=tables[2]['SPY 25-Delta Put - Call Spread Last 20 Days']
    df=df.set_index("Date")
    df.columns
    df.index=[datetime.strptime(i, "%d-%b-%Y") for i in df.index]
    df=df.sort_index()
    driver.quit()
    
    return df

def update_iv_spread_25(ticker):
    iv_row_list=[]
    df=iv_spread_scarp_25(ticker)
    signal=pd.read_excel("./utilities_delta/"+ticker+"_25d_spread.xlsx",index_col=0)
    tmp=df.iloc[df.index.isin(df.index.difference(signal.index))]
    data=pd.concat([signal,tmp],axis=0)
    data.to_excel("./utilities_delta/"+ticker+"_25d_spread.xlsx")
    price=yf.download(ticker,start=data.index[0])["Adj Close"]
    
    price=yf.download(ticker)["Adj Close"]
    price=price.reset_index()
    
    read_data=pd.read_excel("./utilities_delta/"+ticker+"_25d_spread.xlsx")
    table= pd.merge(read_data,price,left_on="Unnamed: 0",right_on="Date",how="left")

    table=table[["Date","Difference Put - Call","Adj Close"]]
    table=table.rename(columns={"Adj Close":ticker.upper()}).set_index("Date")

    for index, row in table.iterrows():
        row_data_tuple=(tuple((index,row["SPY"],row["Difference Put - Call"])))
        iv_row_list.append(row_data_tuple)
    return (iv_row_list)
       
def insert_delta_table(iv_row_list):
    cursor , conn = conncection_database()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS iv_delta (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date TIMESTAMP NOT NULL,
        value FLOAT NOT NULL,
        delta FLOAT NOT NULL,
        sysdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    # Execute the query to create the table
    cursor.execute(create_table_query)
    # Commit changes
    conn.commit()
    # Close the cursor and connection
    cursor.close()
    conn.close()
    print("created iv_delta tables")
    for row in iv_row_list:
        date, value, delta = row  # tuples in the format (date, value, delta)
        check_query = "SELECT COUNT(*) FROM iv_delta WHERE date = %s"
        
        cursor ,conn= conncection_database()

        cursor.execute(check_query, (date,))
        record_exists = cursor.fetchone()[0] > 0
        if not record_exists:
            insert_query = """
            INSERT INTO iv_delta (date, value, delta)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (date, value, delta))
            conn.commit() 
            print(f"Inserted: {row}")
        else:
            pass
            # print(f"Record for date {date} already exists. Skipping insertion.")
    print("Insertion Done")
        

if __name__ == '__main__':
    iv_row_list=update_iv_spread_25("spy")
    insert_delta_table(iv_row_list)
