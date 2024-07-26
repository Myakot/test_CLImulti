import sqlite3


def create_connection():
    return sqlite3.connect('employees.db')


def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_full_name_gender ON employees (full_name, gender)')
    conn.commit()
    conn.close()
    print("DB initialized.")
