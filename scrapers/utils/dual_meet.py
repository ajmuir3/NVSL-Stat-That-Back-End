#

import requests
from bs4 import BeautifulSoup
from utils.scoring import dual_meet_points
import numpy as np

def sort_dict(dict):
    keys = list(dict.keys())
    values = list(dict.values())
    sorted_value_index = np.argsort(values)
    sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
    return sorted_dict

#https://www.mynvsl.com/results/26171?back=dt

# Send a GET request to the URL

url = f'https://www.mynvsl.com/results/25152?back=dt' # 2021 D12

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
tables = soup.find_all('table')

i = 1

stroke_map = {}
team_map = {}
swimmer_map = {}

for table in tables[1:]:

    rows = table.find_all('tr')
    if rows:
        header = rows[0].find('th').get_text(strip=True)
        print(header)
        if "Relay" in header:
            for row in rows[1:2]:
                cells = row.find_all('td')
                if len(cells) <= 4:
                    #get points
                    place = cells[0].get_text(strip=True).split('.')[0]
                    points = dual_meet_points(place=place)

                    #track points by team
                    if(team_abbr not in team_map):
                        team_map[team_abbr] = 0
                        team_map[team_abbr] += points
                    else:
                        team_map[team_abbr] += points
                    
        else:
            for row in rows[1:4]:
                cells = row.find_all('td')
                if len(cells) <= 4:

                    #get points
                    place = cells[0].get_text(strip=True).split('.')[0]
                    points = dual_meet_points(place=place)

                    #get team
                    team_abbr = cells[2].get_text(strip=True)

                    #track points by Swimmer
                    name = cells[3].get_text(strip=True)

                    #track points by swimmer
                    if(name not in swimmer_map):
                        swimmer_map[name] = 0
                        swimmer_map[name] += points
                    else:
                        swimmer_map[name] += points

                    print(f'{name}({team_abbr}): {swimmer_map[name]}')

                    #track points by team
                    if(team_abbr not in team_map):
                        team_map[team_abbr] = 0
                        team_map[team_abbr] += points
                    else:
                        team_map[team_abbr] += points

print(sort_dict(team_map))
print(sort_dict(swimmer_map))
    