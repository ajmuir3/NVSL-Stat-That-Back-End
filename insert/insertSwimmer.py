import csv
import pymysql

# Database configuration
db_host = "cpsc-445-rds.czqa224ckmrq.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "CPSC445password"
db_name = "NVSL"

def insert_data_to_swimmer_table(csv_file_path):
    # Connect to the RDS MySQL database
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Insert query for the Swimmer table
            insert_query = """
            INSERT INTO Swimmer (
                swimmerID, teamID, Name
            ) 
            VALUES (%s, %s, %s)
            """

            # Open the CSV file and read its content
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row if present
                for row in csv_reader:
                    # Prepare the row data
                    row_data = [
                        row[0],  # swimmerID
                        row[1],  # teamID
                        row[2]   # Name
                    ]
                    cursor.execute(insert_query, row_data)

            # Commit changes to the database
            connection.commit()
            print("Data inserted successfully into the Swimmer table.")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()  # Rollback in case of error

    finally:
        connection.close()

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = 'data\NVSL_DB_Swimmers.csv'
    
    insert_data_to_swimmer_table(csv_file_path)
