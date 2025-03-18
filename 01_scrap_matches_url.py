import os
import time

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from src.scraper import Scraper

load_dotenv()

# Output directory
output_dir = os.getenv('OUTPUT_BASE_DIRECTORY')
Path(output_dir).mkdir(parents=True, exist_ok=True)

events_url_dir = os.getenv('VCT_EVENTS_URLS_DIRECTORY')
matches_url_dir = os.getenv('VCT_MATCHES_URLS_DIRECTORY')
Path(matches_url_dir).mkdir(parents=True, exist_ok=True)

# URLs
vlrgg_base_url = os.getenv('VLRGG_BASE_URL')

# VCT year
vct_debut_year = int(os.getenv('VCT_DEBUT_YEAR'))
vct_curr_year = datetime.now().year


sc = Scraper()

# Looping thru vct year (2021 to Current year)

# Scrapping starting time
starting_time = time.time()

for year in range(vct_debut_year, vct_curr_year + 1):
    event_urls_filename = f"{events_url_dir}/vct-{year}-events.txt"
    match_filename = f"{matches_url_dir}/vct-{year}-matches.txt"
    
    # Check if event_urls_filename exists
    if os.path.isfile(event_urls_filename):
        with open(event_urls_filename, "r") as url_file:
            event_urls = url_file.readlines()

            # Check if match_file exists
            if os.path.isfile(match_filename):
                overwrite_dialog = input(f"File {match_filename} exists. Overwrite it ? [y/n][y by default] : ") or "y"

                # Overwriting
                if overwrite_dialog.lower() == "y":
                    print("[INFO]", f"Overwriting {match_filename}")
                    os.remove(match_filename)
                    # Scrap URLs
                    with open(match_filename, "a") as dest_file:
                        for event_url in event_urls:
                            event_url = f"{vlrgg_base_url}{event_url.replace("\n", "")}"
                            
                            print("[INFO]", f"\t Scrapping matches from {event_url}")
                            matches_urls = sc.scrap_matches_url(event_url)
                            for m in matches_urls:
                                dest_file.write(f"{m}\n")
                    dest_file.close()
                # else skip this year
                else:
                    continue
            else:
                print("[INFO]", f"Creating {match_filename}")
                # Scrap URLs
                with open(match_filename, "a") as dest_file:
                    for url in event_urls:
                        url = f"{vlrgg_base_url}{url.replace("\n", "")}"
                        print("[INFO]", f"\t Scrapping matches from {url}")
                        matches_urls = sc.scrap_matches_url(url)
                        for m in matches_urls:
                            dest_file.write(f"{m}\n")
                dest_file.close()
            
        url_file.close()
        
    else:
        print(f"URLs file {event_urls_filename} does not exist. Try running 00_scrap_events_url.py")


# Scrapping ending time
ending_time = time.time()
print("[INFO]", f"Scrapping executed in {ending_time - starting_time} seconds")
