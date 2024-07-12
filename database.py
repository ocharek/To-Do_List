import mysql.connector

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="todolist"
        )
        if conn.is_connected():
            print("Połączono z bazą danych")
            return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

