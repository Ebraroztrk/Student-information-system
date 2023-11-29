import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import messagebox

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '327275',
    'database': 'ubs',
}



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

        # "Öğretmenler" butonu
        self.btn_teachers = tk.Menubutton(self.toolbar, text="Öğretmenler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_teachers.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Öğretmenler" butonunun altındaki menü
        self.teachers_menu = tk.Menu(self.btn_teachers, tearoff=0)
        self.teachers_menu.add_command(label="Öğretmen Ara", command=self.search_teacher)
        self.teachers_menu.add_command(label="Tüm Öğretmenler", command=self.show_all_teachers)
        self.btn_teachers.config(menu=self.teachers_menu)

        # "Çalışanlar" butonu
        self.btn_employees = tk.Menubutton(self.toolbar, text="Çalışanlar", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_employees.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Çalışanlar" butonunun altındaki menü
        self.employees_menu = tk.Menu(self.btn_employees, tearoff=0)
        self.employees_menu.add_command(label="Çalışan Ara", command=self.get_employee_by_id)

        self.employees_menu.add_command(label="Öğretmenler", command=self.show_all_teachers)
        self.employees_menu.add_command(label="Temizlikçiler", command=self.show_cleaners)
        self.employees_menu.add_command(label="İdareciler", command=self.show_administrators)
        self.employees_menu.add_command(label="Tüm Çalışanlar", command=self.show_all_employees)
        self.btn_employees.config(menu=self.employees_menu)

        # "Aileler" butonu
        self.btn_families = tk.Menubutton(self.toolbar, text="Aileler", bg=button_color, fg=text_color, borderwidth=2, relief="solid")
        self.btn_families.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # "Aileler" butonunun altındaki menü
        self.families_menu = tk.Menu(self.btn_families, tearoff=0)
        self.families_menu.add_command(label="Aile Ara", command=self.show_all_parents)
        self.families_menu.add_command(label="Tüm Aileler", command=self.show_all_parents)
        self.btn_families.config(menu=self.families_menu)



        # Notebook oluşturun
        self.notebook = ttk.Notebook(self.root)
        self.style = ttk.Style()
        self.style.configure('TFrame', background=background_color)

        self.tab_general = ttk.Frame(self.notebook, style='TFrame')



        # "Generate Report" butonu
        self.btn_generate_report = tk.Button(self.tab_general, text="Rapor Oluştur", command=self.generate_report, bg=button_color, fg=text_color)
        self.btn_generate_report.pack(pady=20)

        self.notebook.pack(fill=tk.BOTH, expand=True)
        ###################################################################################
        ##FUNCTIONS

    def generate_report(self):
        messagebox.showinfo("Bilgi", "Rapor başarıyla oluşturuldu.")
    
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
        self.clear_labels()

        student_info = self.get_student_by_id(cursor,student_id)  # Use self to access the method
        student_id, age, mail, tel_no, address, name, surname = student_info
        labels = [
            f"Öğrenci ID: {student_id}",
            f"Ad: {name}",
            f"Soyad: {surname}",
            f"Yaş: {age}",
            f"Mail: {mail}",
            f"Cep No: {tel_no}",
            f"Adres: {address}",
        ]
        for label_text in labels:
            label = tk.Label(self.root, text=label_text, padx=10, pady=5)
            label.pack(anchor="w")

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
        labels = [
            f"Öğretmen ID: {teacher_id}",
            f"Ad: {name}",
            f"Soyad: {surname}",
            f"Maaş: {salary} $",
            f"Ders Kodu: {course}",
        ]
        for label_text in labels:
            label = tk.Label(self.root, text=label_text, padx=10, pady=5)
            label.pack(anchor="w")
        
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
        print("SHOW EMPLOYEE INFO")
    # Assuming you have a function to display employee info, modify as needed
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
    # You can then display or use the employee_info as needed
    # ...

    def show_administrators(self):
        messagebox.showinfo("İdareciler", "İdareci bilgileri burada görüntülenecek.")

    def show_all_employees(self):
        messagebox.showinfo("Tüm Çalışanlar", "Tüm çalışan bilgileri burada görüntülenecek.")

    def show_employees(self):
        self.notebook.select(self.tab_employees)

    def show_families(self):
        messagebox.showinfo("Aileler", "Aile bilgileri burada görüntülenecek.")

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
    
    def get_employee(self, cursor, employee_id):
        cursor.execute('''
            SELECT *
            FROM employee e
            WHERE employee_id = %s
        ''', (employee_id,))
        
        employee = cursor.fetchone()
        print(employee)
        return employee
    
    def get_all_parents(self,cursor):
        cursor.execute('''
            select p.*
            from active_student s
            join parents p on s.student_id = p.student_id
        ''')
        values = cursor.fetchall()
        return(values)
if __name__ == "__main__":
    root = tk.Tk()
    app = UBSManagementSystem(root)
    root.mainloop()