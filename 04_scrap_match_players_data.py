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
# Match player stat directory
match_map_players_datasets_dir = os.getenv('VCT_MATCH_MAP_PLAYERS_DATASETS_DIRECTORY')
match_map_players_datasets_dir = f"{output_dir}/{match_map_players_datasets_dir}"
Path(match_map_players_datasets_dir).mkdir(parents=True, exist_ok=True)

matches_url_dir = os.getenv('VCT_MATCHES_URLS_DIRECTORY')

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
    overwrite_dialogs[year] = input(f"Scrap vct-{year} player stats ? [y/n][y by default] (Note: it will overwrite existing data): ") or "y"

# Scrapping starting time
starting_time = time.time()

# Looping thru vct year (2021 to Current year)
for year in year_range:
    # Reading vct matches url file
    matches_url_filename = f"{matches_url_dir}/vct-{year}-matches.txt"
    
    if os.path.isfile(matches_url_filename):
        with open(matches_url_filename, "r", encoding='utf-8') as matches_url_file:
            match_urls = matches_url_file.readlines()
            match_players_data_ilename = f"{match_map_players_datasets_dir}/vct-{year}-players-data.csv"
            
            # Check if overwriting a year datasets else skip
            if overwrite_dialogs[year].lower() != 'n':
                if os.path.isfile(match_players_data_ilename):
                    os.remove(match_players_data_ilename)
                
                # Writing vct match player stat file
                with open(match_players_data_ilename, "a", newline='', encoding='utf-8') as player_data_file:
                    for match_url in match_urls:
                        # Scraping data from each urls
                        match_url = f"{vlrgg_base_url}{match_url.replace('\n', '')}"
                        print("[INFO]", f"Scraping match players data from {match_url}")
                        player_data = sc.scrap_match_player_data(match_url)
                        print("[INFO]", f"Writing match players data into {match_players_data_ilename}")
                        if player_data:
                            for p in player_data:
                                csvwriter = csv.writer(player_data_file)
                                csvwriter.writerow(p.__dict__.values())
                        
                        print("")
                        
                player_data_file.close()
        matches_url_file.close()
    else:
        print(f"URLs file {matches_url_filename} does not exist. Try running 01_scrap_matches_url.py")

# Scrapping ending time
ending_time = time.time()
print("[INFO]", f"Scrapping executed in {ending_time - starting_time} seconds")

