
import sqlite3
import os
import sys

if sys.version_info >= (3, 0):
    print "This script is only compatible with Python 2."
    sys.exit(1)

try:
    os.makedirs('/data')
except:
    pass

conn = sqlite3.connect('/data/test.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, message TEXT)")
cur.execute("INSERT INTO logs (message) VALUES ('boot')")
conn.commit()
conn.close()
print "Log entry written."
