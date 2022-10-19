import sqlite3
conn = sqlite3.connect("database.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS userTable(username VARCHAR(32), email VARCHAR(32),password VARCHAR(32), flash VARCHAR(32) )")