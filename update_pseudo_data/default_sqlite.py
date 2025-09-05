import sqlite3
DB_PATH = "./sqlite.db" 


def init_schema():
    """
    建立/確保三個表存在（精簡版）：
      - users(id, name, email UNIQUE, password, created_at)
      - nav(Date, Nav, Graphname, CreatedDate)
      - benchmark(Date, Price, Symbol)
    備註：SQLite 建議日期以 TEXT('YYYY-MM-DD') 儲存；數值用 REAL。
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        -- users
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL UNIQUE,
            password    TEXT NOT NULL,
            created_at  TEXT
        );

        -- nav (MySQL: Date DATETIME, Nav FLOAT, Graphname VARCHAR, CreatedDate DATETIME)
        CREATE TABLE IF NOT EXISTS nav (
            Date        TEXT,
            Nav         REAL,
            Graphname   TEXT,
            CreatedDate TEXT
        );

        -- benchmark (MySQL: Date DATETIME, Price FLOAT, Symbol VARCHAR)
        CREATE TABLE IF NOT EXISTS benchmark (
            Date    TEXT,
            Price   REAL,
            Symbol  TEXT
        );
    """)

    print("table populated in database..")
    conn.commit()
    cur.close()
    conn.close()

init_schema()
