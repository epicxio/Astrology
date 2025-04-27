import mysql.connector
from mysql.connector import Error
import os

def init_places():
    try:
        # Get database configuration from environment variables
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'epic_x_horoscope')
        }

        # Connect to MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file_path = os.path.join(current_dir, 'indian_cities.sql')

        # Read and execute SQL file
        with open(sql_file_path, 'r') as sql_file:
            sql_commands = sql_file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
                    connection.commit()

        print("Successfully initialized places table with Indian cities data")

    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    init_places() 