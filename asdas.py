import tkinter as tk
from tkinter import ttk
import mysql.connector
def get_dynamic_person(cursor, columns):
    # Ensure all elements in columns are strings
    columns = [str(col) for col in columns]

    view_name = f'dynamic_personview{"_".join(columns)}'

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
    values = cursor.fetchall()
    print(values)

def apply_filter():
    selected_columns = [col for i, col in enumerate(columns_to_display) if checkboxes[i].get() == 1]
    get_dynamic_person(cursor, selected_columns)

root = tk.Tk()
root.title("Filter Page")

host = "localhost"
user = "root"
password = "327275"
database = "ubs"
# Create a cursor
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = connection.cursor()

# Create checkboxes for each column
checkboxes = []
columns_to_display = ["age", "name", "surname", "address", "mail", "tel_no"]

for col in columns_to_display:
    var = tk.IntVar()
    checkbox = tk.Checkbutton(root, text=col, variable=var)
    checkbox.grid(sticky="w")
    checkboxes.append(var)

# Create "Filter" button
filter_button = tk.Button(root, text="Filtrele", command=apply_filter)
filter_button.grid(row=len(columns_to_display), columnspan=2)

root.mainloop()
