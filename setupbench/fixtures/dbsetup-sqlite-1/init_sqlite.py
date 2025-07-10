
import sqlite3
import os

os.makedirs('/data', exist_ok=True)
conn = sqlite3.connect('/data/test.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL
)
""")

cur.executemany("INSERT INTO items (name, quantity) VALUES (?, ?)", [
    ("apple", 10),
    ("banana", 20),
    ("cherry", 15)
])

conn.commit()
conn.close()
print("SQLite DB initialized.")
