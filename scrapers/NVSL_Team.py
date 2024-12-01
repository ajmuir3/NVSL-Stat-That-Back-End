import requests
from bs4 import BeautifulSoup
from utils.abbr import return_abbr
from utils.all_stars import return_score as all_star
from utils.divisonals import return_score as divisional
from utils.location import get_team_location

# File names for output
team_csv = "./data/Team.csv"
season_csv = "./data/Season.csv"

# Initialize the CSV files with headers
with open(team_csv, "w") as team_file:
    team_file.write("teamID,teamName,location\n")

with open(season_csv, "w") as season_file:
    season_file.write(
        "seasonID,teamID,year,division,meetsWon,meetsLost,meetsTied,powerRanking,dmPoints,drPoints,dPoints,arPoints,aPoints,tPoints,gtPoints\n"
    )

# Scrape data for each year
for year in range(2021, 2022):  # Adjust the range as needed
    url = f'https://www.mynvsl.com/standings?year={year}'

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch standings for {year}. URL: {url}")
        continue

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    # Iterate through each division table
    for table_index, table in enumerate(tables):
        # Find all rows in the table body
        rows = table.find_all('tr')

        if rows:
            # Extract division number from the table header
            header = rows[0].find('th').get_text(strip=True)
            division = int(header.split(" ")[1])  # Extract division from header

            # Iterate through each team row (skip header)
            for row in rows[1:]:
                try:
                    cells = row.find_all('td')
                    if len(cells) == 8:  # Ensure row structure matches expected format
                        # Extract team details
                        team_name = cells[0].find('a').get_text(strip=True)
                        team_abbr = return_abbr(team_name)
                        meets_won = int(cells[1].get_text(strip=True))
                        meets_lost = int(cells[2].get_text(strip=True))
                        meets_tied = int(cells[3].get_text(strip=True))
                        dual_meet_points = float(cells[4].get_text(strip=True))
                        division_relays_points = float(cells[5].get_text(strip=True))
                        all_star_relays_points = float(cells[6].get_text(strip=True))
                        total_points = float(cells[7].get_text(strip=True))

                        # Compute additional metrics
                        divisional_points = divisional(team_abbr, year, division)
                        all_star_points = all_star(team_abbr, year)
                        grand_total_points = total_points + all_star_points + divisional_points
                        location = get_team_location(team_name)

                        power_ranking = round((division / (total_points / 3376)) + meets_lost, 2)

                        # Generate unique IDs
                        team_id = f"{team_abbr}"
                        season_id = f"{team_abbr}{year}"

                        # Write to Team CSV
                        with open(team_csv, "a") as team_file:
                            team_row = f"{team_id},{team_name},{location}\n"
                            team_file.write(team_row)

                        # Write to Season CSV
                        with open(season_csv, "a") as season_file:
                            season_row = (
                                f"{season_id},{team_id},{year},{division},{meets_won},{meets_lost},"
                                f"{meets_tied},{power_ranking},{dual_meet_points},{division_relays_points},"
                                f"{divisional_points},{all_star_relays_points},{all_star_points},{total_points},"
                                f"{grand_total_points}\n"
                            )
                            season_file.write(season_row)
                except Exception as e:
                    print(f"Error processing row: {e}")

print(f"Scraping completed. Data saved to {team_csv} and {season_csv}.")
