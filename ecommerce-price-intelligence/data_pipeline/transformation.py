"""
Phase 2 - Transformation.

Reshapes cleaned data for downstream analysis/ML: derived columns,
category normalization, price-history pivoting.
"""

import pandas as pd


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add simple derived fields used throughout analysis/ML."""
    df = df.copy()

    if "price" in df.columns and "original_price" in df.columns:
        df["implied_discount_pct"] = (
            (df["original_price"] - df["price"]) / df["original_price"] * 100
        ).round(1)
        # prefer the scraped discount if present, else the implied one
        if "discount_percent" in df.columns:
            df["discount_percent"] = df["discount_percent"].fillna(df["implied_discount_pct"])

    if "category" in df.columns:
        df["category"] = df["category"].str.strip().str.lower()

    return df


def pivot_price_history(history_df: pd.DataFrame) -> pd.DataFrame:
    """
    Wide-format price history: one row per product_url, one column per
    scraped_at date. Useful for quick trend inspection / correlation.
    """
    if history_df.empty:
        return history_df
    history_df = history_df.copy()
    history_df["scraped_at"] = pd.to_datetime(history_df["scraped_at"])
    return history_df.pivot_table(
        index="product_url", columns="scraped_at", values="price", aggfunc="last"
    )
