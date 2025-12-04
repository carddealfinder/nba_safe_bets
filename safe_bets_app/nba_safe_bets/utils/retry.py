import time
import requests
from nba_safe_bets.utils.logging_config import log

def safe_request(url, params=None, headers=None, retries=3, delay=1):
    """Retry API requests with delay to avoid failures."""
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                log(f"[REQUEST ERROR] {url} -> {response.status_code}")
        except Exception as e:
            log(f"[EXCEPTION] {e}")

        time.sleep(delay)

    log(f"[FAILED AFTER RETRIES] {url}")
    return None
