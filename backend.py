import mysql.connector
import random
import string
from datetime import datetime, timedelta
from random import randint

host = "localhost"
user = "root"
password = "327275"
database = "ubs"

# Commonly used arrays for names, surnames, and addresses
#names = [
#    'John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Christopher', 'Emma', 'Matthew', 'Olivia',
#    'Daniel', 'Sophia', 'James', 'Ava', 'Joseph', 'Mia', 'Benjamin', 'Charlotte', 'Elijah', 'Amelia',
#    'Samuel', 'Harper', 'Alexander', 'Evelyn', 'William', 'Abigail', 'Henry', 'Emily', 'Daniel', 'Elizabeth',
#    'Matthew', 'Avery', 'Andrew', 'Sofia', 'Gabriel', 'Chloe', 'Jackson', 'Ella', 'Nathan', 'Grace', 'Oliver',
#    'Liam', 'Madison', 'Ethan', 'Aria', 'Lucas', 'Scarlett', 'Isaac', 'Lily', 'Noah', 'Sophie', 'Logan', 'Zoe',
#    'Caleb', 'Aurora', 'Ezra', 'Aaliyah', 'Sebastian', 'Aiden', 'Hannah', 'Wyatt', 'Nova', 'Grayson', 'Luna',
#    'Leo', 'Stella', 'Hunter', 'Isla', 'Mason', 'Mila', 'Jack', 'Bella', 'Owen', 'Savannah', 'Eli', 'Layla',
#    'Aiden', 'Scarlet', 'Jackson', 'Penelope', 'Carter', 'Avery', 'Evan', 'Natalie', 'Luke', 'Ellie', 'Levi', 'Hazel',
#    'Isaiah', 'Aria', 'Lincoln', 'Grace', 'Landon', 'Addison', 'Olivia', 'Eleanor', 'Lucy', 'Claire']
#
#surnames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
#            'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson',
#            'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hill', 'King', 'Scott', 'Green',
#            'Baker', 'Adams', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell',
#            'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers']
#
#addresses = ['Main St', 'Oak Ave', 'Pine Ln', 'Elm Blvd', 'Cedar Dr', 'Maple Rd', 'Birch St', 'Sycamore Ave', 'Willow Ln',
#             'Cypress Blvd', 'Spruce Dr', 'Chestnut Rd', 'Hickory St', 'Magnolia Ave', 'Walnut Ln', 'Palm Blvd', 'Poplar Dr',
#             'Fir Rd', 'Larch St', 'Juniper Ave', 'Peach Ln', 'Plum Blvd', 'Cherry Dr', 'Pear Rd', 'Apple St', 'Orange Ave',
#             'Banana Ln', 'Grape Blvd', 'Lemon Dr', 'Lime Rd', 'Coconut St', 'Pineapple Ave', 'Mango Ln', 'Papaya Blvd',
#             'Guava Dr', 'Watermelon Rd', 'Cantaloupe St', 'Kiwi Ave', 'Blueberry Ln', 'Raspberry Blvd', 'Blackberry Dr',
#             'Strawberry Rd', 'Grapefruit St', 'Avocado Ave', 'Cherry Tomatoes Ln', 'Pomegranate Blvd', 'Passion Fruit Dr']

# Function to insert students
def insert_students(cursor, total_student_count):
    departments = ['Department1', 'Department2', 'Department3', 'Department4', 'Department5', 'Department6']
    for i in range(1, total_student_count + 1):
        student_id = i
        department = random.choice(departments)

        cursor.execute('''
            INSERT INTO Student (student_id, department)
            VALUES (%s, %s)
        ''', (student_id, department))

def insert_active_student(cursor, active_student_count):
    for i in range(1, active_student_count + 1):
        student_id = i
        cursor.execute('''
            INSERT INTO Active_student (student_id)
            VALUES (%s)
        ''', (student_id,))

def insert_graduated_student(cursor,graduated_student_count,active_student_count):
    for i in range(active_student_count+1,active_student_count+graduated_student_count+1):
        student_id = i
        graduate_date = datetime(randint(2020,2023), 7, random.randint(1, 31))
        grade = round(random.uniform(2.0, 4.0), 2)

        cursor.execute('''
            INSERT INTO Graduated_student (student_id, graduate_date, grade)
            VALUES (%s, %s, %s)
        ''', (student_id, graduate_date, grade))

# Function to insert employees
def insert_employees(cursor, employee_count, total_student_count):
    for i in range(total_student_count+1 , total_student_count + employee_count + 1):
        employee_id = i
        salary = random.randint(30000, 80000)

        cursor.execute('''
            INSERT INTO Employee (employee_id, salary)
            VALUES (%s, %s)
        ''', (employee_id, salary))
def insert_teachers(cursor,total_student_count,teacher_count):
    for i in range(total_student_count+1,total_student_count+teacher_count+1):
        teacher_id = i
        course_id = i - 420

        cursor.execute('''
            INSERT INTO Teacher (teacher_id, course_id)
            VALUES (%s, %s)
        ''', (teacher_id, course_id))

def insert_admins(cursor, admin_baslangic, admin_bitis):
    for i in range(admin_baslangic + 1, admin_bitis+1):
        admin_id = i
        cursor.execute('''
            INSERT INTO Administrative_staff (personel_id)
            VALUES (%s)
        ''', (admin_id,))

def insert_temizlikci(cursor,temizlikci_baslangic,total_person_count):
    for i in range(temizlikci_baslangic + 1, total_person_count+1):
        tem_id = i
        cursor.execute('''
            INSERT INTO Temizlikci (temizlikci_id)
            VALUES (%s)
        ''', (tem_id,))

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection.is_connected():
        cursor = connection.cursor()

        total_student_count = 520
        #insert_students(cursor, total_student_count)

        active_student_count = 420
        #insert_active_student(cursor,active_student_count)

        
        graduated_student_count = 100
        #insert_graduated_student(cursor,graduated_student_count,active_student_count)

        employee_count = 30
        #insert_employees(cursor, employee_count, total_student_count)

        teacher_count = 6
        #insert_teachers(cursor,total_student_count,teacher_count)

        admin_baslangic = total_student_count+teacher_count
        admin_bitis = admin_baslangic + 6
        insert_admins(cursor,admin_baslangic,admin_bitis)

        total_person_count = 550
        temizlikci_baslangic = admin_bitis
        insert_temizlikci(cursor,temizlikci_baslangic, total_person_count)


        ## Insert 500 persons
        #for i in range(1, 551):
        #    name = random.choice(names)
        #    surname = random.choice(surnames)
        #    surname_initials = surname[:2].lower()
        #    address = f'{random.randint(1, 999)} {random.choice(addresses)}'
        #    age = random.randint(19, 27)
        #    tel_no = '05' + ''.join(random.choices(string.digits, k=9))
        #    mail = f'{name.lower()}.{surname_initials[:1]}@edu.tr'  # Shorter email address
        #
        #    cursor.execute('''
        #        INSERT INTO Person (person_id, age, mail, tel_no, address, name, surname)
        #        VALUES (%s, %s, %s, %s, %s, %s, %s)
        #    ''', (i, age, mail, tel_no, address, name, surname))

        connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")
