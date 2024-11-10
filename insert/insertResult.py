import csv
import pymysql

# Database configuration
db_host = "cpsc-445-rds.czqa224ckmrq.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "CPSC445password"
db_name = "NVSL"

def insert_data_to_result_table(csv_file_path):
    # Connect to the RDS MySQL database
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            
            # Insert query for the Result table
            insert_query = """
            INSERT INTO Result (
                resultID, eventID, swimmerID, Time, Place, Points, PowerIndex
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            # Open the CSV file and read its content
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row if present
                for row in csv_reader:
                    # Cast values as necessary to match the table schema
                    row_data = [
                        row[0],  # resultID
                        row[1],  # eventID
                        row[2],  # swimmerID
                        float(row[3]) if row[3] else None,  # Time
                        int(row[4]) if row[4] else None,  # Place
                        float(row[5]) if row[5] else None,  # Points
                        float(row[6]) if row[6] else None  # PowerIndex
                    ]
                    cursor.execute(insert_query, row_data)

            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # Commit changes to the database
            connection.commit()
            print("Data inserted successfully into the Result table.")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()  # Rollback in case of error

    finally:
        connection.close()

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = 'data/NVSL_DB_Results.csv'  # Updated path with forward slashes
    
    insert_data_to_result_table(csv_file_path)
