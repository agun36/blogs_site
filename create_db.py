import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123"
    # auth_plugin="mysql_native_password"
)

# it makes all execute queries
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE our_users")
mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)


mycursor.close()
mydb.close()