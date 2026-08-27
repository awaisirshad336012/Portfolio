"""
Runs the live Selenium scraper for a search query and writes the
results into the database — the missing link between scraper output
and everything downstream (EDA, ML, dashboard).

Run this repeatedly over time (e.g. daily, via cron/Task Scheduler)
to build real price history, same as the synthetic generator does
for demo data.

Usage:
    python -m scripts.scrape_and_store "laptop" --pages 2
"""

import argparse
import logging

from database.database import init_db, upsert_products
from scraper.selenium_scraper import scrape_search_query

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Scrape Daraz and store results in the database.")
    parser.add_argument("query", help="Search term, e.g. 'laptop'")
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--no-headless", action="store_true")
    args = parser.parse_args()

    init_db()

    products = scrape_search_query(args.query, pages=args.pages, headless=not args.no_headless)

    if not products:
        logger.error(
            "0 products scraped — nothing written to the database. "
            "Check scraper/beautifulsoup_scraper.py selectors against a fresh "
            "debug_page_*.html before re-running."
        )
        return

    records = [p.to_dict() for p in products]
    count = upsert_products(records)
    logger.info(f"Wrote {count} price_history rows for '{args.query}' into the database.")


if __name__ == "__main__":
    main()
