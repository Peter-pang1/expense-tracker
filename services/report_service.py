import pandas as pd
from services.database import get_connection

def get_summary_by_category(user_id):
    conn = get_connection()
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM expenses WHERE user_id=? GROUP BY category",
                           conn, params=(user_id,))
    conn.close()
    return df.to_dict(orient="records")

def get_summary_by_month(user_id):
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id=?
        GROUP BY month
    """, conn, params=(user_id,))
    conn.close()
    return df.to_dict(orient="records")