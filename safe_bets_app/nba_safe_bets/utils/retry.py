import time
import requests


def safe_request(url, params=None, headers=None, retries=3, delay=1):
    for _ in range(retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)
            r.raise_for_status()
            return r
        except:
            time.sleep(delay)
    return None
