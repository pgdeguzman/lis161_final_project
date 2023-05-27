import sqlite3

db_path = 'pa.db'

conn = sqlite3.connect(db_path)
cur = conn.cursor()
query = 'SELECT * FROM pets WHERE type=?'
a_type = input("Please enter animal type:")
results = cur.execute(query, [a_type, '?']).fetchall()
for item in results:
    print(item)
conn.close()
