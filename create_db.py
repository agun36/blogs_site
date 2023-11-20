import sqlite3

# Connect to SQLite3 (or create a new database file if it doesn't exist)
conn = sqlite3.connect('our_users.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table named 'users'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
