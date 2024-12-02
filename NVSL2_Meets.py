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
    Handles both dual meets and championship meets (Divisional Relay Carnival, Divisionals, All Stars, etc.).
    """
    for year in range(2021, 2022):  # Iterate through the years
        for division in range(1, 18):  # Iterate through divisions
            url = f'https://www.mynvsl.com/schedules?year={year}&div={division}'
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to fetch {url}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            league_schedules = soup.find("div", {"id": "league_schedules"})
            if not league_schedules:
                print(f"No league schedules found for {url}")
                continue

            # Process each block of schedule
            schedule_blocks = league_schedules.find_all("table")
            for schedule_block in schedule_blocks:
                rows = schedule_block.find_all("tr")

                for row in rows:
                    try:
                        # Handle championship meets (e.g., Divisional Relays, All Stars)
                        strong_tags = row.find_all("strong")
                        if strong_tags:
                            # This indicates a championship meet
                            meet_title = strong_tags[0].get_text(strip=True)
                            if meet_title in [
                                "Divisional Relays",
                                "Divisionals",
                                "All Star Relay Carnival",
                                "All Stars",
                            ]:
                                date = row.find_previous("h6").get_text(strip=True)
                                date = convert_date_format(date)
                                course = "Meters"  # Default course
                                meet_type = "Champs"
                                with open(meets_csv, "a") as file:
                                    file.write(f"{year},{date},{course},\"{meet_title}\",{meet_type}\n")
                            continue

                        # Handle dual meets
                        cells = row.find_all("a", href=True)
                        if len(cells) < 6:
                            continue  # Skip rows without valid data

                        away_team = cells[0].get_text(strip=True)
                        home_team = cells[2].get_text(strip=True)
                        results_link = cells[-1]['href']
                        
                        date = row.find_previous("h6").get_text(strip=True)
                        date = convert_date_format(date)
                        course = "Meters"  # Default course
                        meet_title = f"{home_team} vs {away_team}"
                        meet_type = "Dual"

                        # Write to CSV
                        with open(meets_csv, "a") as file:
                            file.write(f"{year},{date},{course},\"{meet_title}\",{meet_type}\n")

                    except Exception as e:
                        print(f"Error processing row: {e}")

if __name__ == "__main__":
    fetch_meet_data()
    print(f"Meet data has been successfully written to {meets_csv}.")
