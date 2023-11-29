import mysql.connector
from tkinter import Tk, Label, StringVar, Checkbutton, Button, messagebox

host = "localhost"
user = "root"
password = "327275"
database = "ubs"

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = connection.cursor()

class DynamicPersonFilterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Person Filter")

        # Label
        self.label = Label(root, text="Select Filters:")
        self.label.pack()

        # Checkboxes
        self.age_var = StringVar()
        self.age_cb = Checkbutton(root, text="Age", variable=self.age_var)
        self.age_cb.pack()

        self.name_var = StringVar()
        self.name_cb = Checkbutton(root, text="Name", variable=self.name_var)
        self.name_cb.pack()

        self.surname_var = StringVar()
        self.surname_cb = Checkbutton(root, text="Surname", variable=self.surname_var)
        self.surname_cb.pack()

        self.address_var = StringVar()
        self.address_cb = Checkbutton(root, text="Address", variable=self.address_var)
        self.address_cb.pack()

        self.mail_var = StringVar()
        self.mail_cb = Checkbutton(root, text="Mail", variable=self.mail_var)
        self.mail_cb.pack()

        self.tel_no_var = StringVar()
        self.tel_no_cb = Checkbutton(root, text="Telephone Number", variable=self.tel_no_var)
        self.tel_no_cb.pack()

        # Button to apply filters
        self.apply_button = Button(root, text="Apply Filters", command=self.apply_filters)
        self.apply_button.pack()

    def apply_filters(self):
        selected_columns = []
        if self.age_var.get() == "1":
            selected_columns.append("age")
        if self.name_var.get() == "1":
            selected_columns.append("name")
        if self.surname_var.get() == "1":
            selected_columns.append("surname")
        if self.address_var.get() == "1":
            selected_columns.append("address")
        if self.mail_var.get() == "1":
            selected_columns.append("mail")
        if self.tel_no_var.get() == "1":
            selected_columns.append("tel_no")

        try:
            if connection.is_connected():
                self.get_dynamic_person(*selected_columns)
                connection.commit()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def get_dynamic_person(self, *columns):
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
        values = cursor.fetchall()
        print(values)


if __name__ == "__main__":
    root = Tk()
    app = DynamicPersonFilterGUI(root)
    root.mainloop()
