from datetime import datetime


# News Scraping
WEBSITES = ["cnbc.com", "reuters.com"]
QUERIES = ["AAPL", "MSFT", "AMZN", "NVDA", "TSLA"]
START_DATE = datetime(2023,12,31) # Inclusive
END_DATE = datetime(2023,12,31) # Exclusive
DAYS_PER_QUERY = 14
MIN_DELAY = 1
MAX_DELAY = 2
