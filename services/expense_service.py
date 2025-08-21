from services.database import get_connection

def add_expense(user_id, amount, category, date, note=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (user_id, amount, category, date, note) VALUES (?, ?, ?, ?, ?)",
                (user_id, amount, category, date, note))
    conn.commit()
    conn.close()

def get_expenses(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_expenses_by_date(user_id, start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=? AND date BETWEEN ? AND ? ORDER BY date DESC",
                (user_id, start_date, end_date))
    rows = cur.fetchall()
    conn.close()
    return rows