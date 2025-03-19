import re
import html

from datetime import datetime

class TextUtils:

    @staticmethod
    def clean_str(text):
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Decode HTML entities (e.g., &amp; -> &)
        text = html.unescape(text)
        
        # Trim whitespace
        text = text.strip()
        
        # Replace newlines and excessive spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        # Escape double quotes (needed for CSV)
        text = text.replace('"', '\"')

        # Escape single quotes for SQL
        text = text.replace("'", "\'")

        return text
            
    @staticmethod
    def clean_float(text):
        text = text.replace('%', '')
        text = text.replace('+', '')
        text = text.replace('$', '').replace('USD', '')
        text = text.replace(',', '')
        text = TextUtils.clean_str(text)
        try:
            result = float(text)
        except:
            result = 0
        return result
    
    @staticmethod
    def parse_date_range(date_range: str):
        # Split on the hyphen
        parts = date_range.split(" - ")
        first = parts[0].split(",")

        if len(first) > 1: # Case "Oct 12, 2021 - Nov 1, 2021"
            end_day_month, year = parts[1].split(",")
            end_day_month, year = end_day_month.strip(), year.strip()
            end_month, end_day = end_day_month.split(" ")
            end_month, end_day = end_month.strip(), end_day.strip()
            
            start_day_month, year = parts[0].split(",")
            start_day_month, year = start_day_month.strip(), year.strip()
            start_month, start_day = start_day_month.split(" ")
            start_month, start_day = start_month.strip(), start_day.strip()
            
            start_date = datetime.strptime(f"{start_day} {start_month} {year}", "%d %b %Y").date().strftime("%Y-%m-%d")
            end_date = datetime.strptime(f"{end_day} {end_month} {year}", "%d %b %Y").date().strftime("%Y-%m-%d")
            return (start_date, end_date)
        else: # Case "Aug 1 - 25, 2024"
            month, start_day = parts[0].split(" ")
            month, start_day = month.strip(), start_day.strip()
            
            end_day, year = parts[1].split(",")
            end_day, year = end_day.strip(), year.strip()
            
            start_date = datetime.strptime(f"{start_day} {month} {year}", "%d %b %Y").date().strftime("%Y-%m-%d")
            end_date = datetime.strptime(f"{end_day} {month} {year}", "%d %b %Y").date().strftime("%Y-%m-%d")
            
            return (start_date, end_date)
