import csv
import pymysql

# Database configuration
db_host = "cpsc-445-rds.czqa224ckmrq.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "CPSC445password"
db_name = "NVSL"

def insert_data_to_event_table(csv_file_path):
    # Connect to the RDS MySQL database
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Insert query for the Event table
            insert_query = """
            INSERT INTO Event (
                eventID, meetID, Event_Number, Gender, 
                Age_Group, Distance, Stroke, Individual
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Open the CSV file and read its content
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row if present
                for row in csv_reader:
                    # Cast values as necessary to match the table schema
                    row_data = [
                        row[0],  # eventID
                        row[1],  # meetID
                        int(row[2]),  # Event_Number
                        row[3],  # Gender
                        row[4],  # Age_Group
                        int(row[5]),  # Distance
                        row[6],  # Stroke
                        row[7]   # Individual
                    ]
                    cursor.execute(insert_query, row_data)

            # Commit changes to the database
            connection.commit()
            print("Data inserted successfully into the Event table.")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()  # Rollback in case of error

    finally:
        connection.close()

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = 'data\NVSL_DB_Events.csv'
    
    insert_data_to_event_table(csv_file_path)
