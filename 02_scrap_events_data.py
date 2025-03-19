import os
import time
import csv

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from src.scraper import Scraper

load_dotenv()

# Output directory
output_dir = os.getenv('OUTPUT_BASE_DIRECTORY')
Path(output_dir).mkdir(parents=True, exist_ok=True)

events_datasets_dir = os.getenv('VCT_EVENTS_DATASETS_DIRECTORY')
events_datasets_dir = f"{output_dir}/{events_datasets_dir}"
Path(events_datasets_dir).mkdir(parents=True, exist_ok=True)

events_url_dir = os.getenv('VCT_EVENTS_URLS_DIRECTORY')

# URLs
vlrgg_base_url = os.getenv('VLRGG_BASE_URL')
vlrgg_vct_url = os.getenv('VLRGG_VCT_URL')

# VCT year
vct_debut_year = int(os.getenv('VCT_DEBUT_YEAR'))
vct_curr_year = datetime.now().year

sc = Scraper()

# Scrapping starting time
starting_time = time.time()

# Looping thru vct year (2021 to Current year)
for year in range(vct_debut_year, vct_curr_year + 1):
    # Reading vct events file
    event_url_filename = f"{events_url_dir}/vct-{year}-events.txt"
    with open(event_url_filename, "r", encoding='utf-8') as event_url_file:
        event_urls = event_url_file.readlines()
        event_data_filename = f"{events_datasets_dir}/vct-{year}-events-data.csv"
        with open(event_data_filename, "w", newline='', encoding='utf-8') as event_data_file:
            for event_url in event_urls:
                event_url = f"{vlrgg_base_url}{event_url}"
                # Scraping vct event data
                print("[INFO]", f"Scraping vct event data from {event_url.replace('\n', '')}")
                event_data = sc.scrap_event_data(event_url)
                print("[INFO]", f"\tWriting vct event data into {event_data_filename}")
                print("")
                # Writing vct event data
                if event_data:
                    csvwriter = csv.writer(event_data_file)
                    csvwriter.writerow(event_data.__dict__.values())
                
        event_data_file.close()
    event_url_file.close()

# Scrapping ending time
ending_time = time.time()
print("[INFO]", f"Scrapping executed in {ending_time - starting_time} seconds")

