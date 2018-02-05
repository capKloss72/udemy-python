import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Use INTEGER for auto increment
create_users_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_users_table)

create_item_table = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price float)'
cursor.execute(create_item_table)

connection.commit()
connection.close()
