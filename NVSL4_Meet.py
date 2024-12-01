import re
import requests
from bs4 import BeautifulSoup
from utils.convert_date import convert_date_format
from utils.map_event2 import return_division_allstar_relays, return_dual_divisional_allstar_events
from utils.records2 import get_record
from utils.score_parser import split_swim_meet_result
from utils.abbr import return_abbr
import utils.scoring as score
from utils.convert_time import convert_time_to_seconds

# File paths for CSV outputs
csv_files = {
    "meet": "./data/Meet.csv",
    "dual_meet": "./data/DualMeet.csv",
    "champs_meet": "./data/ChampsMeet.csv",
    "event": "./data/Event.csv",
    "meet_event": "./data/MeetEvent.csv",
    "result": "./data/Result.csv",
    "swimmer": "./data/Swimmer.csv",
    "meet_participant": "./data/MeetParticipant.csv"
}

# Initialize the CSV files with headers
headers = {
    "meet": "meetID,year,date,course,title,meet_type\n",
    "dual_meet": "dualMeetID,meetID,homeTeamID,awayTeamID,homeTeamPoints,awayTeamPoints\n",
    "champs_meet": "champsMeetID,meetID,meet_type\n",
    "event": "eventID,number,gender,ageGroup,distance,stroke,individual\n",
    "meet_event": "meetEventID,meetID,eventID\n",
    "result": "resultID,meetEventID,swimmerID,time,place,points,powerIndex\n",
    "swimmer": "swimmerID,teamID,name\n",
    "meet_participant": "participantID,meetID,teamID\n"
}

for key, file_path in csv_files.items():
    with open(file_path, "w") as file:
        file.write(headers[key])

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

                # Determine meet type
                if "Divisional Relays" in title:
                    meet_type_champs = "Divisional Relay"
                elif "Divisionals" in title:
                    meet_type_champs = "Divisionals"
                elif "All Star Relay Carnival" in title:
                    meet_type_champs = "All Star Relay Carnival"
                elif "All Stars" in title:
                    meet_type_champs = "All Stars"
                else:
                    meet_type = "Dual"
                    title = f"{cells[0].get_text(strip=True)} at {cells[2].get_text(strip=True)}"

                print(title)
                scrape_meet_details(f"https://www.mynvsl.com{result_link}", title, meet_type, year, division, meet_type_champs)

            except Exception as e:
                print(f"Error processing row {row_index + 1} in table {table_index + 1}: {e}")

def scrape_meet_details(url, title, meet_type, year, division, meet_type_champs):
    """
    Scrapes details for a specific meet, based on its type.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Metadata extraction
        meet_id = f"{title.replace(' ', '_')}_{year}"
        meta_data = soup.find("table", {"class": "simple"})

        # Initialize variables for Date and Course
        date = "Date not found"
        course = "Course not found"
        scores = [] if meet_type == "Dual" else None  # Only needed for dual meets

        if meta_data:
            rows = meta_data.find_all('tr')  # Find all rows in the table
            for row in rows:
                header = row.find('th')
                value = row.find('td')

                if header and value:  # Check both <th> and <td> exist
                    header_text = header.get_text(strip=True)
                    value_text = value.get_text(strip=True)

                    # Check for Date and Course
                    if "Date:" in header_text:
                        date = value_text
                    elif "Course:" in header_text:
                        course = value_text
                    elif "Scores" in header_text and meet_type == "Dual":
                        scores_table = value.find("table", {"class": "simple"})
                        if scores_table:
                            for score_row in scores_table.find_all('tr'):
                                for cell in score_row.find_all(['th', 'td']):
                                    score_text = cell.get_text(strip=True)
                                    if score_text:
                                        scores.append(score_text)

        # Output results
        meet_info = [meet_id, year, convert_date_format(date), course, title, meet_type]
        write_to_csv("meet", meet_info)

        if meet_type == "Dual":
            process_dual_meet(title, year, scores, meet_info)
        else:
            process_champs_meet(meet_info, meet_type_champs)

        scrape_events_and_results(soup, url, meet_info, meet_type)

    except Exception as e:
        print(f"Error processing meet details for {url}: {e}")

def process_dual_meet(title, year, scores, meet_info):
    """
    Processes and stores dual meet data.
    """
    try:
        home_team = re.sub(r'\s*\(.*?\)|\d+', '', title.split(" at ")[1])
        away_team = re.sub(r'\s*\(.*?\)|\d+', '', title.split(" at ")[0])
        home_team_id = f"{return_abbr(home_team)}{year}"
        away_team_id = f"{return_abbr(away_team)}{year}"
        if scores[1] == home_team:
            home_points = float(scores[0])
            away_points = float(scores[2])
        else:
            away_points = float(scores[0])
            home_points = float(scores[2])

        dual_meet_id = f"{home_team_id}_vs_{away_team_id}_{year}"
        dual_meet_info = [dual_meet_id, meet_info[0], home_team_id, away_team_id, home_points, away_points]
        write_to_csv("dual_meet", dual_meet_info)
    except Exception as e:
        print(f"Error processing dual meet: {e}")

def process_champs_meet(meet_info, meet_type_champs):
    """
    Processes and stores champs meet data.
    """
    try:
        champs_meet_id = f"{meet_info[0]}_Champs"
        champs_meet_info = [champs_meet_id, meet_info[0], meet_type_champs]
        write_to_csv("champs_meet", champs_meet_info)
    except Exception as e:
        print(f"Error processing champs meet: {e}")

def scrape_events_and_results(soup, url, meet_info, meet_type):
    """
    Extracts and writes data for events, results, swimmers, and participants.
    """
    try:
        tables = soup.find_all("table")[2:]  # Skip metadata tables
        for table_index, table in enumerate(tables):
            rows = table.find_all("tr")
            if not rows:
                continue

            header = rows[0].find("th").get_text(strip=True)
            event_id = f"{map_event(header)}_{meet_info[0]}"
            event = create_event(header, meet_info)
            write_to_csv("event", event)

            meet_event_id = f"{meet_info[0]}_{event_id}"
            meet_event = [meet_event_id, meet_info[0], event_id]
            write_to_csv("meet_event", meet_event)

            for row_index, row in enumerate(rows[1:]):
                try:
                    cells = row.find_all("td")
                    if len(cells) < 4:
                        continue

                    result = create_result(cells, meet_event, header, event,meet_info[-1])
                    write_to_csv("result", result)

                    swimmer = create_swimmer(cells, meet_info)
                    write_to_csv("swimmer", swimmer)

                    participant = create_participant(meet_info, swimmer)
                    write_to_csv("meet_participant", participant)
                except Exception as e:
                    print(f"Error processing result row {row_index + 1} in table {table_index + 1}: {e}")
    except Exception as e:
        print(f"Error scraping events and results for {meet_info[0]}: {e}")

def parse_event_header(header):
    mixed_age = False
    if "Mixed Age" in header:
        mixed_age = True

    event_info = header.split(" ")

    gender = event_info[0]
    distance = int(event_info[2][:-1])
    course = event_info[2][-1:]
    stroke = event_info[1]
    
    if mixed_age != True:
        age_group = event_info[-1]
    else:
        age_group = "Mixed Age"
    
    return gender, age_group, distance, stroke, course
def create_event(header, meet_info):
    """
    Creates an event entity.
    """
    
    event_id = header
    if "Relay" in str(header) and meet_info[2] == "Champs":
        event_number = return_division_allstar_relays(header)
        individual = False
    else:
        event_number = return_dual_divisional_allstar_events(header)
        individual = True
    gender, age_group, distance, course, stroke = parse_event_header(header) 
    return event_id, event_number, gender, age_group, distance, course, stroke, individual

def create_result(cells, meet_event, header, event, meet_type):
    try:
        individual = event[-1]

        # Extract and sanitize place
        raw_place = cells[0].get_text(strip=True).split('.')[0].strip()
        if not raw_place.isdigit():
            raise ValueError(f"Invalid place value: '{raw_place}'")
        place = int(raw_place)

        # Extract and validate time
        raw_time = cells[1].get_text(strip=True)
        if not raw_time:
            raise ValueError(f"Missing time data in cells: {cells}")
        time = convert_time_to_seconds(raw_time)
        # Determine points based on meet type
        if meet_type == "Dual":
            points = score.dual_meet_points(place=str(place), individual=individual)
        elif meet_type == "Divisional Relay":
            points = score.divisional_relays_points(place=place)
        elif meet_type == "Divisionals":
            points = score.divisional_ind_points(place=place)
        elif meet_type == "All Star Relay Carnival":
            points = score.divisional_relays_points(place=place)  # Same as Divisional Relay
        elif meet_type == "All Stars":
            points = score.all_star_points(place=place)
        else:
            points = 0  # Default points if meet type is unknown

        # Calculate power index
        record_time = get_record(event)
        if not record_time:
            record_time = 0
        power_index = round(1000 * (record_time / time) ** 3, 2)

        # Generate result ID
        result_id = f"{meet_event[0]}_{place}"
        return result_id, meet_event[0], time, place, points, power_index

    except KeyError as e:
        print(f"KeyError in create_result for place '{place}' with meet type '{meet_type}': {e}")
    except ValueError as e:
        print(f"ValueError in create_result: {e}")
    except Exception as e:
        print(f"Unexpected error in create_result: {e}")
    return None


def create_swimmer(cells, meet_info):
    """
    Creates a swimmer entity.
    """
    swimmer_id = f"{cells[3].get_text(strip=True)}_{cells[2].get_text(strip=True)}"
    team_id = f"{cells[2].get_text(strip=True)}{meet_info[1]}"
    swimmer_name = cells[3].get_text(strip=True)
    return swimmer_id, team_id, swimmer_name

def create_participant(meet_info,swimmer):
    """
    Creates a meet participant entity.
    """
    participant_id = f"{swimmer[0]}_{meet_info[0]}"
    return participant_id, meet_info[0], swimmer[1]

def write_to_csv(entity, data):
    """
    Writes data to a specified CSV file.
    """
    with open(csv_files[entity], "a") as file:
        file.write(",".join(map(str, data)) + "\n")

if __name__ == "__main__":
    for year in range(2021, 2022):
        for division in range(1, 18):
            scrape_meets(year, division)
 