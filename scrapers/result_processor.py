from event_processor import *
from swimmer_processor import create_result, create_swimmer
from utils.map_event2 import return_division_allstar_relays, return_dual_divisional_allstar_events
from utils.file_write import write_csv

def scrape_events_and_results(soup, url, meet_info, meet_type):
    try:
        tables = soup.find_all("table")[2:]
        for table_index, table in enumerate(tables):
            rows = table.find_all("tr")
            if not rows:
                continue

            header = rows[0].find("th").get_text(strip=True)

            event = create_event(header, meet_info)
            write_csv("event", event)
            meet_event = create_meet_event(event[0],meet_info[0])
            write_csv("meet_event", meet_event)
            
            for row_index, row in enumerate(rows[1:]):
                try:
                    cells = row.find_all("td")
                    if len(cells) < 4:
                        continue

                    result = create_result(cells, meet_event, event,meet_info)
                    write_csv("result", result)

                    
                    swimmer = create_swimmer(cells)
                    write_csv("swimmer", swimmer)
                    
                except Exception as e:
                    print(f"Error processing result row {row_index + 1} in table {table_index + 1}: {e}")
            
    except Exception as e:
        print(f"Error processing events for {meet_info[0]}: {e}")
