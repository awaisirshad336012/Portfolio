"""
Phase 2 - Selenium scraper.

We moved to this earlier than planned: a plain `requests` call to
Daraz returned 403 (bot detection), so a real browser is needed to
render the page and get past that check.

Requires a local Chrome/Chromium install. Selenium 4.6+ auto-manages
the matching chromedriver for you (no manual driver download needed).

Usage:
    python -m scraper.selenium_scraper "laptop" --pages 2
"""

import argparse
import logging
import random
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from scraper.config import BASE_URL, REQUEST_DELAY_SECONDS, REQUEST_DELAY_JITTER
from scraper.beautifulsoup_scraper import parse_listing_page
from scraper.schema import Product

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def build_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a Chrome driver configured to look like a normal browser."""
    options = Options()
    if headless:
        # "new" headless mode is less detectable than the old headless flag
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    # Reduce the most obvious automation fingerprints
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )
    return driver


def polite_delay() -> None:
    time.sleep(REQUEST_DELAY_SECONDS + random.uniform(0, REQUEST_DELAY_JITTER))


def scrape_search_query(query: str, pages: int = 1, headless: bool = True) -> list[Product]:
    """
    Scrape `pages` pages of Daraz search results for `query`.
    Returns a combined list of Product records.
    """
    driver = build_driver(headless=headless)
    all_products: list[Product] = []

    try:
        for page in range(1, pages + 1):
            url = f"{BASE_URL}/catalog/?q={query.replace(' ', '+')}&page={page}"
            logger.info(f"Loading page {page}/{pages}: {url}")
            driver.get(url)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-qa-locator='general-products']")
                    )
                )
            except TimeoutException:
                logger.warning(f"Product grid never appeared on page {page} — "
                                f"skipping (possible CAPTCHA or layout change).")
                continue

            html = driver.page_source
            page_products = parse_listing_page(html, category=query)
            logger.info(f"Page {page}: parsed {len(page_products)} products")

            if len(page_products) == 0:
                # Save the raw HTML so we can inspect real selectors instead of guessing.
                debug_path = f"debug_page_{page}.html"
                with open(debug_path, "w", encoding="utf-8") as f:
                    f.write(html)
                logger.warning(
                    f"0 products parsed — saved raw HTML to {debug_path} for inspection."
                )

            all_products.extend(page_products)

            if page < pages:
                polite_delay()

    finally:
        driver.quit()

    return all_products


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Daraz search results via Selenium.")
    parser.add_argument("query", help="Search term, e.g. 'laptop'")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("--no-headless", action="store_true", help="Show the browser window")
    args = parser.parse_args()

    results = scrape_search_query(args.query, pages=args.pages, headless=not args.no_headless)

    print(f"\nScraped {len(results)} total products for '{args.query}'.")
    for p in results[:5]:
        print(p.to_dict())
