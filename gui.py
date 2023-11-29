import tkinter as tk
import mysql.connector
import random
from random import randint
from tkinter import ttk
from tkinter import messagebox

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '327275',
    'database': 'ubs',
}

days = ["Pzt", "Sali", "Crs", "Prs", "Cuma"]
time_slots = ["08:30-10:30", "10:30-12:30", "12:30-14:30", "14:30-16:30", "16:30-18:30"]


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

class UBSManagementSystem:
    
    def open_insert_dialog(self):
        insert_dialog = InsertDialog(self.insert_active_student)
    def open_teacher_insert(self):
        insert_dialog = InsertTeacher(self.insert_teacher)

    def open_request_insert(self):
        insert_dialog = InsertStudentRequest(self.insert_student_request)

    def insert_student_request(self,student_id,course_id):
        cursor.execute('''
            INSERT INTO Student_Request (student_id, course_id)
            VALUES (%s, %s)
        ''', (student_id, course_id))

    def insert_employee(self,employee_id,salary):
        cursor.execute('''
            INSERT INTO Employee (employee_id, salary)
            VALUES (%s, %s)
        ''', (employee_id, salary))

    def insert_teacher(self,age,mail,tel_no,address,name,surname,salary,course_id):
        teacher_id = self.get_person_count() + 1
        self.insert_person(teacher_id,age,mail,tel_no,address,name,surname)
        self.insert_employee(teacher_id,salary)

        cursor.execute('''
            INSERT INTO Teacher (teacher_id,course_id)
            VALUES (%s,%s)
        ''', (teacher_id,course_id))

        selected_numbers = self.create_random_sections()
        for day_section in selected_numbers:
            cursor.execute('''
                INSERT INTO Teacher_Section_Availability (teacher_id, course_id, available_section)
                VALUES (%s, %s, %s)
            ''', (teacher_id, course_id, day_section))


    def get_person_count(self):
        cursor.execute('''
            SELECT person_id FROM person ORDER BY person_id DESC LIMIT 1;
        ''')
        person_count_tuple = cursor.fetchone()
        count_value = person_count_tuple[0]
        person_count_int = int(count_value)
        return person_count_int

    def insert_person(self,person_id,age,mail,tel_no,address,name,surname):
        cursor.execute('''
            INSERT INTO Person (person_id, age, mail, tel_no, address, name, surname)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (person_id, age, mail, tel_no, address, name, surname))

    def create_student_program(self,student_id):
        cursor.execute('''
            SELECT ssa.available_section
            FROM Student_Section_Availability ssa
            WHERE ssa.student_id = %s
        ''', (student_id,))

        avail_hours = cursor.fetchall()

        cursor.execute('''
            SELECT c.course_id, c.day_section
            FROM course c
            join student_request sr on c.course_id = sr.course_id and sr.student_id = %s
            WHERE c.active
        ''', (student_id,))
        courses = cursor.fetchall()

        added_courses = []  
        added_hours = []
        schedule = []      

        for course in courses:
            course_id, day_section = course
            if course_id not in added_courses and day_section not in added_hours:
                if day_section in [hour[0] for hour in avail_hours]:
                    schedule.append([day_section, course_id])
                    added_courses.append(course_id)
                    added_hours.append(day_section)
        
        for schedule1 in schedule:
            day_section, course_id = schedule1
            cursor.execute('''
                INSERT INTO Student_Program(student_id,day_section,course_id)
                VALUES(%s,%s,%s)
            ''', (student_id,day_section,course_id))


    def create_random_sections(self):
        num_of_random_numbers = random.randint(40, 45)
        self.random_numbers = []

        for i in range(num_of_random_numbers):
            first_digit = random.randint(0, 4)
            second_digit = random.randint(0, 4)
            if (first_digit * 10 + second_digit) not in self.random_numbers:
                self.random_numbers.append(first_digit * 10 + second_digit) 
        return self.random_numbers

    def insert_active_student(self,department,age,mail,tel_no,address,name,surname):
        student_id = self.get_person_count()+1
        self.insert_person(student_id,age,mail,tel_no,address,name,surname)
        cursor.execute('''
            INSERT INTO Student(student_id, department)
            VALUES (%s, %s)
        ''', (student_id, department))

        cursor.execute('''
            INSERT INTO Active_Student(student_id)
            VALUES (%s)
        ''', (student_id,))

        selected_numbers = self.create_random_sections()
        for day_section in selected_numbers:
            cursor.execute('''
                INSERT INTO Student_Section_Availability (student_id, available_section)
                VALUES (%s, %s)
            ''', (student_id, day_section))

    def __init__(self, root):

        self.root = root
        self.root.title("UBS Management System")
        self.root.geometry("1024x768") 
        # Arka plan rengi
        background_color = "#202C33"
        # Buton rengi
        button_color = "#009F78"
        # Yazı rengi
        text_color = "#FFFFFF"

        labels = []
        
        style = ttk.Style(self.root)
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12), background=background_color, foreground=text_color)

        # Toolbar oluşturun
        self.toolbar = tk.Frame(self.root, bg=background_color)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.second_toolbar = tk.Frame(self.root, bg=background_color)
        self.second_toolbar.pack(side=tk.TOP, fill=tk.X)
        self.third_toolbar = tk.Frame(self.root, bg=background_color)
        self.third_toolbar.pack(side=tk.TOP, fill=tk.X)
        # "Öğrenciler" butonu
        self.btn_students = tk.Menubutton(self.toolbar, text="Öğrenciler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_students.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Öğrenciler" butonunun altındaki menü
        self.students_menu = tk.Menu(self.btn_students, tearoff=0)
        self.students_menu.add_command(label="Öğrenci Ara", command=self.search_student)
        self.students_menu.add_command(label="Tüm Öğrenciler", command=self.show_all_students)
        self.students_menu.add_command(label="Aktif Öğrenciler", command=self.show_active_students)
        self.students_menu.add_command(label="Mezun Öğrenciler", command=self.show_graduated_students)
        self.students_menu.add_command(label="Öğrencinin programı",command = self.search_student_program)
        self.students_menu.add_command(label="Öğrencinin müsait saatleri",command = self.search_student_avail_hours)
        self.students_menu.add_command(label="Öğnrecinin seçtiği dersler",command = self.search_student_request)
        self.btn_students.config(menu=self.students_menu)

        # "Öğretmenler" butonu
        self.btn_teachers = tk.Menubutton(self.toolbar, text="Öğretmenler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_teachers.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Öğretmenler" butonunun altındaki menü
        self.teachers_menu = tk.Menu(self.btn_teachers, tearoff=0)
        self.teachers_menu.add_command(label="Öğretmen Ara", command=self.search_teacher)
        self.teachers_menu.add_command(label="Tüm Öğretmenler", command=self.show_all_teachers)
        self.teachers_menu.add_command(label="Öğretmenlerin müsait_saatleri", command=self.search_teacher_avail_hours)
        self.teachers_menu.add_command(label="Öğremenin programı",command = self.search_teacher_program)
        
        self.btn_teachers.config(menu=self.teachers_menu)

        # "Çalışanlar" butonu
        self.btn_employees = tk.Menubutton(self.toolbar, text="Çalışanlar", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_employees.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Çalışanlar" butonunun altındaki menü
        self.employees_menu = tk.Menu(self.btn_employees, tearoff=0)
        self.employees_menu.add_command(label="Çalışan Ara", command=self.get_employee_by_id)

        self.employees_menu.add_command(label="Öğretmenler", command=self.show_all_teachers)
        self.employees_menu.add_command(label="Yöneticiler", command=self.show_all_admins)
        ##admins'i ekle
        #self.employees_menu.add_command(label="İdareciler", command=self.show_administrators)
        ##all employees'i ekle
        #self.employees_menu.add_command(label="Tüm Çalışanlar", command=self.em)
        self.btn_employees.config(menu=self.employees_menu)

        # "Aileler" butonu
        self.btn_families = tk.Menubutton(self.toolbar, text="Aileler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_families.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Aileler" butonunun altındaki menü
        self.families_menu = tk.Menu(self.btn_families, tearoff=0)
        self.families_menu.add_command(label="Aile Ara", command=self.search_parent)
        self.families_menu.add_command(label="Tüm Aileler", command=self.show_all_parents)
        self.btn_families.config(menu=self.families_menu)

        # Notebook oluşturun
        self.notebook = ttk.Notebook(self.root)
        self.style = ttk.Style()
        self.style.configure('TFrame', background=background_color)

        self.tab_general = ttk.Frame(self.notebook, style='TFrame')
        # "Generate Report" butonu
        self.btn_generate_report = tk.Button(self.tab_general, text="Rapor Oluştur",  bg=button_color, fg=text_color)
        self.btn_generate_report.pack(pady=20)

        self.notebook.pack(fill=tk.BOTH, expand=True)


        self.btn_insert = ttk.Button(self.second_toolbar, text="Ogrenci Ekle", command=self.open_insert_dialog)
        self.btn_insert.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btn_insert = ttk.Button(self.second_toolbar, text="Ogretmen Ekle", command=self.open_teacher_insert)
        self.btn_insert.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btn_insert = ttk.Button(self.second_toolbar, text="ogrencinin istedigi ders", command=self.open_request_insert)
        self.btn_insert.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btn_insert = ttk.Button(self.third_toolbar, text="ogrencinin programini olustur", command=self.search_student_for_program)
        self.btn_insert.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        ###################################################################################
        ##FUNCTIONS

    def on_close(self):
        connection.commit()
        connection.close()
        root.destroy()

    def show_all_admins(self):
        window = tk.Toplevel(self.root)
        window.title("Tüm Yöneticiler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("Id", "Yaş", "Mail", "Tel No.", "Adres", "Ad", "Soyad")
        
        for col in tree["columns"]:
            tree.heading(col, text=col,anchor=tk.W)
            tree.column(col, width=100,anchor=tk.W)
        
        data = self.get_all_admins(cursor)  # Use self to access the method
        
        for row in data:
            tree.insert("", "end", values=row)
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
    
    def get_all_admins(self,cursor):
        cursor.execute('''
            SELECT p.* 
            FROM Administrative_staff a
            join employee e on a.personel_id = e.employee_id
            join person p on e.employee_id = p.person_id
        ''')
        values = cursor.fetchall()
        return values

    def search_teacher_avail_hours(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğretmen musait saatleri")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğretmen ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_teacher_avail_hours(entry.get()))
        
        search_button.pack(pady=10)
    def search_student_request(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci İstekleri Ara")

        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğrenci ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_student_request(cursor, entry.get()))
        search_button.pack(pady=10)

    def search_student_avail_hours(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci musait saatleri")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğrenci ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_student_avail_hours(entry.get()))
        
        search_button.pack(pady=10)
    def search_teacher_program(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğretmen Programı")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğretmen ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_teacher_program(entry.get()))
        
        search_button.pack(pady=10)

    def search_student_program(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci Programı")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğrenci ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_student_program(entry.get()))
        
        search_button.pack(pady=10)
    def show_student_avail_hours(self,stduent_id):
        program_data = self.get_student_available_sections(cursor, stduent_id)  # Use self to access the method

        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci Müsait saatleri")

        # Text widget'ını oluştur
        text_widget = tk.Text(search_window, wrap=tk.WORD, width=100, height=10)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, program_data)

    def show_teacher_avail_hours(self, teacher_id):
        program_data = self.get_teacher_available_hours(cursor, teacher_id)  # Use self to access the method

        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğretmen Müsait saatleri")

        # Text widget'ını oluştur
        text_widget = tk.Text(search_window, wrap=tk.WORD, width=100, height=10)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, program_data)

    def show_student_program(self,student_id):
        program_data = self.get_student_program(student_id)  # Use self to access the method

        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci Programı")

        # Text widget'ını oluştur
        text_widget = tk.Text(search_window, wrap=tk.WORD, width=100, height=10)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, program_data)

    def show_teacher_program(self, teacher_id):
        print("A")
        program_data = self.get_teacher_program(cursor, teacher_id)  # Use self to access the method

        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğretmen Programı")

        # Text widget'ını oluştur
        text_widget = tk.Text(search_window, wrap=tk.WORD, width=100, height=10)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, program_data)       
    def show_all_students(self):
        window = tk.Toplevel(self.root)
        window.title("Tüm Öğrenciler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("Öğrenci Numarası", "Ad", "Soyad", "Yaş", "Departman", "Mail", "Cep No.", "Adres")
        
        for col in tree["columns"]:
            tree.heading(col, text=col,anchor=tk.W)
            tree.column(col, width=100,anchor=tk.W)
        
        data = self.get_all_students(cursor)  # Use self to access the method
        
        for row in data:
            tree.insert("", "end", values=row)
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)

    def show_active_students(self):
        window = tk.Toplevel(self.root)
        window.title("Aktif Öğrenciler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("Öğrenci Numarası", "Ad", "Soyad", "Yaş", "Departman", "Mail", "Cep No.", "Adres")

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        data = self.get_active_students(cursor)

        for row in data:
            tree.insert("", "end", values=row)

        scrollbar.config(command=tree.yview)    

        tree.pack(fill=tk.BOTH, expand=True)

    def show_graduated_students(self):
        window = tk.Toplevel(self.root)
        window.title("Mezun Öğrenciler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("Mezuniyet Tarihi", "GANO", "İd", "Yaş", "Mail", "Cep No.","Adres" "Ad", "Soyad")

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        data = self.get_graduated_students(cursor)

        for row in data:
            tree.insert("", "end", values=row)

        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
   
    def search_student(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci Ara")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğrenci ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_student_info(entry.get()))
        search_button.pack(pady=10)

    def search_student_for_program(self):
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğrenci Ara")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğrenci ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.create_student_program(entry.get()))
        search_button.pack(pady=10)

    def show_student_info(self,student_id):
        student_info = self.get_student_by_id(cursor,student_id)  # Use self to access the method
        student_id, age, mail, tel_no, address, name, surname = student_info
        message = f"Öğrenci ID: {student_id}\nAd: {name}\nSoyad: {surname}\nYaş: {age}\nMail: {mail}\nCep No: {tel_no}\nAdres: {address}\n"
        messagebox.showinfo("Öğrenci Bilgileri", message)
    def show_student_request(self, cursor, student_id):
        # Get student requests using the provided student_id
        requests_data = self.get_student_request(cursor, student_id)

        # Display requests_data in a new window or widget as needed
        # For example, you can use a Text widget or a messagebox

        # Arama penceresi oluştur
        requests_window = tk.Toplevel(self.root)
        requests_window.title("Öğrenci İstekleri")

        # Treeview widget'ını oluştur
        tree = ttk.Treeview(requests_window, columns=("student_id", "course_id"))
        tree.heading("student_id", text="Student ID", anchor=tk.W)
        tree.heading("course_id", text="Course ID", anchor=tk.W)

        for row in requests_data:
            tree.insert("", "end", values=row)

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def show_all_teachers(self):
        window = tk.Toplevel(self.root)
        window.title("Tüm Öğretmenler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("öğretmen Id", "Ad", "Soyad", "Maaş", "Ders")
        
        for col in tree["columns"]:
            tree.heading(col, text=col,anchor=tk.W)
            tree.column(col, width=100,anchor=tk.W)
        
        data = self.get_all_teachers(cursor)  # Use self to access the method
        
        for row in data:
            tree.insert("", "end", values=row)
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)

    def search_teacher(self):
        
        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Öğretmen Ara")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğretmen ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_teacher_info(entry.get()))
        search_button.pack(pady=10)

    def show_teacher_info(self,teacher_id):
        self.clear_labels()
        teacher_info = self.get_teacher(cursor,teacher_id)  # Use self to access the method
        teacher_id, name, surname, salary, course = teacher_info
        message = f"Öğretmen ID: {teacher_id}\nAd: {name}\nSoyad: {surname}\nMaaş: {salary} TL\nDers Kodu: {course}\n"
        messagebox.showinfo("Öğretmen Bilgileri", message)
      
    def show_cleaners(self):

        window = tk.Toplevel(self.root)
        window.title("Temizlikçiler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("Id", "Yaş", "Mail", "Tel No", "Adres","Ad","Soyad")
        
        for col in tree["columns"]:
            tree.heading(col, text=col,anchor=tk.W)
            tree.column(col, width=100,anchor=tk.W)
        
        cursor.execute('''
            SELECT p.* 
            FROM temizlikci t
            join employee e on t.temizlikci_id = e.employee_id
            join person p on e.employee_id = p.person_id
            ''')
        data = cursor.fetchall()

        # data = self.get_all_teachers(cursor)  # Use self to access the method
        
        for row in data:
            tree.insert("", "end", values=row)
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)
        
    def get_employee_by_id(self):
        
        search_window = tk.Toplevel(self.root)
        search_window.title("Çalışan Ara")
        
        label = tk.Label(search_window, text="Çalışan ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)
    
        
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_employee_info(entry.get()))
        search_button.pack(pady=10)

    def show_all_parents(self):
        window = tk.Toplevel(self.root)
        window.title("Tüm Aileler")

        scrollbar = ttk.Scrollbar(window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        tree["columns"] = ("Öğrenci Id", "Mail", "Tel No.", "Akraba Ad Soyad")
        
        for col in tree["columns"]:
            tree.heading(col, text=col,anchor=tk.W)
            tree.column(col, width=100,anchor=tk.W)
        
        data = self.get_all_parents(cursor)  # Use self to access the method
        
        for row in data:
            tree.insert("", "end", values=row)
        
        scrollbar.config(command=tree.yview)
        tree.pack(fill=tk.BOTH, expand=True)

    



    def show_employee_info(self, employee_id):
        
        employee_info = self.get_employee(cursor, employee_id)
        employee_id,salary=employee_info
        labels = [
            f"ID: {employee_id}",
            f"Maaş: {salary}"

        ]
        for label_text in labels:
            label = tk.Label(self.root, text=label_text, padx=10, pady=5)
            label.pack(anchor="w")
        
        print(employee_info)
    
    def show_parent_info(self,student_id):
        parent_info = self.get_parent(cursor,student_id)
        print(parent_info)
        student_id,mail,tel_no,name_surname=parent_info
        message = f"Öğrenci İd: {student_id}\nMail: {mail}\nTelefon Numarası: {tel_no}\nAd Soyad:{name_surname}"
        messagebox.showinfo("Aile Bilgiler", message)

    def search_parent(self):

        # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Aile Ara")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğrenci ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        print("asdsclear")
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_parent_info(entry.get()))
        search_button.pack(pady=10)
    

    #####################################################
    def get_all_students(self,cursor):
        cursor.execute('''
            select s.student_id ,p.name ,p.surname ,p.age ,s.department,p.mail,p.tel_no,p.address
            from student s
            join person p on s.student_id=p.person_id
        ''')
        values = cursor.fetchall()
        return values
    
    def get_active_students(self,cursor):
        cursor.execute('''
            select p.*
            from active_student s
            join person p on s.student_id = p.person_id 
        ''')
        values = cursor.fetchall()
        return(values)
    
    def get_graduated_students(self,cursor):
        cursor.execute('''
            select s.graduate_date, s.grade, p.*
            from graduated_student s
            join person p on s.student_id = p.person_id 
        ''')
        values = cursor.fetchall()
        return(values)
         
    def get_student_by_id(self,cursor, student_id):
        cursor.execute('''
            SELECT p.*
            FROM person p
            JOIN student s ON p.person_id = s.student_id
            WHERE s.student_id = %s
        ''', (student_id,))

        student = cursor.fetchone()
        return student
    
    def get_all_employees(self,cursor):
        cursor.execute('''
            select e.*
            from employee e
        ''')
        values = cursor.fetchall()
        return(values)

    def get_all_teachers(self,cursor):
        cursor.execute('''
            select e.employee_id , p.name, p.surname,e.salary  ,t.course_id
            from employee e
            join teacher t on t.teacher_id = e.employee_id
            join person p on t.teacher_id = p.person_id
        ''')
        values = cursor.fetchall()
        return (values)

    def get_teacher(self,cursor,teacher_id):

        cursor.execute('''
            SELECT e.employee_id , p.name, p.surname,e.salary  ,t.course_id
            FROM teacher t
            join employee e on t.teacher_id = e.employee_id
            join person p on e.employee_id = p.person_id
            where t.teacher_id = %s 
        ''',(teacher_id,))
        value = cursor.fetchone()
        return value

    def clear_labels(self):
        # Destroy all stored labels
        for label in self.labels:
            print("asd")
            label.destroy()
        # Clear the list of labels
        self.labels = [] 
    
    def get_employee(self,employee_id):
        cursor.execute('''
            select e.salary,p.*
            from employee e
            join person p on p.person_id = e.employee_id
        ''')
        values = cursor.fetchone()
        
        return values
    
    def get_all_parents(self,cursor):
        cursor.execute('''
            select p.*
            from active_student s
            join parents p on s.student_id = p.student_id
        ''')
        values = cursor.fetchall()
        return(values)
    
    def get_parent(self, cursor, student_id):
        cursor.execute('''
            SELECT p.*
            FROM active_student s
            JOIN parents p ON s.student_id = p.student_id
            WHERE s.student_id = %s
        ''', (student_id,))  # Pass student_id as a tuple

        values = cursor.fetchone()
        return values
    
    def get_student_request(self, cursor, student_id):
        cursor.execute('''
            SELECT sr.*
            FROM student_request sr
            WHERE sr.student_id = %s
        ''', (student_id,))
        values = cursor.fetchall()
        return values

    def get_teacher_available_hours(self,cursor,teacher_id):
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
        
        return self.print_program(schedule)
    
    def get_teacher_program(self, cursor,teacher_id):
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
        return self.print_program(schedule)
        
    def get_student_available_sections(self,cursor,student_id):
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
        return self.print_program(schedule)

    def get_student_program(self,student_id):
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
        return self.print_program(schedule)

    def print_program(self,course_array):
        schedule = [["" for _ in range(len(time_slots))] for _ in range(len(days))]

        for course_id, day_section in course_array:
            day_index = day_section // 10
            time_slot_index = day_section % 10
            schedule[day_index][time_slot_index] = str(course_id)

        schedule_program = ("\t\t" + "\t\t".join(time_slot for time_slot in time_slots)) + "\n"

        for i, day in enumerate(days):
            schedule_program+=(f"{day}\t\t" + "\t\t".join(cell if cell != '' else '-' for cell in schedule[i]))
            schedule_program+="\n"
        return schedule_program
        
    def close_window(self):
        root.destroy()

class InsertTeacher(tk.Toplevel):
    def __init__(self, insert_callback):
        super().__init__()
        self.title("Insert Data")

        self.age_label = ttk.Label(self, text="Age:")
        self.mail_label = ttk.Label(self, text="Mail:")
        self.tel_no_label = ttk.Label(self, text="Tel no:")
        self.address_label = ttk.Label(self, text="Address:")
        self.name_label = ttk.Label(self, text="Name:")
        self.surname_label = ttk.Label(self, text="Surname:")
        self.salary_label = ttk.Label(self, text="Salary:")
        self.course_id_label = ttk.Label(self, text="Course_id:")

        self.age_entry = ttk.Entry(self)
        self.mail_entry = ttk.Entry(self)
        self.tel_no_entry = ttk.Entry(self)
        self.address_entry = ttk.Entry(self)
        self.name_entry = ttk.Entry(self)
        self.surname_entry = ttk.Entry(self)
        self.salary_entry = ttk.Entry(self)
        self.course_id_entry = ttk.Entry(self)

        self.insert_button = ttk.Button(self, text="Insert", command=self.insert_teacher)

        self.age_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.mail_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.tel_no_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.address_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.name_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.surname_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.salary_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.course_id_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.age_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.mail_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.tel_no_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.address_entry.grid (row=3, column=1, padx=10, pady=5, sticky="w")
        self.name_entry.grid (row=4, column=1, padx=10, pady=5, sticky="w")
        self.surname_entry.grid (row=5, column=1, padx=10, pady=5, sticky="w")
        self.salary_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.course_id_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.insert_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.insert_callback = insert_callback



    def insert_teacher(self):
        age = self.age_entry.get()
        mail = self.mail_entry.get()
        tel_no = self.tel_no_entry.get()
        address = self.address_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        salary = self.salary_entry.get()
        course_id = self.course_id_entry.get()
        # Call the insert function with the obtained values
        self.insert_callback(age,mail,tel_no,address, name, surname,salary,course_id)
        self.destroy()

class InsertStudentRequest(tk.Toplevel):
    def __init__(self, insert_callback):
        super().__init__()
        self.title("Insert Data")
        self.student_id_label = ttk.Label(self, text="Student_id:")
        self.course_id_label = ttk.Label(self, text="Course_id:")

        self.student_id_entry = ttk.Entry(self)
        self.course_id_entry = ttk.Entry(self)

        self.insert_button = ttk.Button(self, text="Insert", command=self.insert_student_request)

        self.student_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.course_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.student_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.course_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.insert_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.insert_callback = insert_callback



    def insert_student_request(self):
        student_id = self.student_id_entry.get()
        course_id = self.course_id_entry.get()
        # Call the insert function with the obtained values
        self.insert_callback(student_id,course_id)
        self.destroy()

class InsertDialog(tk.Toplevel):
    def __init__(self, insert_callback):
        super().__init__()

        self.title("Insert Data")

        self.department_label = ttk.Label(self, text= "Department:")
        self.age_label = ttk.Label(self, text="Age:")
        self.mail_label = ttk.Label(self, text="Mail:")
        self.tel_no_label = ttk.Label(self, text="Tel no:")
        self.address_label = ttk.Label(self, text="Address:")
        self.name_label = ttk.Label(self, text="Name:")
        self.surname_label = ttk.Label(self, text="Surname:")


        self.department_entry = ttk.Entry(self)
        self.age_entry = ttk.Entry(self)
        self.mail_entry = ttk.Entry(self)
        self.tel_no_entry = ttk.Entry(self)
        self.address_entry = ttk.Entry(self)
        self.name_entry = ttk.Entry(self)
        self.surname_entry = ttk.Entry(self)

        self.insert_button = ttk.Button(self, text="Insert", command=self.insert_active_student)

        self.department_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.age_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mail_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.tel_no_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.address_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.name_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.surname_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.department_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.age_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.mail_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.tel_no_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.address_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.name_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.surname_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.insert_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.insert_callback = insert_callback



    def insert_active_student(self):
        department = self.department_entry.get()
        age = self.age_entry.get()
        mail = self.mail_entry.get()
        tel_no = self.tel_no_entry.get()
        address = self.address_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        # Call the insert function with the obtained values
        self.insert_callback(department,age,mail,tel_no,address, name, surname)
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UBSManagementSystem(root)
    
    root.mainloop()
