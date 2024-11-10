import csv
import pymysql

# Database configuration
db_host = "cpsc-445-rds.czqa224ckmrq.us-east-1.rds.amazonaws.com"
db_user = "admin"
db_password = "CPSC445password"
db_name = "NVSL"

def insert_data_to_teams_table(csv_file_path):
    # Connect to the RDS MySQL database
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        with connection.cursor() as cursor:
            # Insert query for the teams table
            insert_query = """
            INSERT INTO teams (
                teamID, teamName, teamAbbr, seasonYear, divisionNum, 
                winCount, lossCount, tieCount, dual_meetPoints, 
                divisional_relayPoints, divisionalPoints, 
                all_star_relayPoints, all_star_Points, 
                totalPoints, grand_totalPoints, powerRanking
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Open the CSV file and read its content
            with open(csv_file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header row if present
                for row in csv_reader:
                    # Cast values as necessary to match the table schema
                    row_data = [
                        row[0],  # teamID
                        row[1],  # teamName
                        row[2],  # teamAbbr
                        int(row[3]),  # seasonYear
                        int(row[4]),  # divisionNum
                        int(row[5]),  # winCount
                        int(row[6]),  # lossCount
                        int(row[7]),  # tieCount
                        float(row[8]),  # dual_meetPoints
                        float(row[9]),  # divisional_relayPoints
                        float(row[10]),  # divisionalPoints
                        float(row[11]),  # all_star_relayPoints
                        float(row[12]),  # all_star_Points
                        float(row[13]),  # totalPoints
                        float(row[14]),  # grand_totalPoints
                        float(row[15])   # powerRanking
                    ]
                    cursor.execute(insert_query, row_data)

            # Commit changes to the database
            connection.commit()
            print("Data inserted successfully into the teams table.")

    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()  # Rollback in case of error

    finally:
        connection.close()

if __name__ == "__main__":
    # Path to the CSV file
    csv_file_path = 'data\NVSL_DB_Teams.csv'
    
    # Ensure environment variables are set before running
    if not all([db_host, db_user, db_password, db_name]):
        print("Please set DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME environment variables.")
    else:
        insert_data_to_teams_table(csv_file_path)
