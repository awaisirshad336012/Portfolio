"""
Scraper configuration: headers, delays, base URLs.

Keep all "tunable" scraping behavior here so we don't hardcode
values inside the scraper logic itself.
"""

BASE_URL = "https://www.daraz.pk"

# A normal browser-like header set. Rotate/expand later if needed.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Be polite: wait this many seconds between requests (+ jitter).
REQUEST_DELAY_SECONDS = 2.0
REQUEST_DELAY_JITTER = 1.0  # random 0-1s added on top

# Retry behavior for flaky responses
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 3.0

# Timeout per request
REQUEST_TIMEOUT_SECONDS = 15
