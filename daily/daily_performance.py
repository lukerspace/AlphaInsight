import pandas,datetime
import numpy as np
from datetime import timedelta
import os ,sys
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import yfinance as yf
import pandas as pd
import warnings
import mysql.connector
sys.path.append("./")
warnings.simplefilter(action='ignore', category=FutureWarning)


def daily_performance():
    df1=pandas.read_csv("/app/daily/sp500_component.csv")
    df2=pandas.read_csv("/app/daily/nasdaq100_component.csv")

    already_sent_ticker_list=[]
    strength_table_dic={}
    stock_exchange_ratio_values=[]
    all_symbol_recent_performance=[]
    ticker_of_performance=[]

    for number_of_file in range(2):
        df=[df1,df2][number_of_file]
        advance=0
        decline=0 
        count_big_mover=0
        symbols=[i for i in df["Symbol"]]
        symbols=symbols[:]

        for symbol in symbols:

            try:
                price=yf.download(symbol,start=datetime.datetime.today()-timedelta(days=252))["Adj Close"]
                temp=price.pct_change(1)
                max_value=price.max()
                min_value=price.min()
                current_price=price[-1]
                strength_ratio_index=(current_price-min_value)/(max_value-min_value)
                strength_table_dic[symbol]=(strength_ratio_index)


                quarterly_price=price.tail(66).reset_index()
                change1=round(quarterly_price["Adj Close"][66-1]/quarterly_price["Adj Close"][0]-1,4)

                monthly_price=price.tail(22).reset_index()
                change2=round(monthly_price["Adj Close"][22-1]/monthly_price["Adj Close"][0]-1,4)

                biweekly_price=price.tail(14).reset_index()
                change3=round(biweekly_price["Adj Close"][14-1]/biweekly_price["Adj Close"][0]-1,4)

                weekly_price=price.tail(5).reset_index()
                change4=round(weekly_price["Adj Close"][5-1]/weekly_price["Adj Close"][0]-1,4)

                day_price=price.tail(2).reset_index()
                change5=round(day_price["Adj Close"][2-1]/day_price["Adj Close"][0]-1,4)

                collecting_performace_list=([change1,change2,change3,change4,change5])
                collecting_performace_list=[float(str(x*100)[:5]) for x in collecting_performace_list]
                all_symbol_recent_performance.append(collecting_performace_list)
                ticker_of_performance.append(symbol)

                
            except Exception as e:
                print(f"Error processing symbol {symbol}: {e}")
                continue



            if (temp[-1])>0:
                advance+=1
                if ((temp[-1]) > 0.03) and (symbol not in already_sent_ticker_list):
                    up_text=symbol+" UP by "+ str(round(temp[-1]*100,2)) +"%"
                    count_big_mover+=1
                    already_sent_ticker_list.append(symbol)
            elif (temp[-1]<0):
                decline+=1
                if ((temp[-1]) < -0.03) and (symbol not in already_sent_ticker_list):
                    down_text=symbol+" DOWN by "+ str(round(temp[-1]*100,2)) +"%"
                    count_big_mover+=1
                    already_sent_ticker_list.append(symbol)
        
            print(count_big_mover)
            print(symbol)
        ratios=round(advance/(advance+decline),3)
        stock_exchange_ratio_values.append(ratios)
    

    current_date_in_string=str(temp.index[-1])[:10]

    
    ### Create the highlight
    daily_highlight_table=pd.DataFrame(all_symbol_recent_performance,columns=["Quarterly_Chg","Monthly_Chg","Biweekly_Chg","Weekly_Chg","Day_Chg"])
    daily_highlight_table["Ticker"]=ticker_of_performance
    daily_highlight_table=daily_highlight_table[["Ticker","Day_Chg","Weekly_Chg","Biweekly_Chg","Monthly_Chg","Quarterly_Chg"]].sort_values(by="Weekly_Chg",ascending=False)
    daily_highlight_table["Name"]=daily_highlight_table["Ticker"]
    daily_highlight_table=daily_highlight_table.drop_duplicates(subset="Ticker",keep="first")
    # daily_highlight_table.to_excel("data_{}.xlsx".format(current_date_in_string))
    return daily_highlight_table[["Ticker","Day_Chg","Weekly_Chg","Biweekly_Chg","Monthly_Chg","Quarterly_Chg"]]


load_dotenv()

print("daily...",os.getenv("SERVER_HOST"))

# Establish connection to MySQL database
conn = mysql.connector.connect(
    host=os.getenv("SERVER_HOST"),
    user=os.getenv("SERVER_USER"),
    password=os.getenv("SERVER_PASSWORD"),
    database="dashboard",
    charset="utf8",
    auth_plugin='caching_sha2_password'
)

# Create a cursor object
cursor = conn.cursor()

# SQL query to drop the table if it exists
drop_table_query = """
DROP TABLE IF EXISTS daily_performance;
"""

# SQL query to create the new table
create_table_query = """
CREATE TABLE daily_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL, 
    daily_change FLOAT NOT NULL,     
    week_change FLOAT NOT NULL,       
    bi_weekly_change FLOAT NOT NULL,  
    monthly_change FLOAT NOT NULL,    
    quarterly_change FLOAT NOT NULL,   
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  
);
"""

# Execute the SQL queries
try:
    cursor.execute(drop_table_query)   # Drop table if exists
    cursor.execute(create_table_query) # Create table
    conn.commit()                      # Commit changes
    print("Table daily_performance created successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    conn.rollback()                    # Rollback in case of error

# Close the cursor and connection

insert_query = """
INSERT INTO daily_performance (ticker, daily_change, week_change, bi_weekly_change, monthly_change, quarterly_change)
VALUES (%s, %s, %s, %s, %s, %s);
"""

df=daily_performance()
for index, row in df.iterrows():
    cursor.execute(insert_query, (
        row['Ticker'],        # Ticker symbol
        row['Day_Chg'],       # Daily change
        row['Weekly_Chg'],    # Weekly change
        row['Biweekly_Chg'],  # Biweekly change
        row['Monthly_Chg'],   # Monthly change
        row['Quarterly_Chg']  # Quarterly change
    ))
    print(row['Ticker'],"... ")
# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()