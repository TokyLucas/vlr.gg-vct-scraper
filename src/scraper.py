import requests
import traceback
import logging

from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

from src.entity.event import Event
from src.entity.match import Match
from src.entity.match_map_overview import MatchMapOverview
from src.entity.match_map_player_stats import MatchMapPlayerStats

from src.utils.text_utils import TextUtils

class Scraper:
    def __init__(self):
        log_file = f'logs//scrapping-{datetime.now().strftime('%y%m%d%H%M%S')}.log'
        logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        self.logger=logging.getLogger(__name__)

    def scrap_events_url(self, url):
        events_url = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            div_match_list = soup.find_all('div', class_="events-container-col")
            completed_events = div_match_list[-1]
            if completed_events:
                links = completed_events.find_all('a', class_='event-item')
                for link in links:
                    events_url.append(link.get('href'))
        except Exception as ex:
            print("[ERROR]", ex)

        return events_url

    def scrap_matches_url(self, url):
        match_urls = []
        try:
            url = url.replace("/event/", "/event/matches/")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            match_links = soup.find_all('a', class_="match-item")
            for link in match_links:
                match_urls.append(link.get('href'))
            
        except Exception as ex:
            print("[ERROR]", ex)

        return match_urls
        
    def scrap_event_data(self, event_url):
        event = None
        try:
            event_url = event_url.replace('\n', '')
            response = requests.get(event_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            event_header = soup.find('div', class_="event-header")
            if event_header:
                event_id = event_url.split('/')[4] if not None else -1
                title = TextUtils.clean_str(event_header.find('h1', class_="wf-title").text if not None else 'No title')
                desc = TextUtils.clean_str(event_header.find('h2', class_="event-desc-subtitle").text if not None else 'No description')

                desc_item = event_header.find_all('div', class_="event-desc-item")

                date = TextUtils.parse_date_range(desc_item[0].find('div', class_="event-desc-item-value").text) if not None else ''
                starting_date = date[0] if not None else ''
                ending_date = date[1] if not None else ''
                
                prize_pool = TextUtils.clean_float(desc_item[1].find('div', class_="event-desc-item-value").text) if not None else 0
                location = TextUtils.clean_str(desc_item[2].find('div', class_="event-desc-item-value").text) if not None else ''

                event = Event(event_id, title, desc, starting_date, ending_date, prize_pool, location)
            assert KeyError
        except Exception as ex:
            print("[ERROR]", ex)
            
        return event
    
    def scrap_match_data(self, match_url):
        match = None
        match_map_overviews = []
        try:
            match_url = match_url
            match_id = match_url.split('/')[3] if not None else -1
            response = requests.get(match_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            html_match_header = soup.find('div', class_='match-header')

            if html_match_header:
                # Scrap event data from <div class='match-header'> and <a class='match-header-event'>
                html_event_block = html_match_header.find('a', class_='match-header-event')
                event_url = TextUtils.clean_str(html_event_block.get('href') if not None else '')
                event_id = TextUtils.clean_str(event_url.split('/')[2] if not None else -1)
                event_name = TextUtils.clean_str(html_event_block.find('div').find('div').text if not None else '')
                event_series = TextUtils.clean_str(html_match_header.find('div', class_='match-header-event-series').text if not None else '')

                html_match_event_date = html_match_header.find('div', class_='match-header-date').find_all('div')
                match_date = TextUtils.clean_str(html_match_event_date[0].text if not None else '')
                match_patch = ''
                if len(html_match_event_date) > 2:
                    match_patch = TextUtils.clean_str(html_match_event_date[2].text if not None else '')

                # Team and score
                html_match_event_vs = html_match_header.find('div', class_='match-header-vs')
                html_match_score1, vs, html_match_score2 = html_match_event_vs.find('div', class_='js-spoiler').find_all('span')
                match_team1_score = TextUtils.clean_float(html_match_score1.text if not None else 0)
                match_team2_score = TextUtils.clean_float(html_match_score2.text if not None else 0)

                html_match_teams_info = html_match_event_vs.find_all('a', class_='match-header-link')
                team1_id = TextUtils.clean_str( html_match_teams_info[0].get('href').split('/')[2] if not None else 0 )
                team1_name = TextUtils.clean_str( html_match_teams_info[0].find('div', class_="wf-title-med").text if not None else '' )

                team2_id = TextUtils.clean_str( html_match_teams_info[1].get('href').split('/')[2] if not None else 0 )
                team2_name = TextUtils.clean_str( html_match_teams_info[1].find('div', class_="wf-title-med").text if not None else '' )
                
                html_match_note = html_match_header.find('div', class_='match-header-note')
                match_note = TextUtils.clean_str(html_match_note.text if html_match_note is not None else '')

                match = Match(match_id, team1_id, team1_name, match_team1_score, team2_id, team2_name, match_team2_score, match_date, match_patch, match_note, event_name, event_series, event_id)

                html_match_overviews = soup.find_all('div', class_='vm-stats-game')
                for i in range(0, len(html_match_overviews)):
                    html_match_overviews_header = html_match_overviews[i].find('div', class_='vm-stats-game-header')
                    match_map_id = html_match_overviews[i].get('data-game-id') if not None else f"{match_id}{i}"
                    if html_match_overviews_header:
                        
                        html_score_atk = html_match_overviews_header.find_all('span', class_='mod-t')
                        html_score_def = html_match_overviews_header.find_all('span', class_='mod-ct')
                        
                        team1_atk_won = team1_def_won = team2_atk_won = team2_def_won = 0
                        if len(html_score_atk) == 2:
                            team1_atk_won = TextUtils.clean_float(html_score_atk[0].text)
                            team2_atk_won = TextUtils.clean_float(html_score_atk[1].text)
                        if len(html_score_def) == 2:
                            team1_def_won = TextUtils.clean_float(html_score_def[0].text)
                            team2_def_won = TextUtils.clean_float(html_score_def[1].text)
                        
                        html_score = html_match_overviews_header.find_all('div', class_='score')
                        match_team1_score = TextUtils.clean_float(html_score[0].text if not None else 0)
                        match_team2_score = TextUtils.clean_float(html_score[1].text if not None else 0)
                        
                        html_map_name = html_match_overviews_header.find('div', class_='map').find('span')
                        map_name = TextUtils.clean_str(html_map_name.text.replace('PICK', '') if not None else '')
                        
                        map_overview = MatchMapOverview(match_map_id, match_id , team1_id, team1_name, match_team1_score, team1_atk_won, team1_def_won, team2_id, team2_name, match_team2_score, team2_atk_won, team2_def_won, map_name)
                        match_map_overviews.append(map_overview)
            
        except Exception as ex:
            self.logger.error(traceback.format_exc())
            print("[ERROR]", traceback.format_exc())
            
        return match, match_map_overviews
    
    def scrap_match_player_data(self, match_url):
        match_player_data = []
        try:
            match_url = match_url
            match_id = match_url.split('/')[3] if not None else -1
            response = requests.get(match_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            html_match_overviews = soup.find_all('div', class_='vm-stats-game')
            for i in range(0, len(html_match_overviews)):
                html_match_overviews_header = html_match_overviews[i].find('div', class_='vm-stats-game-header')
                match_map_id = html_match_overviews[i].get('data-game-id') if not None else f"{match_id}{i}"
                if html_match_overviews_header:
                    html_tables = html_match_overviews[i].find_all('table')
                    for table in html_tables:
                        html_trs = table.find_all('tr')
                        if len(html_trs) > 5:
                            html_trs = html_trs[1:]
                        for tr in html_trs:
                            html_tds = tr.find_all('td')
                            
                            # Assuming the table will always have 14 cols
                            if len(html_tds) == 14:
                                # Player info
                                html_player = html_tds[0].find('a')
                                player_id = html_player.get('href').split('/')[2] if not None else -1
                                player_name = TextUtils.clean_str(html_player.find('div').text)
                                player_team = TextUtils.clean_str(html_player.find_all('div')[-1].text)
                                
                                html_player_agent = html_tds[1].find('img')
                                player_agent = TextUtils.clean_str(html_player_agent.get('title') if html_player_agent is not None else '' )
                                # Player stats
                                # Assuming the col 2 to 14 in the table is structured as follow:
                                # rating_20, average_combat_score, kills, deaths, assists, kd_ratio, kill_assits_trade_surival_perc, average_dmg_perround, headshot_percentages, first_kills, first_deaths, first_kill_deaths_ratio
                                atk_arr = []
                                def_arr = []
                                for i in range(2, 14):
                                    t, ct = html_tds[i].find_all('span', class_=['mod-t', 'mod-ct'])
                                    atk_arr.append(TextUtils.clean_float(t.text if not None else 0))
                                    def_arr.append(TextUtils.clean_float(ct.text if not None else 0))
                                
                                atk_rating_20, atk_average_combat_score, atk_kills, atk_deaths, atk_assists, atk_kd_ratio, atk_kill_assits_trade_surival_perc, atk_average_dmg_perround, atk_headshot_percentages, atk_first_kills, atk_first_deaths, atk_first_kill_deaths_ratio = atk_arr
                                
                                atk_stat = MatchMapPlayerStats(match_id, match_map_id, player_id, player_name, player_team, player_agent, atk_rating_20, atk_average_combat_score, atk_kills, atk_deaths, atk_assists, atk_kd_ratio, atk_kill_assits_trade_surival_perc, atk_average_dmg_perround, atk_headshot_percentages, atk_first_kills, atk_first_deaths, atk_first_kill_deaths_ratio, 'ATK')
                                match_player_data.append(atk_stat)
                                
                                def_rating_20, def_average_combat_score, def_kills, def_deaths, def_assists, def_kd_ratio, def_kill_assits_trade_surival_perc, def_average_dmg_perround, def_headshot_percentages, def_first_kills, def_first_deaths, def_first_kill_deaths_ratio = def_arr 
                                def_stat = MatchMapPlayerStats(match_id, match_map_id, player_id, player_name, player_team, player_agent, def_rating_20, def_average_combat_score, def_kills, def_deaths, def_assists, def_kd_ratio, def_kill_assits_trade_surival_perc, def_average_dmg_perround, def_headshot_percentages, def_first_kills, def_first_deaths, def_first_kill_deaths_ratio, 'DEF')
                                match_player_data.append(def_stat)
                                
                                break
                                
                                
                                
                    
                
        except Exception as ex:
            self.logger.error(traceback.format_exc())
            print("[ERROR]", traceback.format_exc())
        
        return match_player_data

