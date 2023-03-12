import os
import time
from random import random

import pandas as pd
import requests
from bs4 import BeautifulSoup

from pkg.robustQuery import robustQuery


class TextScrapper:

    def scrapeLinks(self, links:list[str], extra_cols:dict[str,list[str]] = {}):
        for k,v in extra_cols.items():
            assert len(v)==len(links), f"required len(extra_cols[{k}]) == len(links)"

        if os.path.exists("./data/scrapped.csv"):
            print("Collecting articles from checkpoint: ./data/scrapped.csv")
            df = pd.read_csv("./data/scrapped.csv")
        else:
            print("Collecting articles...")
            data = {'links':[], 'articles':[]}
            # Add extra_cols
            for k in extra_cols.keys():
                data[k] = [] 
            df = pd.DataFrame(data)

        threshold = 0
        count = 0
        gathered = set(df['links'])
        for i in range(len(links)):
            link = links[i]
            # Skip already scraped links
            if link in gathered:
                continue

            # Query
            page = robustQuery(link)

            soup = BeautifulSoup(page.content, "html.parser")
            txt = ' '.join([p.get_text() for p in soup.find_all("p")])

            # Save
            data = {'links':[link], "articles":[txt]}
            for k in extra_cols.keys():
                data[k] = [extra_cols[k][i]]
            df = pd.concat([df, pd.DataFrame(data)])
            df.to_csv("./data/scrapped.csv", index=False)

            # Print status
            count += 1
            completed = round(100*count/len(links),1)
            if completed>threshold:
                print(f"Percent articles gathered: {completed}%")
                threshold += 10

