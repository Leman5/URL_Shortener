import sqlite3

def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    
    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls_entry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            shprt_url TEXT UNIQUE NOT NULL,
        )
    ''')
    conn.commit()
    conn.close()
