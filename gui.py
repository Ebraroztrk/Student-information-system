import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import messagebox

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'ubs',
}

days = ["Pzt", "Sali", "Crs", "Prs", "Cuma"]
time_slots = ["08:30-10:30", "10:30-12:30", "12:30-14:30", "14:30-16:30", "16:30-18:30"]


connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

class UBSManagementSystem:


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

        style = ttk.Style(self.root)
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12), background=background_color, foreground=text_color)

        # Toolbar oluşturun
        self.toolbar = tk.Frame(self.root, bg=background_color)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        #Labels
        self.labels = []
    

        # "Öğrenciler" butonu
        self.btn_students = tk.Menubutton(self.toolbar, text="Öğrenciler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_students.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Öğrenciler" butonunun altındaki menü
        self.students_menu = tk.Menu(self.btn_students, tearoff=0)
        self.students_menu.add_command(label="Öğrenci Ara", command=self.search_student)
        self.students_menu.add_command(label="Tüm Öğrenciler", command=self.show_all_students)
        self.students_menu.add_command(label="Aktif Öğrenciler", command=self.show_active_students)
        self.students_menu.add_command(label="Mezun Öğrenciler", command=self.show_graduated_students)
        self.btn_students.config(menu=self.students_menu)

        self.submenu_students = tk.Menu(self.students_menu, tearoff=0)
        self.submenu_students.add_command(label="Öğrenci Ekle", command=self.insert_student)
        
        # "Öğrenciler" menüsüne alt menüyü ekle
        self.students_menu.add_cascade(label="Öğrenci İşlemleri", menu=self.submenu_students)
        
        self.btn_students.config(menu=self.students_menu)


        # "Öğretmenler" butonu
        self.btn_teachers = tk.Menubutton(self.toolbar, text="Öğretmenler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_teachers.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Öğretmenler" butonunun altındaki menü
        self.teachers_menu = tk.Menu(self.btn_teachers, tearoff=0)
        self.teachers_menu.add_command(label="Öğretmen Ara", command=self.search_teacher)
        self.teachers_menu.add_command(label="Tüm Öğretmenler", command=self.show_all_teachers)
        self.teachers_menu.add_command(label="Öğretmenlerin Programları", command=self.search_teacher_avail_hours)
        
        self.btn_teachers.config(menu=self.teachers_menu)

        # "Çalışanlar" butonu
        self.btn_employees = tk.Menubutton(self.toolbar, text="Çalışanlar", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_employees.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Çalışanlar" butonunun altındaki menü
        self.employees_menu = tk.Menu(self.btn_employees, tearoff=0)
        self.employees_menu.add_command(label="Çalışan Ara", command=self.get_employee_by_id)

        self.employees_menu.add_command(label="Öğretmenler", command=self.show_all_teachers)
        self.employees_menu.add_command(label="Yöneticiler", command=self.show_all_admins)
        
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

        input_frame = ttk.Frame(root, padding=(10, 10, 10, 10))
        input_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        




        ###################################################################################
        ##FUNCTIONS

    def insert_student(self):
        # Yeni pencere oluştur
        insert_window = tk.Toplevel(root)
        insert_window.title("Öğrenci Ekle")

        # Giriş alanları için bir çerçeve oluştur
        input_frame = ttk.Frame(insert_window, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Giriş alanları oluştur
        ttk.Label(input_frame, text="Bölüm:").grid(column=0, row=0, sticky=tk.W)
        department_entry = ttk.Entry(input_frame)
        department_entry.grid(column=1, row=0, sticky=tk.W)

        ttk.Label(input_frame, text="Yaş:").grid(column=0, row=1, sticky=tk.W)
        age_entry = ttk.Entry(input_frame)
        age_entry.grid(column=1, row=1, sticky=tk.W)

        ttk.Label(input_frame, text="Mail:").grid(column=0, row=2, sticky=tk.W)
        mail_entry = ttk.Entry(input_frame)
        mail_entry.grid(column=1, row=2, sticky=tk.W)

        ttk.Label(input_frame, text="Telefon No:").grid(column=0, row=3, sticky=tk.W)
        tel_no_entry = ttk.Entry(input_frame)
        tel_no_entry.grid(column=1, row=3, sticky=tk.W)

        ttk.Label(input_frame, text="Adres:").grid(column=0, row=4, sticky=tk.W)
        address_entry = ttk.Entry(input_frame)
        address_entry.grid(column=1, row=4, sticky=tk.W)

        ttk.Label(input_frame, text="Ad:").grid(column=0, row=5, sticky=tk.W)
        name_entry = ttk.Entry(input_frame)
        name_entry.grid(column=1, row=5, sticky=tk.W)

        ttk.Label(input_frame, text="Soyad:").grid(column=0, row=6, sticky=tk.W)
        surname_entry = ttk.Entry(input_frame)
        surname_entry.grid(column=1, row=6, sticky=tk.W)

        # "Öğrenci Ekle" butonu
        insert_button = tk.Button(insert_window, text="Öğrenci Ekle", command=lambda: self.add_active_student(
            department_entry.get(), age_entry.get(), mail_entry.get(),
            tel_no_entry.get(), address_entry.get(), name_entry.get(), surname_entry.get()
        ))
        insert_button.grid(column=0, row=1, sticky=tk.W)


    def add_active_student(self):
        # Kullanıcının girdiği değerleri al
        department = self.department_entry.get()
        age = self.age_entry.get()
        mail = self.mail_entry.get()
        tel_no = self.tel_no_entry.get()
        address = self.address_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        # student_id'yi al

        # Veritabanına ekleme işlemlerini gerçekleştir
        self.insert_active_student()
            


    def get_request_count(self):
        cursor.execute('''
            SELECT request_id FROM section_request ORDER BY request_id DESC LIMIT 1;
        ''')
        request_count_tuple = cursor.fetchone()
        count_value = request_count_tuple[0]
        request_count_int = int(count_value)
        return request_count_int

    def insert_active_student(self,department,age,mail,tel_no,address,name,surname):
        student_id = self.get_person_count()+1
        self.insert_person(self,student_id,age,mail,tel_no,address,name,surname)
        cursor.execute('''
            INSERT INTO Student(student_id, department)
            VALUES (%s, %s)
        ''', (student_id, department))

    def insert_person(self,person_id,age,mail,tel_no,address,name,surname):
        cursor.execute('''
            INSERT INTO Person (person_id, age, mail, tel_no, address, name, surname)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (person_id, age, mail, tel_no, address, name, surname))

#admin falan eklendiginde otomatik person da olussun diye yazdim
    def insert_employee(employee_id,salary):
        cursor.execute('''
            INSERT INTO Employee (employee_id, salary)
            VALUES (%s, %s)
        ''', (employee_id, salary))    

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
        search_window.title("Öğretmen Programı")
        # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Öğretmen ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

        # "Ara" butonu
        search_button = tk.Button(search_window, text="Ara", command=lambda: self.show_teacher_avail_hours(entry.get()))
        
        search_button.pack(pady=10)

    def show_teacher_avail_hours(self, teacher_id):
        print("A")
        program_data = self.get_teacher_available_hours(cursor, teacher_id)  # Use self to access the method

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
    
    def show_student_info(self,student_id):
        student_info = self.get_student_by_id(cursor,student_id)  # Use self to access the method
        student_id, age, mail, tel_no, address, name, surname = student_info
        message = f"Öğrenci ID: {student_id}\nAd: {name}\nSoyad: {surname}\nYaş: {age}\nMail: {mail}\nCep No: {tel_no}\nAdres: {address}\n"
        messagebox.showinfo("Öğrenci Bilgileri", message)

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
    # Arama penceresi oluştur
        search_window = tk.Toplevel(self.root)
        search_window.title("Çalışan Ara")
    # Etiket ve giriş kutusu oluştur
        label = tk.Label(search_window, text="Çalışan ID'sini girin:")
        label.pack(pady=5)

        entry = tk.Entry(search_window)
        entry.pack(pady=5)

    # "Ara" butonu
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



if __name__ == "__main__":
    root = tk.Tk()
    app = UBSManagementSystem(root)
    root.mainloop()
