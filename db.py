import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE temperature (date TEXT, time TEXT, temperature REAL, humidity REAL)')
print("Table created successfully")

conn.execute('CREATE TABLE distance (date TEXT, time TEXT, distance REAL)')
print("Table created successfully")

conn.close()


