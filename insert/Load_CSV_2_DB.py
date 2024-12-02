import csv
import pymysql

# Database connection details
db_host = 'database-1.czqa224ckmrq.us-east-1.rds.amazonaws.com'
db_user = 'admin'
db_password = 'password'
db_name = 'NVSL'

# Connect to the database
connection = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Define the path to your CSV file
csv_file_path = 'NVSL_Teams2.csv'

def insert_into_database(row):
    with connection.cursor() as cursor:
        # Example INSERT INTO command, adjust table name and columns as necessary
        sql = "INSERT INTO Team (team_name, team_abbr) VALUES (%s, %s)"
        cursor.execute(sql, (row[0], row[1]))
        connection.commit()

try:
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            print(f"Processing row: {row}")
            insert_into_database(row)
finally:
    connection.close()
