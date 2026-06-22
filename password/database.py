import sqlite3

DB = "passwords.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history (password TEXT)")
    conn.commit()
    conn.close()

def save_password(password):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO history VALUES (?)", (password,))
    conn.commit()
    conn.close()

def is_reused(password):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT password FROM history WHERE password=?", (password,))
    result = cur.fetchone()
    conn.close()
    return result is not None