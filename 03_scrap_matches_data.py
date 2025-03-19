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

matches_datasets_dir = os.getenv('VCT_MATCHES_DATASETS_DIRECTORY')
matches_datasets_dir = f"{output_dir}/{matches_datasets_dir}"
Path(matches_datasets_dir).mkdir(parents=True, exist_ok=True)

match_map_ovw_datasets_dir = os.getenv('VCT_MATCH_MAP_OVWS_DATASETS_DIRECTORY')
match_map_ovw_datasets_dir = f"{output_dir}/{match_map_ovw_datasets_dir}"
Path(match_map_ovw_datasets_dir).mkdir(parents=True, exist_ok=True)

matches_url_dir = os.getenv('VCT_MATCHES_URLS_DIRECTORY')

# URLs
vlrgg_base_url = os.getenv('VLRGG_BASE_URL')
vlrgg_vct_url = os.getenv('VLRGG_VCT_URL')

# VCT year
vct_debut_year = int(os.getenv('VCT_DEBUT_YEAR'))
vct_curr_year = datetime.now().year

sc = Scraper()
year_range = range(vct_curr_year , vct_debut_year -1 , -1)

# Choose which year to scarp
overwrite_dialogs = {}
for year in year_range:
    print(year)
    overwrite_dialogs[year] = input(f"Scrap vct-{year} ? [y/n][y by default] (Note: it will overwrite existing data): ") or "y"

# Scrapping starting time
starting_time = time.time()

# Looping thru vct year (2021 to Current year)
for year in year_range:
    # Reading vct matches file
    matches_url_filename = f"{matches_url_dir}/vct-{year}-matches.txt"
    with open(matches_url_filename, "r", encoding='utf-8') as matches_url_file:
        match_urls = matches_url_file.readlines()
        match_data_filename = f"{matches_datasets_dir}/vct-{year}-matches-data.csv"
        if os.path.isfile(match_data_filename):
            os.remove(match_data_filename)
            
        match_map_overviews_data_filename = f"{match_map_ovw_datasets_dir}/vct-{year}-match-overviews-data.csv"
        
        if overwrite_dialogs[year].lower() != 'n':
            if os.path.isfile(match_map_overviews_data_filename):
                os.remove(match_map_overviews_data_filename)
                            
            with open(match_data_filename, "a", newline='', encoding='utf-8') as match_data_file:
                for match_url in match_urls:
                    match_url = f"{vlrgg_base_url}{match_url.replace('\n', '')}"
                    print("[INFO]", f"Scraping match data from {match_url}")
                    match_data, match_map_overviews_data = sc.scrap_match_data(match_url)
                    print("[INFO]", f"Writing match data into {match_data_filename}")
                    if match_data:
                        csvwriter = csv.writer(match_data_file)
                        csvwriter.writerow(match_data.__dict__.values())

                        if len(match_map_overviews_data) > 0:
                            with open(match_map_overviews_data_filename, "a", newline='', encoding='utf-8') as match_map_overviews_data_file:
                                
                                print("\t[INFO]", f"Writing match overviews into {match_map_overviews_data_filename}")
                                print("")
                                for m_ovws in match_map_overviews_data:
                                    csvwriter = csv.writer(match_map_overviews_data_file)
                                    csvwriter.writerow(m_ovws.__dict__.values())
                            
                            match_map_overviews_data_file.close()
                    
            match_data_file.close()
    matches_url_file.close()

# Scrapping ending time
ending_time = time.time()
print("[INFO]", f"Scrapping executed in {ending_time - starting_time} seconds")

