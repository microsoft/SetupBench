
import sqlite3
import os

os.makedirs('/data', exist_ok=True)
conn = sqlite3.connect('/data/test.db')
cur = conn.cursor()

with open("schema.sql", "r") as f:
    cur.executescript(f.read())

conn.commit()
conn.close()
print("DB initialized.")
