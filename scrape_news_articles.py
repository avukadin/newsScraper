import os

import pandas as pd

import parameters as params
from pkg.GoogleRSSParser import GoogleRSSParser
from pkg.TextScrapper import TextScrapper

if __name__ == "__main__":
    if not os.path.exists("./data"):
        os.mkdir("./data")

    for query in params.QUERIES:
        for source in params.WEBSITES:
            links_file = f"./data/links_{query}_{source}.csv"

            # Gather Links
            if not os.path.exists(links_file):
                df = GoogleRSSParser().query_stories(
                           start_date=params.START_DATE,
                           end_date=params.END_DATE,
                           days_per_query=params.DAYS_PER_QUERY,
                           query=query,
                           source=source
                       )
                df.to_csv(links_file, index=False)
            else:
                print(f"Using links from {links_file}")
                df = pd.read_csv(links_file)

            # Gather Stories
            extra_cols = {'queries':[query]*len(df), "pudDates": list(df["pubDates"])}
            TextScrapper().scrapeLinks(list(df['links']), extra_cols=extra_cols) 
