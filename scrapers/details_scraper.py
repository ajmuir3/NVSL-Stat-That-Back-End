import re
import requests
from bs4 import BeautifulSoup
from meet_processor import process_champs_meet, process_dual_meet, process_meet_participant_champs, process_meet_participant_dual
from result_processor import scrape_events_and_results
from utils.file_write import write_csv
from utils.abbr import return_abbr
from utils.convert_date import convert_date_format

def generate_meet_id(title, meet_type, year, division, meet_type_champs):
    
    # Dual Meet ID
    if meet_type == "Dual":
        pattern = r'^([A-Za-z\s\-]+?)(?:\(\d+\.\d+\))?\s+at\s+([A-Za-z\s\-]+?)(?:\(\d+\.\d+\))?$'
        match = re.match(pattern, title)
        if match:
            away_team = match.group(1).strip()
            home_team = match.group(2).strip()
            #print(f"Away Team: {away_team}, Home Team: {home_team}")
            return f"{return_abbr(away_team)}@{return_abbr(home_team)}{year}"

    print(meet_type_champs)
    # Divisional Relays
    if "Divisional Relays" in meet_type_champs:
        return f"D{division}RC{year}"

    # Divisionals
    if "Divisionals" in meet_type_champs:
        return f"D{division}D{year}"

    # All Star Relay Carnival
    if "All Star Relay Carnival" in meet_type_champs:
        return f"ASRC{year}"

    # All Stars
    if "All Stars" in meet_type_champs:
        return f"AS{year}"

    return "UNKNOWN"

def scrape_meet_details(url, title, meet_type, year, division, meet_type_champs):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        # Metadata extraction
        meet_id = generate_meet_id(title, meet_type, year, division, meet_type_champs)
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
        meet_info = [meet_id, convert_date_format(date), course, title, meet_type, year]
        #print(f"meet_id: {meet_id} date: {convert_date_format(date)}, course: {course}, title: {title}, meet_type: {meet_type}, meet_type_champs:{meet_type_champs}")
        
        write_csv("meet", meet_info[:5])

        if meet_type == "Dual":
            process_dual_meet(title, scores, meet_info)
            process_meet_participant_dual(title, meet_info[0])
        else:
            process_champs_meet(meet_info, meet_type_champs)
            process_meet_participant_champs(url, meet_info[0])


        scrape_events_and_results(soup, url, meet_info, meet_type)

    except Exception as e:
        print(f"Error processing meet details for {url}: {e}")
