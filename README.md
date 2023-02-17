# News Scrapper
Simple repo which gathers news aricles from the web. The service uses the Google RSS News Feed to search for news articles by keyword, then scrapes the articles from the returned links. 


## Configuration
Use the `parameters.py` file to specify:
1. `WEBSITES`: a list of websites to gather articles from. 
2. `QUERIES`: a list of terms which mush be contained in the articles
3. `START_DATE`: the earliest the articles are published (inclusive)
4. `END_DATE`: the latest the articles are published (exclusive)
5. `DAYS_PER_QUERY`: the number of days off links to gather per query to Google RSS
6. `MIN_DELAY`: the min seconds to wait between queries
7. `MAX_DELAY`: the max seconds to wait between queries


## Running the Scrapper

1. Install all requirements from requirements.txt
2. Run `scrape_news_articles.py`

All data is saved in CSV in the ./data folder.
Note that in order to avoid being blocked by either Google RSS Feed or the news site itself, there is a delay between queries of 5 to 8 seconds by default. You may want to let this service run overnight, or change the delay time between queries.
