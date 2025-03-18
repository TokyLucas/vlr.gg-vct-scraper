import requests

from bs4 import BeautifulSoup

from src.entity.event import Event
from src.entity.match import Match
from src.entity.match_overview import MatchOverview

from src.utils.text_utils import TextUtils

class Scraper:

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
            # response = requests.get(event_url)
            # soup = BeautifulSoup(response.content, 'html.parser')
            
            # event_header = soup.find('div', class_="event-header")
            if True:
                event_id = event_url.split('/')[4] or -1
                title = TextUtils.clean_str('Hello, "World"! &amp; Welcome\nto <i>SQL\'s</i> world.')
                event = Event(event_id, title)
            
        except Exception as ex:
            print("[ERROR]", ex)
            
        return event
    
    def scrap_match_data(self, match_url):
        match = None
        match_overviews = []
        try:
            match_url = match_url.replace('\n', '')
            match_id = match_url.split('/')[3] or -1
            #response = requests.get(url)
            #soup = BeautifulSoup(response.content, 'html.parser')

            #match_links = soup.find_all('a', class_="match-item")
            #for link in match_links:
                #match_urls.append(link.get('href'))
                
            match = Match(match_id, "match_url")
            match_overviews = [MatchOverview(1, "vct"), MatchOverview(1, "vct")]
            
        except Exception as ex:
            print("[ERROR]", ex)
            
        return match, match_overviews

            

