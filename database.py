import sqlite3

def init_db():
    conn = sqlite3.connect("fake_news.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                prediction TEXT)""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
