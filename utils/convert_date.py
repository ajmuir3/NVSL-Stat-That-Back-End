from datetime import datetime

def convert_date_format(date_str):
    # Parse the input date string to a datetime object
    date_obj = datetime.strptime(date_str, '%B %d, %Y')
    
    # Format the datetime object to the desired output format
    formatted_date = date_obj.strftime('%Y-%m-%d')
    
    return formatted_date