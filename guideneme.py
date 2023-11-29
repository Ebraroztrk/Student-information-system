import tkinter as tk
from tkinter import ttk

class StudentInsertionGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Insert Student")

        # Department
        self.department_label = ttk.Label(master, text="Department:")
        self.department_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.department_entry = ttk.Entry(master)
        self.department_entry.grid(row=0, column=1, padx=10, pady=5)

        # Age
        self.age_label = ttk.Label(master, text="Age:")
        self.age_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.age_entry = ttk.Entry(master)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        # Mail
        self.mail_label = ttk.Label(master, text="Mail:")
        self.mail_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.mail_entry = ttk.Entry(master)
        self.mail_entry.grid(row=2, column=1, padx=10, pady=5)

        # Telephone Number
        self.tel_no_label = ttk.Label(master, text="Telephone Number:")
        self.tel_no_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.tel_no_entry = ttk.Entry(master)
        self.tel_no_entry.grid(row=3, column=1, padx=10, pady=5)

        # Address
        self.address_label = ttk.Label(master, text="Address:")
        self.address_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.address_entry = ttk.Entry(master)
        self.address_entry.grid(row=4, column=1, padx=10, pady=5)

        # Name
        self.name_label = ttk.Label(master, text="Name:")
        self.name_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(master)
        self.name_entry.grid(row=5, column=1, padx=10, pady=5)

        # Surname
        self.surname_label = ttk.Label(master, text="Surname:")
        self.surname_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.surname_entry = ttk.Entry(master)
        self.surname_entry.grid(row=6, column=1, padx=10, pady=5)

        # Button to execute the insertion
        self.insert_button = ttk.Button(
            master,
            text="Insert Student",
            command=self.insert_student
        )
        self.insert_button.grid(row=7, column=0, columnspan=2, pady=10)

    def insert_student(self):
        department = self.department_entry.get()
        age = self.age_entry.get()
        mail = self.mail_entry.get()
        tel_no = self.tel_no_entry.get()
        address = self.address_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()

        insert(department, age, mail, tel_no, address, name, surname)

def insert(department, age, mail, tel_no, address, name, surname):
    print("Inserting student:")
    print(f"Department: {department}")
    print(f"Age: {age}")
    print(f"Mail: {mail}")
    print(f"Telephone Number: {tel_no}")
    print(f"Address: {address}")
    print(f"Name: {name}")
    print(f"Surname: {surname}")

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Main App")

        # Create a toolbar with an "Insert Student" button
        toolbar = tk.Frame(master)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        insert_student_button = ttk.Button(toolbar, text="Insert Student", command=self.open_insert_student_window)
        insert_student_button.pack(side=tk.LEFT, padx=5, pady=5)

    def open_insert_student_window(self):
        insert_window = tk.Toplevel(self.master)
        student_insertion_gui = StudentInsertionGUI(insert_window)

# Create the main Tkinter window
root = tk.Tk()

# Create an instance of the MainApp
main_app = MainApp(root)

# Start the Tkinter event loop
root.mainloop()
