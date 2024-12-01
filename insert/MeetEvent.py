import mysql.connector
import csv

# RDS Connection Configuration
rds_config = {
    "host": "cpsc-445-rds.czqa224ckmrq.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "CPSC445password",
    "database": "NVSL"
}

# CSV File Path
csv_file_path = "data\MeetEvent.csv"

# Table Name
table_name = "MeetEvent"

# Connect to RDS
try:
    connection = mysql.connector.connect(**rds_config)
    cursor = connection.cursor()

    print("Connected to RDS successfully!")

    # Open and Read the CSV File
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        column_names = csv_reader.fieldnames  # Get column headers from the CSV

        # Construct the SQL INSERT Statement
        columns = ", ".join(column_names)
        placeholders = ", ".join(["%s"] * len(column_names))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Insert Rows from CSV into the Table
        for row in csv_reader:
            values = tuple(row[column] for column in column_names)
            cursor.execute(insert_query, values)

        # Commit the Changes
        connection.commit()
        print(f"Data from {csv_file_path} inserted successfully into {table_name}!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the Cursor and Connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Connection to RDS closed.")
