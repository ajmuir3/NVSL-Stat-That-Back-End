import requests
from bs4 import BeautifulSoup
from utils.convert_date import convert_date_format
from utils.score_parser import split_swim_meet_result
from utils.abbr import return_abbr
from utils.event_list import map_event
from utils.scoring import dual_meet_points
from utils.records import retrieve_record
from utils.convert_time import convert_time_to_seconds

# File paths for CSV outputs
csv_files = {
    "meet": "Meet.csv",
    "dual_meet": "DualMeet.csv",
    "champs_meet": "ChampsMeet.csv",
    "event": "Event.csv",
    "result": "Result.csv",
    "swimmer": "Swimmer.csv",
    "meet_participant": "MeetParticipant.csv"
}

# Initialize the CSV files with headers
headers = {
    "meet": "meetID,year,date,location,division,course,title\n",
    "dual_meet": "dualMeetID,meetID,homeTeamID,awayTeamID,homeTeamPoints,awayTeamPoints\n",
    "champs_meet": "champsMeetID,meetID\n",
    "event": "eventID,meetID,eventNumber,gender,ageGroup,distance,course,stroke,individual\n",
    "result": "resultID,eventID,swimmerID,time,place,points,powerIndex\n",
    "swimmer": "swimmerID,teamID,name\n",
    "meet_participant": "participantID,meetID,teamID\n"
}

for key, file_path in csv_files.items():
    with open(file_path, "w") as file:
        file.write(headers[key])

def scrape_meets(year, division):
    """
    so far so good
    """
    url = f"https://www.mynvsl.com/schedules?year={year}&div={division}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            try:
                cells = row.find_all("td")
                if len(cells) < 5:
                    continue

                result_link = cells[-1].find("a")["href"]
                title = f"{cells[0].get_text(strip=True)}"

                # Determine meet type
                if "Divisional Relays" in title:
                    meet_type = "Divisional Relays"
                elif "Divisionals" in title:
                    meet_type = "Divisionals"
                elif "All Star Relay Carnival" in title:
                    meet_type = "All Star Relay Carnival"
                elif "All Stars" in title:
                    meet_type = "All Stars"
                else:
                    meet_type = "Dual"
                    title = f"{cells[0].get_text(strip=True)} at {cells[2].get_text(strip=True)}"
                
                scrape_meet_details(f"https://www.mynvsl.com{result_link}", title, meet_type, year, division)

            except Exception as e:
                print(f"Error processing row: {e}")

def scrape_meet_details(url, title, meet_type, year, division):
    """
    Scrapes details for a specific meet, based on its type.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Metadata extraction
    meet_info = [year, date, course, title, meet_type]
    write_meet_data(meet_info)

    if meet_type == "Dual":
        home_team = soup.find("a", {"class": "home"}).get_text(strip=True)
        away_team = soup.find("a", {"class": "away"}).get_text(strip=True)
        home_points = 0  # Placeholder, replace with actual logic
        away_points = 0  # Placeholder, replace with actual logic

        write_dual_meet_data(meet_info, home_team, away_team, home_points, away_points)

    else:
        write_champs_meet_data(meet_info)

    # Scrape events, results, swimmers, and participants
    scrape_events_and_results(soup, meet_info)

def scrape_events_and_results(soup, meet_info):
    """
    Extracts and writes data for events, results, swimmers, and participants.
    """
    tables = soup.find_all("table")[2:]  # Skip metadata tables
    for table in tables:
        rows = table.find_all("tr")
        if not rows:
            continue

        # Process event header
        header = rows[0].find("th").get_text(strip=True)
        event = create_event(header, meet_info)
        write_to_csv("event", event)

        # Process results
        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            result = create_result(cells, event, header)
            write_to_csv("result", result)

            swimmer = create_swimmer(cells, meet_info)
            write_to_csv("swimmer", swimmer)

            participant = create_participant(swimmer, meet_info)
            write_to_csv("meet_participant", participant)

def create_event(header, meet_info):
    """
    Creates an event entity.
    """
    event_id = f"{meet_info[0]}_{map_event(header)}"
    event_number = map_event(header)
    gender, distance, stroke, age_group = parse_event_header(header)
    course = meet_info[-1]
    individual = "Relay" not in header
    return event_id, meet_info[0], event_number, gender, age_group, distance, course, stroke, individual

def create_result(cells, event, header):
    """
    Creates a result entity.
    """
    result_id = f"{event[0]}_{cells[0].get_text(strip=True)[:-1]}"
    swimmer_id = f"{cells[3].get_text(strip=True)}_{cells[2].get_text(strip=True)}"
    place = int(cells[0].get_text(strip=True).split(".")[0])
    time = convert_time_to_seconds(cells[1].get_text(strip=True))
    points = dual_meet_points(place=place, event=event)
    power_index = round(1000 * (retrieve_record(header) / time) ** 3, 2)
    return result_id, event[0], swimmer_id, time, place, points, power_index

def create_swimmer(cells, meet_info):
    """
    Creates a swimmer entity.
    """
    swimmer_id = f"{cells[3].get_text(strip=True)}_{cells[2].get_text(strip=True)}"
    team_id = f"{cells[2].get_text(strip=True)}"
    swimmer_name = cells[3].get_text(strip=True)
    return swimmer_id, team_id, swimmer_name

def create_participant(swimmer, meet_info):
    """
    Creates a meet participant entity.
    """
    participant_id = f"{swimmer[0]}_{meet_info[0]}"
    return participant_id, meet_info[0], swimmer[1]

def write_meet_data(meet_info):
    """
    Writes meet data to the CSV.
    """
    with open(csv_files["meet"], "a") as file:
        file.write(f"{meet_info[1]},{meet_info[2]},'{meet_info[0]}'\n")

def write_dual_meet_data(meet_info, home_team, away_team, home_points, away_points):
    """
    Writes dual meet data to the CSV.
    """
    with open(csv_files["dual_meet"], "a") as file:
        file.write(f"{meet_info[1]},{home_team},{away_team},{home_points},{away_points}\n")

def write_champs_meet_data(meet_info):
    """
    Writes championship meet data to the CSV.
    """
    with open(csv_files["champs_meet"], "a") as file:
        file.write(f"{meet_info[1]},{meet_info[0]}\n")

def write_to_csv(entity, data):
    """
    Writes data to a specified CSV file.
    """
    with open(csv_files[entity], "a") as file:
        file.write(",".join(map(str, data)) + "\n")

if __name__ == "__main__":
    for year in range(2021, 2025):
        for division in range(1, 18):
            scrape_meets(year, division)
