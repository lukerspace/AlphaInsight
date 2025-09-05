import sqlite3
import yfinance as yf

DB_PATH = "./sqlite.db" 

def import_benchmark(symbol="SPY", start="2010-01-01"):
    # 下載與前處理
    benchmark = yf.download(symbol, start=start)[["Close"]]
    benchmark_ffill = benchmark.ffill()
    benchmark_ffill["Symbol"] = symbol.upper()
    benchmark_ffill = benchmark_ffill.rename(columns={"Close": "Price"}).reset_index()
    benchmark_ffill["Date"] = benchmark_ffill["Date"].dt.strftime("%Y-%m-%d").astype(str)

    # 準備 insert_list
    insert_list = [tuple(row) for row in benchmark_ffill[["Date", "Price", "Symbol"]].itertuples(index=False, name=None)]

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # 建表（如果不存在）
    cur.execute("""
    CREATE TABLE IF NOT EXISTS benchmark (
        Date    TEXT,
        Price   REAL,
        Symbol  TEXT
    )
    """)

    # 逐列檢查與插入
    for data_row in insert_list:
        data_row = list(data_row)
        data_row[1] = float(data_row[1])  # 確保 Price 是 float
        data_row = tuple(data_row)

        cur.execute("SELECT COUNT(*) FROM benchmark WHERE Date = ? AND Symbol = ?", (data_row[0], data_row[2]))
        result = cur.fetchone()[0]

        if result == 0:
            cur.execute(
                "INSERT INTO benchmark (Date, Price, Symbol) VALUES (?, ?, ?)",
                data_row
            )

    con.commit()
    con.close()

import_benchmark()
