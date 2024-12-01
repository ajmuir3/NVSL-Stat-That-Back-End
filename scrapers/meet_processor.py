import re

from bs4 import BeautifulSoup
import requests
from utils.abbr import return_abbr
from utils.file_write import write_csv

def process_dual_meet(title, scores, meet_info):
    """
    Processes and stores dual meet data.
    """
    meet_id = meet_info[0]
    dual_meet_id = meet_id[:-4]
    try:
        if 'Sleepy Hollow B & R' in title:
            title = re.sub(r"Sleepy Hollow B & R", "Seals", title)

        pattern = r'^([A-Za-z\s\-]+?)(?:\(\d+\.\d+\))?\s+at\s+([A-Za-z\s\-]+?)(?:\(\d+\.\d+\))?$'
        match = re.match(pattern, title)
        if match:
            away_team = match.group(1).strip()
            home_team = match.group(2).strip()
            
        

        if scores[1] == home_team or scores[3] == away_team:
            home_points = float(scores[0])
            away_points = float(scores[2])

        else:
            away_points = float(scores[0])
            home_points = float(scores[2])

        dual_meet_info = [dual_meet_id, meet_info[0], return_abbr(home_team), return_abbr(away_team), home_points, away_points]
        #print(dual_meet_info)
        write_csv("dual_meet", dual_meet_info)
    except Exception as e:
        print(f"Error processing dual meet: {e}")

def process_champs_meet(meet_info, meet_type_champs):
    """
    Processes and stores champs meet data.
    """
    try:
        champs_meet_id = f"{meet_info[0]}_Champs"
        champs_meet_info = [champs_meet_id, meet_info[0], meet_type_champs]
        write_csv("champs_meet", champs_meet_info)
    except Exception as e:
        print(f"Error processing champs meet: {e}")

def process_meet_participant_dual(title, meet_info):
    """
    Creates a meet participant entity.
    """
    pattern = r'^([A-Za-z\s\-]+?)(?:\(\d+\.\d+\))?\s+at\s+([A-Za-z\s\-]+?)(?:\(\d+\.\d+\))?$'
    if 'Sleepy Hollow B & R' in title:
            title = re.sub(r"Sleepy Hollow B & R", "Seals", title)
    match = re.match(pattern, title)
    if match:
        away_team = match.group(1).strip()
        home_team = match.group(2).strip()
    teams = [home_team,away_team]
    for team in teams:
        team = return_abbr(team)
        participant_id = f"{team}@{meet_info}"
        meet_id = meet_info
        team_id = team
        meet_participant_info = [participant_id,meet_id,team_id]
        #print(meet_participant_info)
        write_csv("meet_participant", meet_participant_info)
def process_meet_participant_champs(url,meet_info):
    """
    Creates a meet participant entity.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Metadata extraction
    meta_data = soup.find("table", {"class": "simple"})

    # Initialize variables for Date and Course
    scores= []
    if meta_data:
        rows = meta_data.find_all('tr')  # Find all rows in the table
        for row in rows:
            header = row.find('th')
            value = row.find('td')

            if header and value:  # Check both <th> and <td> exist
                header_text = header.get_text(strip=True)

                # Check for Date and Course
                if "Scores" in header_text:
                    scores_table = value.find("table", {"class": "simple"})
                    if scores_table:
                        for score_row in scores_table.find_all('tr'):
                            for cell in score_row.find_all(['th', 'td']):
                                score_text = cell.get_text(strip=True)
                                if score_text:
                                    scores.append(score_text)
    for i in range(1,len(scores),2):
        team = return_abbr(scores[i])
        participant_id = f"{team}@{meet_info}"
        meet_id = meet_info
        team_id = team
        meet_participant_info = [participant_id,meet_id,team_id]
        #print(meet_participant_info)
        write_csv("meet_participant", meet_participant_info)


