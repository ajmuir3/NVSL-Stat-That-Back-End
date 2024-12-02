import requests
from bs4 import BeautifulSoup
from utils.abbr import return_abbr
from utils.all_stars import return_score as all_star
from utils.divisonals import return_score as divisional
from utils.location import get_team_location

# Open a CSV file to write data
with open("NVSL_2021_Data.csv", "w") as file:
    # Scrape data for 2021
    year = 2021
    url = f'https://www.mynvsl.com/standings?year={year}'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables on the page
    tables = soup.find_all('table')

    # Iterate through each table
    for table_index, table in enumerate(tables):
        # Find all rows in the table body
        rows = table.find_all('tr')

        if rows:
            # Extract division number from the table header
            header = rows[0].find('th').get_text(strip=True)

            # Iterate through each team row (skip header)
            for row in rows[1:]:
                cells = row.find_all('td')
                if len(cells) == 8:  # Ensure row structure matches expected format
                    # Extract team details
                    team_name = cells[0].find('a').get_text(strip=True)
                    team_abbr = return_abbr(team_name)
                    division = int(header.split(" ")[1])  # Extract division from header
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

                    power_rankings = (division / (total_points / 3376)) + meets_lost
                    power_rankings = round(power_rankings, 2)

                    # Generate a unique team ID
                    team_id = f"{team_abbr}{year}"

                    # Print and write to CSV
                    csv_row = f"{team_id},{team_name},{team_abbr},{year},{location},{division},{meets_won},{meets_lost},{meets_tied},{power_rankings},{dual_meet_points},{division_relays_points},{divisional_points},{all_star_relays_points},{all_star_points},{total_points},{grand_total_points}\n"
                    print(csv_row)
                    file.write(csv_row)

print("Scraping completed. Data saved to NVSL_2021_Data.csv.")
