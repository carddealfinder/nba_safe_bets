import time
import requests
from utils.logging_config import log

def safe_request(url, params=None, headers=None, max_retries=5, delay=1.0):
    """
    Makes an HTTP request with retry and logging.
    Returns parsed JSON if successful, otherwise None.
    """
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=10)

            # NBA Stats API blocks too-fast requests
            if r.status_code == 429:
                log.warning(f"Rate limited (429). Sleeping 1.5 sec... Attempt {attempt}/{max_retries}")
                time.sleep(1.5)
                continue

            if r.status_code != 200:
                log.warning(f"Non-200 status {r.status_code} for {url}. Attempt {attempt}/{max_retries}")
                time.sleep(delay)
                continue

            return r.json()

        except Exception as e:
            log.error(f"Request error for {url} on attempt {attempt}: {e}")
            time.sleep(delay)

    log.error(f"FAILED after {max_retries} attempts: {url}")
    return None
