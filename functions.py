import mysql.connector
import random
import string
from datetime import datetime, timedelta
from random import randint, choice, sample

host = "localhost"
user = "root"
password = "327275"
database = "ubs"

person_id = 551 #yeni insanlar eklendikce 551den sonra id alicak



def get_all_students(cursor):
    cursor.execute('''
        select *
        from student s
        join person p on s.student_id=p.person_id
    ''')
    values = cursor.fetchall()
    print(values)

def get_active_students(cursor):
    cursor.execute('''
        select p.*
        from active_student s
        join person p on s.student_id = p.person_id 
    ''')
    values = cursor.fetchall()
    print(values)

def get_graduated_students(cursor):
    cursor.execute('''
        select s.graduate_date, s.grade, p.*
        from graduated_student s
        join person p on s.student_id = p.person_id 
    ''')
    values = cursor.fetchall()
    print(values)

def get_all_parents(cursor):
    cursor.execute('''
        select p.*
        from active_student s
        join parents p on s.student_id = p.student_id
    ''')
    values = cursor.fetchall()
    print(values)

def get_all_employees(cursor):
    cursor.execute('''
        select e.*
        from employee e
    ''')
    values = cursor.fetchall()
    print(values)


def get_all_teachers(cursor):
    cursor.execute('''
        select e.*,t.course_id
        from employee e
        join teacher t on t.teacher_id = e.employee_id
    ''')
    values = cursor.fetchall()
    print(values)


try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection.is_connected():
        cursor = connection.cursor()
        get_all_teachers(cursor)
    connection.commit()
except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")