import pandas as pd
import sqlite3
from datetime import datetime
import yfinance as yf

DB_PATH = "./sqlite.db"

def update_nav(ticker="NVDA", start="2010-01-01"):
    dt = str(datetime.today().strftime("%Y-%m-%d"))
    ticker = ticker.upper()

    # 下載資料
    df = yf.download(ticker, start=start)[["Close"]]
    df["Graphname"] = ticker
    df["CreatedDate"] = dt
    df.columns = ["Nav", "Graphname", "CreatedDate"]
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)

    # 準備要插入的資料
    insert_list = [tuple(row) for row in df[["Date","Nav","Graphname","CreatedDate"]].itertuples(index=False, name=None)]

    # 寫入 SQLite
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    for data_row in insert_list:
        data_row = list(data_row)
        data_row[1] = float(data_row[1])  # 確保 Nav 為 float
        data_row = tuple(data_row)

        cur.execute(
            "SELECT COUNT(*) FROM nav WHERE Date=? AND Graphname=? AND CreatedDate<=?",
            (data_row[0], data_row[2], data_row[3]),
        )
        result = cur.fetchone()[0]

        if result == 0:
            cur.execute(
                "INSERT INTO nav (Date, Nav, Graphname, CreatedDate) VALUES (?, ?, ?, ?)",
                data_row,
            )
            print("Inserted:", data_row)
        else:
            pass
            # print("Skipped:", data_row[0])

    con.commit()
    con.close()


update_nav("AMZN")
