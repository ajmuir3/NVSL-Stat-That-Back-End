import requests
from bs4 import BeautifulSoup
from utils.scoring import all_star_points
from utils.abbr import return_abbr
import numpy as np

def sort_dict(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    return sorted_dict

def score_meet(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    team_map = {}

    for table in tables[1:]:

        rows = table.find_all('tr')
        if rows:
            header = rows[0].find('th').get_text(strip=True)
        for row in rows[1:]:
            cells = row.find_all('td')
            if len(cells) <= 4:

                #get points
                place = cells[0].get_text(strip=True).split('.')[0]
                points = all_star_points(place=place)

                #get team
                team_abbr = cells[2].get_text(strip=True)

                #track points by team
                if(team_abbr not in team_map):
                    team_map[team_abbr] = 0
                    team_map[team_abbr] += points
                else:
                    team_map[team_abbr] += points

    return sort_dict(team_map)

def return_score(team_abbr, year):
    urls = {2021:'https://www.mynvsl.com/results/26171?back=dt', 
            2022:'https://www.mynvsl.com/results/26586?back=dt', 
            2023:'https://www.mynvsl.com/results/27000?back=dt',
            2024:'https://www.mynvsl.com/results/27419?back=dt'}
    
    scores = score_meet(urls[year])
    try:
        return scores[team_abbr]
    except:
        return 0

print(return_score(return_abbr('Commonwealth'),2021))