import http
import requests
from bs4 import BeautifulSoup
from utils.score_parser import split_swim_meet_result
from utils.convert_date import convert_date_format
from NVSL_DB_Results import meet_results
from utils.file_writer import write_meet_data

error = False
count = 1

meets = "NVSL_DB_Meets.csv"
events = "NVSL_DB_Events.csv","a"
results = "NVSL_DB_Results.csv","a"
swimmers = "NVSL_DB_Swimmers.csv","a"
files = [meets,events,results,swimmers]

for i in range(2021,2025):
    for j in range(2,18):
        url = f'https://www.mynvsl.com/schedules?year={i}&div={j}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                try:
                    a = 0
                    cells = row.find_all('a',href=True)
                    away_team = cells[0].get_text(strip=True)
                    home_team = cells[1].get_text(strip=True)
                    results = cells[3]['href']
                    data = meet_results(f'https://www.mynvsl.com{results}',home_team,away_team,j)
                    for file in files:
                        with open(str(file), 'a') as file:
                            if a == 3:
                                for each in data[a]:
                                    formatted_data = ','.join([str(item) for item in each])
                                    file.write(formatted_data + '\n')
                            else: 
                                for each in data[a]:
                                    break
                        a += 1
                
                except IndexError as e:
                    try:
                        results = cells[2]['href']
                        data = meet_results(f'https://www.mynvsl.com{results}',"Divisional Relay Carnival",f"Division {j}",j)
                        print(data)

                    except IndexError as e:
                        print(f"{e}:{cells}")
                '''
                except TypeError as t:
                    error = True
                except KeyError as k:
                    error = True
                '''
                    


           
     
