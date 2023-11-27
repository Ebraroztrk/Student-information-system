import mysql.connector

# Replace these values with your MySQL server configuration
host = "localhost"
user = "root"
password = "327275"
database = "ubs"

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to MySQL server")

        # Perform your MySQL operations here

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the connection when done
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")


