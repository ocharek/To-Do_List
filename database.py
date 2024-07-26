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

def select_all_tasks(conn, name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM zadania_{name}')
    tasks = cursor.fetchall()
    return tasks

def add_task(conn, name, t):
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO zadania_{name} (Task, Done) VALUES ("{t}", 0)')
    conn.commit()

def delete_task(conn, task_id, name):
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM zadania_{name} WHERE ZadanieID = %s', (task_id,))
    conn.commit()

def check_task(conn, task_id, state, name):
    cursor = conn.cursor()
    cursor.execute(f'UPDATE zadania_{name} SET Done = {state} WHERE ZadanieID = %s', (task_id,))
    conn.commit()
def close_connection(conn):
    if conn:
        conn.close()

