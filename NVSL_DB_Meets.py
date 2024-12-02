import requests
from bs4 import BeautifulSoup
from utils.convert_date import convert_date_format

# File for CSV output
meets_csv = "NVSL_DB_Meets.csv"

# Initialize the CSV file with headers
with open(meets_csv, "w") as file:
    file.write("year,date,course,title,meet_type\n")

# Define the function to process meet data
def fetch_meet_data():
    """
    Fetches meet data from the NVSL website and writes it into a CSV file.
    Handles all meet types for all divisions and ensures complete parsing.
    """
    for year in range(2021, 2022):  # Iterate through the years
        for division in range(1, 18):  # Iterate through divisions
            url = f'https://www.mynvsl.com/schedules?year={year}&div={division}'
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to fetch {url}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')

            for table in tables:
                rows = table.find_all('tr')

                for row in rows:
                    try:
                        # Extract date
                        date_header = row.find_previous("h6")
                        date_text = date_header.get_text(strip=True) if date_header else None
                        date = convert_date_format(date_text) if date_text else None

                        # Extract meet details
                        cells = row.find_all('a', href=True)
                        if len(cells) < 3:
                            continue  # Skip rows without valid data

                        # Identify meet type and title
                        if "Divisional Relays" in row.get_text():
                            title = "Divisional Relays"
                            meet_type = "Champs"
                        elif "Divisionals" in row.get_text():
                            title = "Divisionals"
                            meet_type = "Champs"
                        elif "All Star Relay Carnival" in row.get_text():
                            title = "All Star Relay Carnival"
                            meet_type = "Champs"
                        elif "All Stars" in row.get_text():
                            title = "All Stars"
                            meet_type = "Champs"
                        else:
                            away_team = cells[0].get_text(strip=True)
                            home_team = cells[1].get_text(strip=True)
                            title = f"{home_team} vs {away_team}"
                            meet_type = "Dual"

                        # Write to CSV
                        with open(meets_csv, "a") as file:
                            meet = f"{year},{date},Meters,\"{title}\",{meet_type}\n"
                            file.write(meet)
                            print(meet)

                    except (IndexError, AttributeError, ValueError) as e:
                        print(f"Error processing row: {e}")

if __name__ == "__main__":
    fetch_meet_data()
    print(f"Meet data has been successfully written to {meets_csv}.")
