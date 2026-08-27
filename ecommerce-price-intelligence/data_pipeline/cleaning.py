"""
Phase 2 - Data cleaning.

Takes raw scraped Product dicts/DataFrames and fixes the messy parts:
missing prices, duplicate cards, obviously-broken values.
"""

import logging

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def clean_products(records: list[dict]) -> pd.DataFrame:
    """
    Turn a list of raw product dicts into a cleaned DataFrame.

    Rules:
      - drop rows with no product_url or no price
      - drop exact duplicate product_urls (keep first)
      - clip discount_percent to [0, 95] (bad parses sometimes yield junk %)
      - original_price must be >= price, otherwise treat as unknown
      - rating must be within [0, 5], otherwise null it out
    """
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    before = len(df)

    df = df.dropna(subset=["product_url"])
    df = df[df["price"].notna()]
    df = df.drop_duplicates(subset=["product_url"], keep="first")

    if "discount_percent" in df.columns:
        df["discount_percent"] = df["discount_percent"].clip(lower=0, upper=95)

    if "original_price" in df.columns and "price" in df.columns:
        bad_original = df["original_price"] < df["price"]
        df.loc[bad_original, "original_price"] = None

    if "rating" in df.columns:
        df.loc[(df["rating"] < 0) | (df["rating"] > 5), "rating"] = None

    after = len(df)
    logger.info(f"Cleaned {before} -> {after} rows ({before - after} dropped).")
    return df.reset_index(drop=True)
