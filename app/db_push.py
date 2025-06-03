import sqlite3

conn = sqlite3.connect("auth.db")
cursor = conn.cursor()

with open("schema.sql", "r") as file:
  schema = file.read()
  cursor.executescript(schema)


conn.commit()
conn.close()

