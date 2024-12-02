import os
import requests
from bs4 import BeautifulSoup
import csv

# File paths for CSV output
EVENT_RESULTS_FILE = "AllStars_EventResults.csv"

def scrape_all_stars_page(html_file):
    """
    Scrapes an All-Stars HTML page and extracts event results.
    """
    with open(html_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Data container
    event_results = []

    # Extract event results
    event_tables = soup.find_all("table")
    for table in event_tables:
        if table.find("th"):
            event_name = table.find("th").text.strip()
            for row in table.find_all("tr", {"class": ["odd", "even"]}):
                cells = row.find_all("td")
                if len(cells) >= 4:  # Ensure the row has the expected number of columns
                    event_results.append({
                        "Event": event_name,
                        "Place": cells[0].text.strip(),
                        "Time": cells[1].text.strip(),
                        "Team": cells[2].text.strip(),
                        "Swimmers": cells[3].text.strip().replace("\n", ", ")
                    })

    return event_results

def save_to_csv(data, filename, headers):
    """
    Saves the given data to a CSV file with the specified headers.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def main():
    # Path to the local HTML file
    all_stars_html_file = "All-Stars.html"

    # Scrape the page
    event_results = scrape_all_stars_page(all_stars_html_file)

    # Save results to CSV
    save_to_csv(event_results, EVENT_RESULTS_FILE, ["Event", "Place", "Time", "Team", "Swimmers"])

    print(f"Data successfully scraped and saved to {EVENT_RESULTS_FILE}")

if __name__ == "__main__":
    main()
