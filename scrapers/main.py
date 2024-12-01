from meet_scraper import scrape_meets
from utils.file_write import write_csv_headers

if __name__ == "__main__":
    write_csv_headers()
    for year in range(2021, 2022):
        for division in range(1, 18):
            scrape_meets(year, division)