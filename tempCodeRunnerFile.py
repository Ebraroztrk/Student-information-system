import mysql.connector
import random
import string
from datetime import datetime, timedelta
from random import randint, choice, sample

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



try:
    if connection.is_connected():
        user_input = "age,name,surname,address,mail,tel_no"
        columns_to_display = [col.strip() for col in user_input.split(',')]
        get_dynamic_person(*columns_to_display)
        connection.commit()

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("Connection closed")