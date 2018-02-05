import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = "INSERT INTO items VALUES(NULL, 'pin', 12.25)"
#query = "SELECT * FROM users"
#query = "SELECT * FROM items"
#query = "DELETE FROM items WHERE name = 'plate'"
cursor.execute(query)
connection.commit()

query = "SELECT * FROM items"
for i in cursor.execute(query):
    assert isinstance(i)
    print(i)
