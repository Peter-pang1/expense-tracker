from services.database import get_connection

def add_expense(amount, category, date, note=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                (amount, category, date, note))
    conn.commit()
    conn.close()

def get_expenses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_expenses_by_date(start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC",
                (start_date, end_date))
    rows = cur.fetchall()
    conn.close()
    return rows