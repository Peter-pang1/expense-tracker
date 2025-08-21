import pandas as pd
from services.database import get_connection

def get_summary_by_category():
    conn = get_connection()
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM expenses GROUP BY category", conn)
    conn.close()
    return df.to_dict(orient="records")

def get_summary_by_month():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        GROUP BY month
    """, conn)
    conn.close()
    return df.to_dict(orient="records")