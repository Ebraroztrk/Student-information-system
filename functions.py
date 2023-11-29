import mysql.connector
import random
import string
from datetime import datetime, timedelta
from random import randint, choice, sample

host = "localhost"
user = "root"
password = "327275"
database = "ubs"

days = ["Pzt", "Sali", "Crs", "Prs", "Cuma"]
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

def get_employee(employee_id):
    cursor.execute('''
        select e.salary,p.*
        from employee e
        join person p on p.person_id = e.employee_id
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

def get_weekly_reports():
    cursor.execute('''
        SELECT wp.*
        FROM report_weekly wp
    ''')
    values = cursor.fetchall()
    print(values)
    return values

def get_weekly_report(report_id):
    cursor.execute('''
        SELECT r.*
        FROM report_weekly r
        WHERE r.report_id = %s
    ''', (report_id,))
    values = cursor.fetchall()
    print(values)
    return values

def get_monthly_reports():
    cursor.execute('''
        SELECT mp.*
        FROM report_monthly mp
    ''')
    values = cursor.fetchall()
    print(values)
    return values    

def get_monthly_report(report_id):
    cursor.execute('''
        SELECT r.*
        FROM report_monthly r
        WHERE r.report_id = %s
    ''', (report_id,))
    values = cursor.fetchall()
    print(values)
    return values

def get_course_uses_material():
    cursor.execute('''
        SELECT cm.*,m.value,m.stock_amount
        FROM course_uses_material cm, material m
        where cm.material_id = m.material_id
    ''')
    values = cursor.fetchall()
    print(values)
    return values  

def get_course_uses(course_id):
    cursor.execute('''
        SELECT cm.*
        FROM course_uses_material cm
        WHERE cm.course_id = %s
    ''', (course_id,))
    values = cursor.fetchall()
    print(values)
    return values

def get_materials():
    cursor.execute('''
        SELECT m.*
        FROM material m
    ''')
    values = cursor.fetchall()
    print(values)
    return values

def get_material(material_id):
    cursor.execute('''
        SELECT m.*
        FROM material m
        WHERE m.material_id = %s
    ''', (material_id,))
    values = cursor.fetchall()
    print(values)
    return values   


# Filter for person
def get_dynamic_person(*columns):
    view_name = f'dynamic_person_view_{"_".join(columns)}'
    
    # Check if the view exists
    cursor.execute(f'SHOW TABLES LIKE "{view_name}"')
    result = cursor.fetchone()

    if result:
        print(f"View {view_name} already exists.")
    else:
        query = f'''
            CREATE VIEW {view_name} AS
            SELECT {', '.join(columns)}
            FROM person
        '''
        cursor.execute(query)
        print(f"View {view_name} created successfully.")
    
    cursor.execute(f'''
        SELECT *
        FROM {view_name}
    ''')
    values = cursor.fetchall();
    print (values)



def print_program(course_array):
    schedule = [["" for _ in range(len(time_slots))] for _ in range(len(days))]

    for course_id, day_section in course_array:
        day_index = day_section // 10
        time_slot_index = day_section % 10
        schedule[day_index][time_slot_index] = str(course_id)

    print("\t" + "\t".join(time_slot for time_slot in time_slots))
    for i, day in enumerate(days):
        print(f"{day}\t\t" + "\t\t".join(cell if cell != '' else '-' for cell in schedule[i]))




# -------------------------------------------------------------------------------------------------------------------
#yeni eklenen kisinin isdini almak icin
def get_person_count():
    cursor.execute('''
        SELECT person_id FROM person ORDER BY person_id DESC LIMIT 1;
    ''')
    person_count_tuple = cursor.fetchone()
    count_value = person_count_tuple[0]
    person_count_int = int(count_value)
    return person_count_int

# yeni eklenen material'e id atamak icin
def get_material_count():
    cursor.execute('''
        SELECT material_id FROM material ORDER BY material_id DESC LIMIT 1;
    ''')
    material_count_tuple = cursor.fetchone()
    count_value = material_count_tuple[0]
    material_count_int = int(count_value)
    return material_count_int

#Yeni eklenen hatalikrapora id atamak icinn
def get_report_weekly_count():
    cursor.execute('''
        SELECT report_id FROM report_weekly ORDER BY report_id DESC LIMIT 1;
    ''')
    report_count_tuple = cursor.fetchone()
    count_value = report_count_tuple[0]
    report_count_int = int(count_value)
    return report_count_int

#Yeni eklenen aylikrapora id atamak icinn
def get_report_monthly_count():
    cursor.execute('''
        SELECT report_id FROM report_monthly ORDER BY report_id DESC LIMIT 1;
    ''')
    report_count_tuple = cursor.fetchone()
    count_value = report_count_tuple[0]
    report_count_int = int(count_value)
    return report_count_int

# bir section icin request oldugunda id atamak icin
def get_request_count():
    cursor.execute('''
        SELECT request_id FROM section_request ORDER BY request_id DESC LIMIT 1;
    ''')
    request_count_tuple = cursor.fetchone()
    count_value = request_count_tuple[0]
    request_count_int = int(count_value)
    return request_count_int

#day_section [pzt,3] gibi girdileri sayiya cevirmek icin 
def convert_section_to_number(day_section):
    day, section = day_section
    first_digit = days.index(day) 
    second_digit = time_slots.index(section) 
    
    return first_digit * 10 + second_digit
#------------------------------------------------------------------------------------------------------------------------

try:
    if connection.is_connected():
        
        #user_input = "age,name,surname,address,mail,tel_no"
        #columns_to_display = [col.strip() for col in user_input.split(',')]
        #get_dynamic_person(*columns_to_display)
        #get_weekly_reports()
        #get_monthly_reports()
        #get_course_uses_material()
        #get_course_uses(101)
        #get_materials()
        #get_material(10)
        #get_monthly_report(1)
        #get_weekly_report(1)
        input = 'Crs', '12:30-14:30'
        print(convert_section_to_number(input))
        connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("Connection closed")