import time
from datetime import datetime, timedelta
from random import random

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pkg.robustQuery import robustQuery

class GoogleRSSParser:
    base_url = 'https://news.google.com/rss/search?q="{query}"+inurl:{source}+after:{start_date}+before:{end_date}'

    def query_stories(self, start_date:datetime, end_date:datetime, query:str, source:str, days_per_query:int):
        assert start_date<end_date, "require start_date<end_date"
        start_dates, end_dates = self._get_randomized_dates(start_date, end_date, days_per_query)

        dfs = []
        threshold = 0
        count = 0
        for s, e in zip(start_dates, end_dates):
            stories = self._make_query(s, e, query, source)
            dfs.append(stories)

            # Print status
            count += 1
            completed = round(100*count/len(start_dates),1)
            if completed>threshold:
                print(f"Percent complete for {query} from {source}: {completed}%")
                threshold += 10

        df = pd.concat(dfs)
        return df

    def _make_query(self, start_date:datetime, end_date:datetime, query:str, source:str):
        url = self._make_url(start_date, end_date, query, source)
 
        response = robustQuery(url)

        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all('item')

        data = {
            "titles": [item.title.get_text() for item in items],
            "pubDates": [self.parse_date(item.pubDate.get_text()) for item in items],
            "links": [item.link.get_text() for item in items]
        }
 
        return pd.DataFrame(data)

    def _make_url(self, start_date:datetime, end_date:datetime, query:str, source:str):
        s = start_date.strftime('%Y-%m-%d')
        e = end_date.strftime('%Y-%m-%d')
        url = self.base_url.format(query=query, source=source, start_date=s, end_date=e)
        return url

    @staticmethod
    def _get_randomized_dates(start_date:datetime, end_date:datetime, days_per_query:int):
        # Randomizing dates may help us avoid being blocked
        current_date = start_date
        start_dates, end_dates = [], []
        while current_date <= end_date:
            next_date = min(end_date, current_date + timedelta(days=days_per_query))

            start_dates.append(current_date)
            end_dates.append(next_date)

            current_date += timedelta(days=days_per_query)

        ndx = np.random.choice(range(len(start_dates)), len(start_dates), replace=False)
        return list(np.array(start_dates)[ndx]), list(np.array(end_dates)[ndx])
        
    @staticmethod
    def parse_date(date:str):
        return datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
