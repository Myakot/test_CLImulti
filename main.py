import sys
from database import initialize_db, create_connection
from employee import Employee
import random
import time


def add_employee(full_name, birth_date, gender):
    emp = Employee(full_name, birth_date, gender)
    emp.save_to_db()
    print("Employee added successfully.")


def list_employees():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT full_name, birth_date, gender FROM employees ORDER BY full_name')
    rows = cursor.fetchall()
    for row in rows:
        emp = Employee(*row)
        print(f'{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.calculate_age()} years old')
    conn.close()


def generate_random_employee(gender=None, last_name_start=None):
    first_names_male = ['Igor', 'Stepan', 'Vladimir', 'Aleksandr', 'Dmitry', 'Alexei', 'Vladislav', 'Sergey']
    first_names_female = ['Anya', 'Olga', 'Alena', 'Natalia', 'Svetlana', 'Maryana', 'Ksenia']
    last_names_male = ['Fedorov', 'Lebedev', 'Emelyanenko', 'Kruzov', 'Zlatoglav', 'Gudz']
    last_names_female = ['Fedorova', 'Lebedeva', 'Emelyanenko', 'Kruzova', 'Zlatoglava', 'Gudz']
    patronymics_male = ['Ivanovich', 'Petrovich', 'Sergeevich', 'Nikolaevich', 'Alexandrovich']
    patronymics_female = ['Ivanovna', 'Petrovna', 'Sergeevna', 'Nikolaevna', 'Alexandrovna']
    genders = ['Male', 'Female']

    if gender is None:
        gender = random.choice(genders)

    if gender == 'Male':
        first_name = random.choice(first_names_male)
        last_name = random.choice(last_names_male)
        patronymic = random.choice(patronymics_male)
    else:
        first_name = random.choice(first_names_female)
        last_name = random.choice(last_names_female)
        patronymic = random.choice(patronymics_female)

    if last_name_start:
        last_name = f'{last_name_start}{last_name[1:]}'

    full_name = f'{last_name} {first_name} {patronymic}'
    birth_date = f'{random.randint(1960, 2006)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}'
    return Employee(full_name, birth_date, gender)


def fill_employees():
    employees = []
    male_count = 0
    female_count = 0

    for _ in range(1000000):
        if male_count < female_count:
            employees.append(generate_random_employee(gender='Male'))
            male_count += 1
        else:
            employees.append(generate_random_employee(gender='Female'))
            female_count += 1

    Employee.bulk_insert(employees)
    print("Employees added successfully.")


def query_employees():
    conn = create_connection()
    cursor = conn.cursor()
    start_time = time.time()
    cursor.execute('SELECT * FROM employees WHERE gender = "Male" AND full_name LIKE "F%"')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    end_time = time.time()
    print(f"Query executed in {end_time - start_time} seconds")
    conn.close()


if __name__ == '__main__':
    mode = int(sys.argv[1])
    if mode == 1:
        initialize_db()
    elif mode == 2:
        full_name = sys.argv[2]
        birth_date = sys.argv[3]
        gender = sys.argv[4]
        add_employee(full_name, birth_date, gender)
    elif mode == 3:
        list_employees()
    elif mode == 4:
        fill_employees()
    elif mode == 5:
        query_employees()
