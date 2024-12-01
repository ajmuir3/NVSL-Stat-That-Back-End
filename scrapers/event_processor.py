
from utils.file_write import write_csv
from utils.map_event2 import return_division_allstar_relays, return_dual_divisional_allstar_events

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

def create_event(header,meet_info): 
    event_id = header
    if "Relay" in str(header) and meet_info[4] == "Champs":
        event_number = return_division_allstar_relays(header)
        individual = False
    else:
        event_number = return_dual_divisional_allstar_events(header)
        if "Relay" in str(header):
            individual = False
        else:
            individual= True
    gender, age_group, distance, course, stroke = parse_event_header(header) 
    return [event_id, event_number, gender, age_group, distance, course, stroke, individual]

def create_meet_event(event, meet):
    meet_event_id = f'{event}@{meet}'
    meet_event= [meet_event_id, event, meet]
    return meet_event