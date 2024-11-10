import csv
import pymysql

# Database configuration
db_host = "cpsc-445-rds.czqa224ckmrq.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "CPSC445password"
db_name = "NVSL"

def insert_data_to_meet_table(csv_file_path):
    # Connect to the RDS MySQL database
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Insert query for the Meet table
            insert_query = """
            INSERT INTO Meet (
                meetID, teamID_Home, teamID_Away, teamPoints_Home, 
                teamPoints_Away, Title, Year, Date, Location, 
                Division, Course
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Open the CSV file and read its content
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row if present
                for row in csv_reader:
                    # Cast values as necessary to match the table schema
                    row_data = [
                        row[0],  # meetID
                        row[1],  # teamID_Home
                        row[2],  # teamID_Away
                        float(row[3]),  # teamPoints_Home
                        float(row[4]),  # teamPoints_Away
                        row[5],  # Title
                        int(row[6]),  # Year
                        row[7],  # Date (should be in YYYY-MM-DD format)
                        row[8],  # Location
                        int(row[9]),  # Division
                        row[10]  # Course
                    ]
                    cursor.execute(insert_query, row_data)

            # Commit changes to the database
            connection.commit()
            print("Data inserted successfully into the Meet table.")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()  # Rollback in case of error

    finally:
        connection.close()

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = 'data\NVSL_DB_Meets.csv'
    
    insert_data_to_meet_table(csv_file_path)
