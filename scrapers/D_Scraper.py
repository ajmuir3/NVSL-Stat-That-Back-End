import requests
from bs4 import BeautifulSoup
import csv

# File paths for CSV output
TEAM_SCORES_FILE = "Divisionals_TeamScores.csv"
EVENT_RESULTS_FILE = "Divisionals_EventResults.csv"

def scrape_divisionals_page(url):
    """
    Scrapes a Divisionals page and extracts relevant information:
    - Team scores
    - Event results
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Data containers
    team_scores = []
    event_results = []

    # Extract team scores
    scores_section = soup.find("th", text="Scores:").find_next("table")
    for row in scores_section.find_all("tr"):
        cells = row.find_all(["th", "td"])
        for i in range(0, len(cells), 2):  # Iterate in pairs
            if i + 1 < len(cells):
                team_scores.append({
                    "Score": cells[i].text.strip(),
                    "Team": cells[i + 1].text.strip(),
                })

    # Extract event results
    event_tables = soup.find_all("table", {"class": "simple"})[1:]  # Skip the first table (team scores)
    for table in event_tables:
        event_name = table.find("th").text.strip()
        for row in table.find_all("tr", {"class": ["odd", "even"]}):
            cells = row.find_all("td")
            event_results.append({
                "Event": event_name,
                "Place": cells[0].text.strip(),
                "Time": cells[1].text.strip(),
                "Team": cells[2].text.strip(),
                "Swimmers": cells[3].text.strip().replace("\n", ", ")
            })

    return team_scores, event_results

def save_to_csv(data, filename, headers):
    """
    Saves the given data to a CSV file with the specified headers.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def main():
    # URL of the Divisionals page (replace with actual URL)
    divisionals_url = "https://mynvsl.com/results/26312?back=dv"

    # Scrape the page
    team_scores, event_results = scrape_divisionals_page(divisionals_url)

    # Save results to CSV
    save_to_csv(team_scores, TEAM_SCORES_FILE, ["Score", "Team"])
    save_to_csv(event_results, EVENT_RESULTS_FILE, ["Event", "Place", "Time", "Team", "Swimmers"])

    print(f"Data successfully scraped and saved to {TEAM_SCORES_FILE} and {EVENT_RESULTS_FILE}")

if __name__ == "__main__":
    main()
