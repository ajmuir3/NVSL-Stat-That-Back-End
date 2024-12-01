from utils.records2 import get_record
from utils.convert_time import convert_time_to_seconds
from utils.scoring import dual_meet_points,divisional_relays_points,divisional_ind_points,all_star_points

def create_swimmer(cells):
    """
    Creates a swimmer entity.
    """
    swimmer_id = f"{cells[3].get_text(strip=True)}_{cells[2].get_text(strip=True)}"
    team_id = f"{cells[2].get_text(strip=True)}"
    swimmer_name = cells[3].get_text(strip=True)
    return swimmer_id, team_id, swimmer_name

def create_result(cells, meet_event, event, meet_info):
    try:
        individual = event[-1]
        meet_type = meet_info[-2]
        # Extract and sanitize place
        raw_place = cells[0].get_text(strip=True).split('.')[0].strip()
        if not raw_place.isdigit():
            raise ValueError(f"Invalid place value: '{raw_place}'")
        place = raw_place

        # Extract and validate time
        raw_time = cells[1].get_text(strip=True)
        if not raw_time:
            raise ValueError(f"Missing time data in cells: {cells}")
        time = round(convert_time_to_seconds(raw_time),2)
        
        # Determine points based on meet type
        if meet_type == "Dual":
            points = dual_meet_points(place, individual)
        elif meet_type == "Divisional Relay":
            points = divisional_relays_points(place)
        elif meet_type == "Divisionals":
            points = divisional_ind_points(place)
        elif meet_type == "All Star Relay Carnival":
            points = divisional_relays_points(place)  # Same as Divisional Relay
        elif meet_type == "All Stars":
            points = all_star_points(place)
        else:
            points = 0  # Default points if meet type is unknown

        # Calculate power index
        record_time = get_record(event)
        if not record_time:
            record_time = 0
        power_index = round(1000 * (record_time / time) ** 3, 2)

        # Generate result ID
        result_id = f"{meet_event[0]}_{place}"
        result = [result_id,meet_event[0],time,place,points,power_index]
        return result

    except KeyError as e:
        print(f"KeyError in create_result for place '{place}' with meet type '{meet_type}': {e}")
    except ValueError as e:
        print(f"ValueError in create_result: {e}")
    except Exception as e:
        print(f"Unexpected error in create_result: {e}")
    return None