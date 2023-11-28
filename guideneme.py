import tkinter as tk
from tkinter import ttk
import mysql.connector

# Replace these with your actual database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '327275',
    'database': 'ubs',
}

# Create a MySQL connection
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

def get_all_students():
    cursor.execute('''
        SELECT *
        FROM student s
        JOIN person p ON s.student_id = p.person_id
    ''')
    values = cursor.fetchall()
    return values

def get_active_students():
    cursor.execute('''
        SELECT p.*
        FROM active_student s
        JOIN person p ON s.student_id = p.person_id
    ''')
    values = cursor.fetchall()
    return values

def get_graduated_students():
    cursor.execute('''
        SELECT s.graduate_date, s.grade, p.*
        FROM graduated_student s
        JOIN person p ON s.student_id = p.person_id
    ''')
    values = cursor.fetchall()
    return values

def get_all_parents():
    cursor.execute('''
        SELECT p.*
        FROM active_student s
        JOIN parents p ON s.student_id = p.student_id
    ''')
    values = cursor.fetchall()
    return values

def get_all_employees():
    cursor.execute('''
        SELECT e.*
        FROM employee e
    ''')
    values = cursor.fetchall()
    return values

def get_all_teachers():
    cursor.execute('''
        SELECT e.*, t.course_id
        FROM employee e
        JOIN teacher t ON t.teacher_id = e.employee_id
    ''')
    values = cursor.fetchall()
    return values

def display_results(data):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    for item in data:
        result_text.insert(tk.END, str(item) + '\n')
    result_text.config(state=tk.DISABLED)

def on_select():
    selected_tab = tab_control.index(tab_control.select())
    data_function = tabs[selected_tab][1]
    display_results(data_function())

# Create the main window
root = tk.Tk()
root.title("UBS Database Viewer")

# Create a notebook (tabs)
tab_control = ttk.Notebook(root)

# Define tabs
tabs = [
    ("All Students", get_all_students),
    ("Active Students", get_active_students),
    ("Graduated Students", get_graduated_students),
    ("All Parents", get_all_parents),
    ("All Employees", get_all_employees),
    ("All Teachers", get_all_teachers),
]

# Create tabs and populate them with data
for tab_name, _ in tabs:
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=tab_name)

# Create a button to fetch data
fetch_button = tk.Button(root, text="Fetch Data", command=on_select)
fetch_button.pack(pady=10)

# Create a text widget to display the results
result_text = tk.Text(root, wrap=tk.WORD, height=20, width=80, state=tk.DISABLED)
result_text.pack(padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()

# Close the database connection when the application is closed
cursor.close()
connection.close()
