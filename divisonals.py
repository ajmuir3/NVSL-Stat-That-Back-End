import requests
from bs4 import BeautifulSoup
from utils.scoring import divisional_ind_points
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
                points = divisional_ind_points(place=place)

                #get team
                team_abbr = cells[2].get_text(strip=True)

                #track points by team
                if(team_abbr not in team_map):
                    team_map[team_abbr] = 0
                    team_map[team_abbr] += points
                else:
                    team_map[team_abbr] += points

    return sort_dict(team_map)

def return_score(team_abbr, year, division):
    
    url = 0

    if(year == 2022):
        urls = {1: 26312,
                2: 26329,
                3: 26346,
                4: 26363,
                5: 26380,
                6: 26582,
                7: 26397,
                8: 26414,
                9: 26431,
                10: 26584,
                11: 26464,
                12: 26481,
                13: 26489,
                14: 26515,
                15: 26532,
                16: 26549,
                17: 26566}
        
        url = urls[division]

    else:
        urls = {2024: 27402,
            2023: 26982,
            2021: 26154}
    
        url = urls[year]
        
        division = division - 1
        url = url + division 

    scores = score_meet(f'https://www.mynvsl.com/results/{url}?back=dv')
    return scores[team_abbr]

print(return_score("WG", 2024, 10))