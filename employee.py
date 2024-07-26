from database import create_connection
from datetime import datetime


class Employee:
    def __init__(self, full_name, birth_date, gender):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def save_to_db(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)',
                       (self.full_name, self.birth_date, self.gender))
        conn.commit()
        conn.close()

    def calculate_age(self):
        birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d')
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    @staticmethod
    def bulk_insert(employees):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)',
                           [(emp.full_name, emp.birth_date, emp.gender) for emp in employees])
        conn.commit()
        conn.close()
