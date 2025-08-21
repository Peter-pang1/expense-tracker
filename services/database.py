import sqlite3

def init_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            date TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("expenses.db")