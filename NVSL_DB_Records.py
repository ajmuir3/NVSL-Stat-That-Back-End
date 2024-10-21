#url: https://www.mynvsl.com/records

import requests
import re
from bs4 import BeautifulSoup
from utils.convert_time import convert_time_to_seconds

def records(url, dict):

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    #Find all headers on the page
    
    # Find all tables on the page
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        if rows:
            for row in rows:
                try:
                    cells = row.find_all('td')
                    event = cells[0].get_text(strip=True)
                    if 'relay-carnival' in url:
                        event = event + " relay-carnival"
                    time = cells[1].get_text(strip=True)
                    dict[event] = round(convert_time_to_seconds(time),2)
                except ValueError as e:
                    print()
    return dict

urls = ['https://www.mynvsl.com/records','https://www.mynvsl.com/records/saturday-meets-yards','https://www.mynvsl.com/records/relay-carnival']
record_book = {}
for url in urls:
    records(url,record_book)

print(record_book)
