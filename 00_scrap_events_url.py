import os
from inputimeout import inputimeout, TimeoutOccurred
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from src.scraper import Scraper

load_dotenv()

# Output directory
ouput_dir = os.getenv('OUTPUT_BASE_DIRECTORY')
Path(ouput_dir).mkdir(parents=True, exist_ok=True)

events_url_dir = os.getenv('VCT_EVENTS_URLS_DIRECTORY')
Path(events_url_dir).mkdir(parents=True, exist_ok=True)

# URLs
vlrgg_vct_url = os.getenv('VLRGG_VCT_URL')

# VCT year
vct_debut_year = int(os.getenv('VCT_DEBUT_YEAR'))
vct_curr_year = datetime.now().year

sc = Scraper()

# Looping thru vct year (2021 to Current year)
for year in range(vct_debut_year, vct_curr_year + 1):
    filename = f"{events_url_dir}/vct-{year}-events.txt"
    url = f"{vlrgg_vct_url}{year}"
    # Check if file exists
    if os.path.isfile(filename):
        try:
            # Ask permission to overwrite
            overwrite_dialog = inputimeout(f"File {filename} exists. Overwrite it ? [y/n][y by default] : ", 5) or "y"

            # Overwriting
            if overwrite_dialog.lower() == "y":
                print("[INFO]", f"Overwriting {filename}")
                # Scrap URLs
                with open(filename, "w") as dest_file:
                    events_urls = sc.scrap_events_url(url)
                    for u in events_urls:
                        dest_file.write(f"{u}\n")
                dest_file.close()

            # else skip this year
            else:
                continue
        # Default to skip after timeout
        except TimeoutOccurred:
            continue
    # else create it normally
    else:
        print("[INFO]", f"Creating {filename}")
        # Scrap URLs
        with open(filename, "w") as dest_file:
            events_urls = sc.scrap_events_url(url)
            for u in events_urls:
                dest_file.write(f"{u}\n")
        dest_file.close()
    


