import sqlite3


def create_connection():
    return sqlite3.connect('employees.db')


def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
