import re
import html

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

        # If the text contains a comma, double quotes, or newline, wrap it in quotes
        if any(char in text for char in [',', '"', '\n', '\r']):
            text = f'"{text}"'

        # Escape single quotes for SQL
        text = text.replace("'", "\'")

        return text
            
    @staticmethod
    def clean_float(text):
        text = TextUtils.clean_str(text)
        text.replace('%', '').replace('$', '').replace('€', '')
        try:
            result = float(text)
        except:
            result = 0
        return result
        
