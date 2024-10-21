import re

def split_swim_meet_result(result_str):
    # Regular expression to match the pattern (score)(team name)
    pattern = re.compile(r'(\d+\.\d+)([A-Za-z\s]+)')
    matches = pattern.findall(result_str)
    
    # Creating the dictionary from the matches
    result_dict = {match[1].strip(): float(match[0]) for match in matches}
    
    return result_dict

# Example usage
result_str = "234.0Broyhill Crest131.0Springfield"
result_dict = split_swim_meet_result(result_str)
