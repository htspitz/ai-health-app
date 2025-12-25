import sqlite3

DB_NAME = "health_app.db"

def init_db():
    """テーブルを作成する"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            input_text TEXT,
            ai_summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_record(user_name, input_text, ai_summary):
    """データを保存する"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO records (user_name, input_text, ai_summary) VALUES (?, ?, ?)", (user_name, input_text, ai_summary))
    conn.commit()
    conn.close()

def get_chat_history(limit=5):
    """履歴を取得する"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT created_at, ai_summary FROM records ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
    