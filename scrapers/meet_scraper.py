import requests
from bs4 import BeautifulSoup
from details_scraper import scrape_meet_details

def scrape_meets(year, division):
    """
    Scrapes meet schedules and results for a given year and division.
    """
    url = f"https://www.mynvsl.com/schedules?year={year}&div={division}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    for table_index, table in enumerate(tables):
        rows = table.find_all("tr")
        for row_index, row in enumerate(rows):
            try:
                cells = row.find_all("td")
                if len(cells) < 5:
                    continue

                result_link = cells[-1].find("a")["href"]
                title = f"{cells[0].get_text(strip=True)}"
                meet_type = "Champs"
                meet_type_champs = ""

                if "Divisional Relays" in title:
                    meet_type_champs = "Divisional Relays"
                elif "Divisionals" in title:
                    meet_type_champs = "Divisionals"
                elif "All Star Relay Carnival" in title:
                    meet_type_champs = "All Star Relay Carnival"
                elif "All Stars" in title:
                    meet_type_champs = "All Stars"
                else:
                    meet_type = "Dual"
                    title = f"{cells[0].get_text(strip=True)} at {cells[2].get_text(strip=True)}"

                if "team" not in f"https://www.mynvsl.com{result_link}":
                    print(f"url: https://www.mynvsl.com{result_link} title: {title}, meet type: {meet_type}, year: {year}, division: {division}, meet_type_chmaps:{meet_type_champs}")
                    scrape_meet_details(f"https://www.mynvsl.com{result_link}", title, meet_type, year, division, meet_type_champs)

            except Exception as e:
                print(f"Error processing row {row_index + 1} in table {table_index + 1}: {e}")