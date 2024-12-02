import mysql.connector
from mysql.connector import errorcode

# RDS connection details
db_host = "database-1.czqa224ckmrq.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "CPSC445password"
db_name = "NVSL"

def execute_sql_file(cursor, file_path):
    """
    Execute SQL commands from a file.
    """
    with open(file_path, 'r') as file:
        sql_commands = file.read()
    commands = sql_commands.split(';')  # Split into individual commands
    for command in commands:
        if command.strip():  # Skip empty commands
            try:
                cursor.execute(command)
                print("Executed command successfully.")
            except mysql.connector.Error as err:
                print(f"Failed to execute command: {err}")

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database {db_name} already exists.")
        else:
            print(f"Failed to create database: {err}")
            exit(1)

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        print("Connected to RDS successfully.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def main():
    sql_file_path = "sql\CreateNVSLTables.sql"  # Path to your SQL file

    # Connect to RDS
    conn = connect_to_database()
    cursor = conn.cursor()

    # Create database if it doesn't exist
    try:
        conn.database = db_name
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            conn.database = db_name
        else:
            print(f"Error: {err}")
            exit(1)

    # Execute SQL file to create tables
    execute_sql_file(cursor, sql_file_path)

    # Clean up
    cursor.close()
    conn.close()
    print("Database and tables setup complete.")

if __name__ == "__main__":
    main()
