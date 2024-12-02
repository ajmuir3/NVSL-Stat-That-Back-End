import requests
from bs4 import BeautifulSoup
from file_write import write_csv
from D_Scraper import scrape_divisionals_page
from AR_Scraper import scrape_all_star_relay_page
from A_Scraper import scrape_all_stars_page
from DR_Scraper import scrape_divisional_relay_page
from NVSL_DB_Results import meet_results

# File paths
MEETS_FILE = "Meets.csv"
EVENTS_FILE = "Events.csv"
RESULTS_FILE = "Results.csv"
SWIMMERS_FILE = "Swimmers.csv"

# List of meet types for special handling
MEET_TYPES = ["Divisional Relay", "All Star Relay Carnival", "Divisional", "All Stars"]

def identify_meet_type(row_text):
    """
    Identify the meet type based on the text in the row.
    """
    for meet_type in MEET_TYPES:
        if meet_type in row_text:
            return meet_type
    return "Dual Meet"

def scrape_schedule(year=2022):
    """
    Scrape the schedule for the given year and handle meet-specific scraping.
    """
    meets, events, results, swimmers = [], [], [], []

    for div in range(1, 18):  # Divisions 2-17
        url = f'https://www.mynvsl.com/schedules?year={year}&div={div}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')

        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                try:
                    row_text = row.get_text(strip=True)
                    cells = row.find_all('a', href=True)

                    if not cells:
                        continue

                    # Identify meet type
                    meet_type = identify_meet_type(row_text)

                    # Handle different meet types
                    if meet_type == "Dual Meet":
                        away_team = cells[0].get_text(strip=True)
                        home_team = cells[1].get_text(strip=True)
                        results_url = cells[3]['href']
                        meet_info = meet_results(f'https://www.mynvsl.com{results_url}', home_team, away_team, div)

                    elif meet_type == "Divisional Relay":
                        results_url = cells[-1]['href']
                        meet_info = scrape_divisional_relay_page(f'https://www.mynvsl.com{results_url}')

                    elif meet_type == "All Star Relay Carnival":
                        results_url = cells[-1]['href']
                        meet_info = scrape_all_star_relay_page(f'https://www.mynvsl.com{results_url}')

                    elif meet_type == "Divisional":
                        results_url = cells[-1]['href']
                        meet_info = scrape_divisionals_page(f'https://www.mynvsl.com{results_url}')

                    elif meet_type == "All Stars":
                        results_url = cells[-1]['href']
                        meet_info = scrape_all_stars_page(f'https://www.mynvsl.com{results_url}')

                    else:
                        print(f"Unknown meet type: {meet_type}")
                        continue

                    # Append meet data
                    meets.append(meet_info[0])
                    events.extend(meet_info[1])
                    results.extend(meet_info[2])
                    swimmers.extend(meet_info[3])

                except Exception as e:
                    print(f"Error processing row: {e}")

    return meets, events, results, swimmers

def main():
    # Scrape schedule and results
    year = 2021  # Replace with the desired year
    meets, events, results, swimmers = scrape_schedule(year)

    # Write to CSV files
    write_csv(MEETS_FILE, meets)
    write_csv(EVENTS_FILE, events)
    write_csv(RESULTS_FILE, results)
    write_csv(SWIMMERS_FILE, swimmers)
    print("Data scraping completed and files written!")

if __name__ == "__main__":
    main()
