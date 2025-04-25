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
# Event data directory
events_datasets_dir = os.getenv('VCT_EVENTS_DATASETS_DIRECTORY')
events_datasets_dir = f"{output_dir}/{events_datasets_dir}"
Path(events_datasets_dir).mkdir(parents=True, exist_ok=True)
# Event urls directory
events_url_dir = os.getenv('VCT_EVENTS_URLS_DIRECTORY')

# URLs
vlrgg_base_url = os.getenv('VLRGG_BASE_URL')
vlrgg_vct_url = os.getenv('VLRGG_VCT_URL')

# VCT year
vct_debut_year = int(os.getenv('VCT_DEBUT_YEAR'))
vct_curr_year = datetime.now().year

sc = Scraper()
# current year to debut year (Recent year contains less matches)
year_range = range(vct_curr_year , vct_debut_year -1 , -1)

# Choose which year to scarp
overwrite_dialogs = {}
for year in year_range:
    print(year)
    overwrite_dialogs[year] = input(f"Scrap vct-{year} ? [y/n][y by default] (Note: it will overwrite existing data): ") or "y"

# Scrapping starting time
starting_time = time.time()

# Looping thru vct year_range
for year in year_range:

    if overwrite_dialogs[year].lower() != 'n':
        # Reading vct events url file
        event_url_filename = f"{events_url_dir}/vct-{year}-events.txt"
        # Check if event_urls_filename exists
        if os.path.isfile(event_url_filename):
            with open(event_url_filename, "r", encoding='utf-8') as event_url_file:
                event_urls = event_url_file.readlines()
                # Writing event_data_file
                event_data_filename = f"{events_datasets_dir}/vct-{year}-events-data.csv"
                with open(event_data_filename, "w", newline='', encoding='utf-8') as event_data_file:
                    for event_url in event_urls:
                        # Reading each url and creating the full url for scraping
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
        else:
            print(f"URLs file {event_url_filename} does not exist. Try running 00_scrap_events_url.py")
# Scrapping ending time
ending_time = time.time()
print("[INFO]", f"Scrapping executed in {ending_time - starting_time} seconds")

