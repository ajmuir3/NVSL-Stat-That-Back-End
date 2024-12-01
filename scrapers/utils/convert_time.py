import re

def convert_time_to_seconds(time):
    if ":" in time:
        split = re.split('[:]',time)
        seconds = (float(split[0])*60.0) + float(split[1])
        return seconds
    else:
        return float(time)