import os
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

# === SQLite 設定 ===
# 可用環境變數 DB_PATH 覆蓋，預設 sqlite.db
DB_PATH = os.getenv("DB_PATH", "sqlite.db")

def get_conn():
    """取得 SQLite 連線；含輕量 PRAGMA。"""
    # 確保資料夾存在
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")    # 改善多讀一寫
    cur.execute("PRAGMA synchronous=NORMAL;")  # 寫入較快
    cur.execute("PRAGMA cache_size=-20000;")   # ~20MB page cache
    cur.close()
    return conn

# 工具：將 cursor.fetchall() 轉為 list[dict]
def rows_to_dicts(rows):
    return [dict(r) for r in rows]

# ===== 通用查詢器：等號與日期大於 =====
def _build_where_and_params(kwargs, date_key="date"):
    """
    規則：
      - 若 key == date_key：使用  column > ?
      - 其他 key：          使用  column = ?
    傳回 where_sql, params
    """
    clauses, params = [], []
    for k, v in kwargs.items():
        if k == date_key:
            clauses.append(f"{k} > ?")
            params.append(v)
        else:
            clauses.append(f"{k} = ?")
            params.append(v)
    if not clauses:
        return "", []
    return " WHERE " + " AND ".join(clauses), params

# ================= 你原本函數對應（SQLite 版本） =================

def user_select(**kargs):
    conn = get_conn()
    cur = conn.cursor()
    where_sql, params = _build_where_and_params(kargs)
    sql = f"SELECT * FROM users{where_sql} LIMIT 1;"
    print(sql, params)
    cur.execute(sql, params)
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return dict(row)
    return None

def user_insert(**kargs):
    conn = get_conn()
    cur = conn.cursor()
    cols = ",".join(kargs.keys())
    placeholders = ",".join(["?"] * len(kargs))
    sql = f"INSERT INTO users ({cols}) VALUES ({placeholders});"
    vals = list(kargs.values())
    print(sql, vals)
    cur.execute(sql, vals)
    conn.commit()
    cur.close()
    conn.close()

def select_nav(**kwargs):
    conn = get_conn()
    cur = conn.cursor()
    where_sql, params = _build_where_and_params(kwargs, date_key="date")
    sql = f"SELECT * FROM nav{where_sql};"
    print(sql, params)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows_to_dicts(rows) if rows else None

def select_benchmark(**kwargs):
    conn = get_conn()
    cur = conn.cursor()
    where_sql, params = _build_where_and_params(kwargs, date_key="date")
    sql = f"SELECT * FROM benchmark{where_sql};"
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows_to_dicts(rows) if rows else None

def select_strategy():
    conn = get_conn()
    cur = conn.cursor()
    sql = "SELECT DISTINCT graphname FROM nav;"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    dropdownlist = [r[0] for r in rows]
    return dropdownlist




