import psycopg2
import os
import traceback
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

load_dotenv()
# VCT year
vct_debut_year = int(os.getenv('VCT_DEBUT_YEAR'))
vct_curr_year = datetime.now().year
# current year to debut year (Recent year contains less matches)
year_range = range(vct_curr_year , vct_debut_year - 1 , -1)


conn = psycopg2.connect(database=os.getenv('POSTGRES_DB_NAME'), 
    user=os.getenv('POSTGRES_DB_USER'), password=os.getenv('POSTGRES_DB_PASSWORD'), 
    host=os.getenv('POSTGRES_DB_HOST'), port=os.getenv('POSTGRES_DB_PORT')
) 

conn.autocommit = True
cursor = conn.cursor() 

for year in year_range:
    file_path = Path(f'output/vct-events-datasets/vct-{year}-events-data.csv').resolve()
    try:
        sql2 = f'''COPY events
            from '{file_path}'
            WITH (
                FORMAT CSV,
                DELIMITER ',',
                ENCODING 'UTF8'
            );'''
        cursor.execute(sql2)
        print("[INFO]", f"{file_path} inserted")
    except:
        print("[ERROR]", traceback.format_exc())


print("--")

for year in year_range:
    file_path = Path(f'output/vct-matches-datasets/vct-{year}-matches-data.csv').resolve()
    try:
        sql2 = f'''COPY matches
            from '{file_path}'
            WITH (
                FORMAT CSV,
                DELIMITER ',',
                ENCODING 'UTF8'
            );'''
        cursor.execute(sql2)
        print("[INFO]", f"{file_path} inserted")
    except:
        print("[ERROR]", traceback.format_exc())

print("--")

for year in year_range:
    file_path = Path(f'output/vct-match-map-ovws-datasets/vct-{year}-match-overviews-data.csv').resolve()
    try:
        sql2 = f'''COPY match_map_overviews
            from '{file_path}'
            WITH (
                FORMAT CSV,
                DELIMITER ',',
                ENCODING 'UTF8'
            );'''
        cursor.execute(sql2)
        print("[INFO]", f"{file_path} inserted")
    except:
        print("[ERROR]", traceback.format_exc())

print("--")

for year in year_range:
    file_path = Path(f'output/vct-match-map-players-datasets/vct-{year}-players-data.csv').resolve()
    try:
        sql2 = f'''COPY match_map_player_stats (
            match_id,
            match_map_id,
            player_id,
            player_name,
            team_name,
            agent,
            
            rating_20,
            average_combat_score,
            kills,
            deaths,
            assists,
            kd_ratio,
            kill_assists_trade_survival_perc,
            average_dmg_per_round,
            headshot_percentages,
            first_kills,
            first_deaths,
            first_kill_deaths_ratio,
            side
        )
            from '{file_path}'
            WITH (
                FORMAT CSV,
                DELIMITER ',',
                ENCODING 'UTF8'
            );'''
        cursor.execute(sql2)
        print("[INFO]", f"{file_path} inserted")
    except:
        print("[ERROR]", traceback.format_exc())

conn.commit() 
conn.close() 
