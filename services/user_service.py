from services.database import get_connection
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password)))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (username, hash_password(password)))
    user = cur.fetchone()
    conn.close()
    return user