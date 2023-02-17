import time
from random import random
import requests
from parameters import MAX_DELAY, MIN_DELAY

def robustQuery(url:str, min_delay=MIN_DELAY, max_delay=MAX_DELAY, retries=3, timeout=60, headers={}):
    assert min_delay<=max_delay, "must have min_delay<=max_delay"
    assert retries>=0, "must have retries>=0"
    assert timeout>0, "must have timeout>0"

    for n in range(retries): # Try the query up to `retiries` times
        time.sleep(min_delay+(max_delay-min_delay)*random()) # sleep seconds to avoid being blocked
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError:
            if n==retries-1:
                raise
            print(response.content)
            print(f"Failed with status: {response.status_code} on attempt {n}, retrying.")
            print(f"Failed URL: {url}")
            time.sleep((n+1)*2)

