import time
import requests
from .logging_config import log


def safe_request(url, params=None, headers=None, retries=3, delay=1):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            log(f"[safe_request] Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
    return None
