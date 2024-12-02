import requests
from bs4 import BeautifulSoup
from utils.abbr import return_abbr
from utils.all_stars import return_score as all_star
from utils.divisonals import return_score as divisional

file = open("NVSL_DB_Teams_2021.csv", "a")

# Specify the year
year = 2021

# URL of the webpage you want to scrape
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
        header = rows[0].find('th').get_text(strip=True)

        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) == 8:  # Adjusted to match the new row structure
                team_name = cells[0].find('a').get_text(strip=True)  # Extract team name from the <a> tag
                team_abbr = return_abbr(team_name)
                division = int(header.split(" ")[1])
                meets_won = int(cells[1].get_text(strip=True))
                meets_lost = int(cells[2].get_text(strip=True))
                meets_tied = int(cells[3].get_text(strip=True))
                dual_meet_points = float(cells[4].get_text(strip=True))
                division_relays_points = float(cells[5].get_text(strip=True))
                all_star_relays_points = float(cells[6].get_text(strip=True))
                total_points = float(cells[7].get_text(strip=True))

                team_id = team_abbr + str(year)

                all_star_points = all_star(team_abbr, year)

                divisional_points = divisional(team_abbr, year, division)

                grand_total_points = total_points + all_star_points + divisional_points

                power_rankings = (division / (total_points / 3376)) + meets_lost
                power_rankings = round(power_rankings, 2)

                print(f"{team_id},{team_name},{team_abbr},{year},{division},{meets_won},{meets_lost},{meets_tied},{dual_meet_points},{division_relays_points},{divisional_points},{all_star_relays_points},{all_star_points},{total_points},{grand_total_points},{power_rankings}\n")

                file.write(f"{team_id},{team_name},{team_abbr},{year},{division},{meets_won},{meets_lost},{meets_tied},{dual_meet_points},{division_relays_points},{divisional_points},{all_star_relays_points},{all_star_points},{total_points},{grand_total_points},{power_rankings}\n")

file.close()
