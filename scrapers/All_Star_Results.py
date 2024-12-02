import requests
from bs4 import BeautifulSoup
from utils.score_parser import split_swim_meet_result
from utils.convert_date import convert_date_format
from utils.abbr import return_abbr
from utils.event_list import map_event
from utils.scoring import dual_meet_points
from utils.records import retrive_record
from utils.convert_time import convert_time_to_seconds

def meet_data(meet_info,home_team,away_team,div):
    #Meet Metadata
    year = int(meet_info[0][-4:])
    title = f"{away_team} at {home_team} ({year})"
    date = convert_date_format(meet_info[0])
    location = meet_info[1]
    course = meet_info[2][3:]

    #Home vs Away Team
    home_abbr = return_abbr(home_team)
    away_abbr = return_abbr(away_team)
    home_team_id = f"{home_abbr}{meet_info[0][-4:]}"
    away_team_away = f"{away_abbr}{meet_info[0][-4:]}"

    #Primary Key of Meet Record
    meet_id = f"{away_abbr}@{home_abbr}{year}"

    return meet_id,home_team_id,away_team_away,title,year,date,location,div,course

def event_data(header,meet):
    
    event_info = header.split(" ")
    event_id = f'{meet[0]}{map_event(header)}'
    event_number = map_event(header)
    gender = event_info[0]
    age_group = event_info[-1]
    distance = int(event_info[2][:-1])
    course = meet[-1]
    stroke = event_info[1]
    individual = True
    if "Relay" in header:
        individual = False

    return event_id,meet[0],event_number,gender,age_group,distance,course,stroke,individual

def result_data(cells,event,meet,header):

    result_id = f'{event[0]}{cells[0].get_text(strip=True)[:-1]}'
    swimmer_id = f'{cells[3].get_text(strip=True)}{cells[2].get_text(strip=True)}{meet[-5]}'
    
    #Result Scoring
    place = cells[0].get_text(strip=True).split('.')[0]
    points = dual_meet_points(place=place,event=event)

    place = int(place)
    points = float(points)

    #Performance Statistics
    time = convert_time_to_seconds(cells[1].get_text(strip=True))
    power_index = round(1000 * pow((retrive_record(header)/time),3),2)
    return result_id,event[0],swimmer_id,time,place,points,power_index

def swimmer_data(cells,meet):

    swimmer_id = f'{cells[3].get_text(strip=True)}{cells[2].get_text(strip=True)}{meet[-5]}'
    team_id = f'{cells[2].get_text(strip = True)}{meet[-5]}'
    swimmer_name = cells[3].get_text(strip=True)
    
    return swimmer_id,team_id,swimmer_name

def meet_results(url,home_team, away_team,div):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables on the page
        tables = soup.find_all('table')
                
        # Find Meet Date, Location, Course, Home_Team_Points, and Away_Team_Points
        meet_info = []
        tables = soup.find_all('table')
        for table in tables[:1]:
            rows = table.find_all('tr')
            if rows:
                for row in rows:
                    cells = row.find_all('td')[0].get_text(strip=True)
                    meet_info.append(cells)

        meet = meet_data(meet_info,home_team,away_team,div)
        #print(meet)
        events = []
        results = []
        swimmers = []
    
        # Iterate through each table
        for table in tables[2:]:
        # Find all rows in the table body
            rows = table.find_all('tr')

            # Check if the table has a header row
            if rows:
                # Process the header row
                header = rows[0].find('th').get_text(strip=True)
                event = event_data(header,meet)
                events.append(event)
                #print(event)

                # Process the remainder of the rows in the table body
                for row in rows[1:]:
                    cells = row.find_all('td')
                    result = result_data(cells,event,meet,header)
                    #print(result)
                    results.append(result)
                    swimmer = swimmer_data(cells,meet)
                    if swimmer not in swimmers:
                        swimmers.append(swimmer)
                        #print(swimmer)

        info = [meet,events,results,swimmers]
        return info
    except ValueError as e:
        print(f'error:{url}')
                
meet_results("https://mynvsl.com/results/26586?back=dv","NVSL","NVSL",0)