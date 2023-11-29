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

days = ["Pzt", "Sali", "Cars", "Prs", "Cuma"]
time_slots = ["08:30-10:30", "10:30-12:30", "12:30-14:30", "14:30-16:30", "16:30-18:30"]

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = connection.cursor()

def get_all_students():
    cursor.execute('''
        select *
        from student s
        join person p on s.student_id=p.person_id
    ''')
    values = cursor.fetchall()
    print(values)

def get_active_students():
    cursor.execute('''
        select p.*
        from active_student s
        join person p on s.student_id = p.person_id 
    ''')
    values = cursor.fetchall()
    print(values)

def get_graduated_students():
    cursor.execute('''
        select s.graduate_date, s.grade, p.*
        from graduated_student s
        join person p on s.student_id = p.person_id 
    ''')
    values = cursor.fetchall()
    print(values)

def get_all_parents():
    cursor.execute('''
        select p.*
        from active_student s
        join parents p on s.student_id = p.student_id
    ''')
    values = cursor.fetchall()
    print(values)

def get_all_employees():
    cursor.execute('''
        select e.*
        from employee e
    ''')
    values = cursor.fetchall()
    print(values)


def get_all_teachers():
    cursor.execute('''
        select e.*,t.course_id
        from employee e
        join teacher t on t.teacher_id = e.employee_id
    ''')
    values = cursor.fetchall()
    print(values)

def get_all_administrative_staff():
    cursor.execute('''
        SELECT p.* 
        FROM Administrative_staff a
        join employee e on a.personel_id = e.employee_id
        join person p on e.employee_id = p.person_id
    ''')
    values = cursor.fetchall()
    print (values)
    return values

def get_all_cleaners():
    cursor.execute('''
        SELECT p.* 
        FROM temizlikci t
        join employee e on t.temizlikci_id = e.employee_id
        join person p on e.employee_id = p.person_id
    ''')
    values = cursor.fetchall()
    print (values)
    return values

def get_admin(personel_id):
    cursor.execute('''
        SELECT p.* 
        FROM Administrative_staff a
        join employee e on a.personel_id = e.employee_id
        join person p on e.employee_id = p.person_id
        where a.personel_id = %s 
    ''',(personel_id,))
    value = cursor.fetchone()
    print (value)
    return value

def get_teacher(teacher_id):
    cursor.execute('''
        SELECT p.*,t.course_id as course_id
        FROM teacher t
        join employee e on t.teacher_id = e.employee_id
        join person p on e.employee_id = p.person_id
        where t.teacher_id = %s 
    ''',(teacher_id,))
    value = cursor.fetchone()
    print (value)
    return value

def get_cleaner(cleaner_id):
    cursor.execute('''
        SELECT p.*
        FROM temizlikci t
        join employee e on t.temizlikci_id= e.employee_id
        join person p on e.employee_id = p.person_id
        where t.temizlikci_id = %s 
    ''',(cleaner_id,))
    value = cursor.fetchone()
    print (value)
    return value

def get_active_student(student_id):
    cursor.execute('''
        SELECT p.*
        FROM Active_student s
        join person p on s.student_id = p.person_id
        where s.student_id = %s 
    ''',(student_id,))
    value = cursor.fetchone()
    print (value)
    return value
def get_graduated_student(student_id):
    cursor.execute('''
        SELECT p.*,s.graduate_date,s.grade
        FROM graduated_student s
        join person p on s.student_id = p.person_id
        where s.student_id = %s 
    ''',(student_id,))
    value = cursor.fetchone()
    print (value)
    return value

def get_parent (student_id):
    cursor.execute('''
        SELECT p.*
        FROM student s
        join parents p on s.student_id = p.student_id
        where s.student_id = %s 
    ''',(student_id,))
    value = cursor.fetchone()
    print (value)
    return value

def get_teacher_available_hours(teacher_id):
    cursor.execute('''
        SELECT t.*
        FROM teacher_section_availability t
        where t.teacher_id = %s
    ''',(teacher_id,))
    values = cursor.fetchall()
    schedule = []
    for value in values:
        teacher_id, course_id, day_section = value
        schedule.append((course_id, day_section))
    print_program(schedule)
    return values

def get_all_section_requests():
    cursor.execute('''
            SELECT sr.course_id,sr.day_section
            FROM section_request sr
    ''')
    values = cursor.fetchall()
    print (values)
    return values

def get_section_request(course_id):
    cursor.execute('''
        SELECT c.course_id, c.day_section, c.request_count
        FROM course c
        WHERE c.course_id = %s
    ''', (course_id,))
    values = cursor.fetchall()
    schedule = []
    for value in values:
        course_id, day_section, request_count= value
        schedule.append((request_count, day_section))
    print_program(schedule)
    return values

def get_student_requests():
    cursor.execute('''
            SELECT sr.*
            FROM student_request sr
    ''')
    values = cursor.fetchall()
    print (values)
    return values

def get_student_request(student_id):
    cursor.execute('''
        SELECT sr.*
        FROM student_request sr
        WHERE sr.student_id = %s
    ''', (student_id,))
    values = cursor.fetchall()
    print(values)
    return values
def get_student_available_sections(student_id):
    cursor.execute('''
        SELECT sc.*
        FROM student_section_availability sc
        WHERE sc.student_id = %s
    ''', (student_id,))
    values = cursor.fetchall()
    schedule = []
    for value in values:
        student_id, day_section= value
        schedule.append((1, day_section))
    print_program(schedule)
    return values

def get_student_program(student_id):
    cursor.execute('''
        SELECT sp.*
        FROM student_program sp
        WHERE sp.student_id = %s
    ''', (student_id,))
    values = cursor.fetchall()
    schedule = []
    for value in values:
        student_id, day_section, course_id = value
        schedule.append((course_id, day_section))
    print_program(schedule)
    return values

def get_teacher_program(teacher_id):
    cursor.execute('''
        SELECT sp.*
        FROM teacher_program sp
        WHERE sp.teacher_id = %s
    ''', (teacher_id,))
    values = cursor.fetchall()
    schedule = []
    for value in values:
        teacher_id, day_section, course_id = value
        schedule.append((course_id, day_section))
    print_program(schedule)
    return values


def get_dynamic_person(view_name, *columns):
    query = f'''
        CREATE VIEW {view_name} AS
        SELECT {', '.join(columns)}
        FROM person
        SELECT *
        FROM {view_name}
    '''
    cursor.execute(query)
    print(f"View {view_name} created successfully.")   



def print_program(course_array):
    schedule = [["" for _ in range(len(time_slots))] for _ in range(len(days))]

    for course_id, day_section in course_array:
        day_index = day_section // 10
        time_slot_index = day_section % 10
        schedule[day_index][time_slot_index] = str(course_id)

    print("\t" + "\t".join(time_slot for time_slot in time_slots))
    for i, day in enumerate(days):
        print(f"{day}\t\t" + "\t\t".join(cell if cell != '' else '-' for cell in schedule[i]))


try:
    if connection.is_connected():
        user_input = "age,name,surname"
        columns_to_display = [col.strip() for col in user_input.split(',')]
        get_dynamic_person("1",*columns_to_display)
        connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("Connection closed")