"""
Phase 1 - HTML parsing layer.

Turns raw HTML (from requests_scraper.fetch_page, or later from
Selenium's page_source) into a list of Product records.

IMPORTANT — read before relying on this:
Daraz's search/listing pages render their product grid with
JavaScript. A plain `requests.get()` often returns a mostly-empty
HTML shell with the products loaded in afterward by JS. This module
is written against the DOM structure Daraz uses (verified via public
examples: the grid lives in a
`<div data-qa-locator="general-products">` container), but you
should confirm it works on a real fetch before trusting it:

    python -m scraper.requests_scraper       # see how much HTML we actually get
    python -m scraper.beautifulsoup_scraper  # see how many products we parse out of it

If parsing returns 0 products, the page was very likely JS-rendered
and empty for a plain requests call — that's the signal to move to
the Selenium scraper (Phase 2) rather than a bug in this parser.
"""

import re
import logging
from typing import Optional

from bs4 import BeautifulSoup

from scraper.schema import Product

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def _clean_price(text: Optional[str]) -> Optional[float]:
    """'Rs. 249,999' -> 249999.0"""
    if not text:
        return None
    digits = re.sub(r"[^\d.]", "", text)
    try:
        return float(digits) if digits else None
    except ValueError:
        return None


def _clean_int(text: Optional[str]) -> Optional[int]:
    """'(1,234)' -> 1234"""
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def _clean_percent(text: Optional[str]) -> Optional[float]:
    """'-45%' -> 45.0"""
    if not text:
        return None
    digits = re.sub(r"[^\d.]", "", text)
    try:
        return float(digits) if digits else None
    except ValueError:
        return None


def parse_listing_page(html: str, category: str = "") -> list[Product]:
    """
    Parse a Daraz search/category listing page into a list of Products.

    Daraz uses randomly-generated CSS class names (e.g. 'Bm3ON') that
    change on every frontend deploy, so we deliberately do NOT select
    by class. Instead we rely on stable signals:
      - data-qa-locator="product-item" marks each card
      - product URLs (which embed the name + a numeric id, e.g.
        .../dell-latitude-5320-...-i837117978.html)
      - regex text search for price/rating/review patterns within
        each card's visible text, since the text itself is stable
        even when the wrapping class names aren't.

    `category` is passed in by the caller (e.g. from the search query
    or category URL) since it's usually not printed on every card.
    """
    soup = BeautifulSoup(html, "lxml")
    products: list[Product] = []

    grid = soup.find("div", {"data-qa-locator": "general-products"})
    if grid is None:
        logger.warning("Could not find product grid (data-qa-locator='general-products'). "
                        "Page may be JS-rendered and empty, or Daraz changed its markup.")
        return products

    cards = grid.find_all(attrs={"data-qa-locator": "product-item"})
    logger.info(f"Found {len(cards)} product-item card(s) inside the product grid.")

    seen_urls = set()  # Daraz sometimes duplicates cards in the DOM; dedupe by URL

    for card in cards:
        try:
            link_el = card.find("a", href=True)
            if not link_el:
                continue
            url = link_el["href"]
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("/"):
                url = "https://www.daraz.pk" + url

            if url in seen_urls:
                continue
            seen_urls.add(url)

            card_text = card.get_text(separator=" | ", strip=True)

            # --- Name: prefer the link's title/alt, fall back to slug in the URL ---
            name = link_el.get("title") or None
            if not name:
                img = card.find("img")
                if img and img.get("alt"):
                    name = img["alt"].strip()
            if not name:
                # Fall back to deriving a readable name from the URL slug
                slug_match = re.search(r"/products/([\w-]+)-i\d+\.html", url)
                if slug_match:
                    name = slug_match.group(1).replace("-", " ").title()

            # --- Price: first "Rs. X,XXX"-style number in the card text ---
            price_matches = re.findall(r"Rs\.?\s?([\d,]+)", card_text)
            price = _clean_price(price_matches[0]) if price_matches else None
            original_price = _clean_price(price_matches[1]) if len(price_matches) > 1 else None

            # --- Discount: "-45%" pattern ---
            discount_match = re.search(r"-(\d+)%", card_text)
            discount_percent = float(discount_match.group(1)) if discount_match else None

            # --- Rating: look for an aria-label like "4.5 out of 5" ---
            rating = None
            rating_el = card.find(attrs={"aria-label": re.compile(r"out of 5", re.I)})
            if rating_el:
                m = re.search(r"([\d.]+)\s*out of 5", rating_el["aria-label"], re.I)
                if m:
                    rating = float(m.group(1))

            # --- Review count: "(1,234)" pattern near a rating ---
            reviews_match = re.search(r"\((\d[\d,]*)\)", card_text)
            num_reviews = _clean_int(reviews_match.group(1)) if reviews_match else None

            if not name or not url:
                continue

            products.append(Product(
                product_name=name,
                category=category,
                brand=None,  # usually only on the product detail page
                price=price,
                original_price=original_price,
                discount_percent=discount_percent,
                rating=rating,
                num_reviews=num_reviews,
                availability="in_stock",  # out-of-stock items are usually excluded from listings
                seller=None,  # not reliably present on listing cards; fetch from detail page later
                product_url=url,
            ))

        except Exception as e:
            logger.warning(f"Skipped a card due to parse error: {e}")
            continue

    logger.info(f"Parsed {len(products)} products from listing page.")
    return products


if __name__ == "__main__":
    # Smoke test: fetch + parse a real search page
    from scraper.requests_scraper import fetch_page

    test_url = "https://www.daraz.pk/catalog/?q=laptop"
    html = fetch_page(test_url)
    if html:
        results = parse_listing_page(html, category="laptop")
        print(f"Got {len(results)} products.")
        for p in results[:3]:
            print(p.to_dict())
    else:
        print("Fetch failed — nothing to parse.")
