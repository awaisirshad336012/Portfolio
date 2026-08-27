"""
Phase 1 - low-level HTTP fetcher.

Responsible only for *getting* a page's HTML reliably and politely.
Parsing happens in beautifulsoup_scraper.py.
"""

import random
import time
import logging

import requests

from scraper.config import (
    HEADERS,
    REQUEST_DELAY_SECONDS,
    REQUEST_DELAY_JITTER,
    MAX_RETRIES,
    RETRY_BACKOFF_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def polite_delay() -> None:
    """Sleep between requests so we don't hammer the server."""
    delay = REQUEST_DELAY_SECONDS + random.uniform(0, REQUEST_DELAY_JITTER)
    time.sleep(delay)


def fetch_page(url: str) -> str | None:
    """
    Fetch a single page's HTML with retries and a polite delay.

    Returns the HTML as a string, or None if all retries failed.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)

            if response.status_code == 200:
                polite_delay()
                return response.text

            if response.status_code == 404:
                logger.warning(f"404 Not Found: {url}")
                return None

            logger.warning(
                f"Attempt {attempt}/{MAX_RETRIES} - "
                f"status {response.status_code} for {url}"
            )

        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt}/{MAX_RETRIES} - request error for {url}: {e}")

        time.sleep(RETRY_BACKOFF_SECONDS * attempt)  # backoff grows each retry

    logger.error(f"Failed to fetch after {MAX_RETRIES} attempts: {url}")
    return None


if __name__ == "__main__":
    # Quick manual smoke test
    test_url = "https://www.daraz.pk/"
    html = fetch_page(test_url)
    if html:
        print(f"Fetched {len(html)} characters from {test_url}")
    else:
        print("Fetch failed.")
