"""
Phase 5 (prep) - Feature engineering for the ML models.

Builds the feature matrix from price_history: rolling stats per
product that let the model see trend/volatility, not just a single
snapshot.
"""

import pandas as pd


def build_features(history_df: pd.DataFrame, min_points: int = 3) -> pd.DataFrame:
    """
    From long-format price_history (product_url, price, scraped_at, ...),
    build one feature row per product using its most recent snapshot
    plus rolling statistics computed from its history.

    Products with fewer than `min_points` historical price points are
    dropped — not enough history yet to compute meaningful trend features.
    """
    if history_df.empty:
        return pd.DataFrame()

    df = history_df.copy()
    df["scraped_at"] = pd.to_datetime(df["scraped_at"])
    df = df.sort_values(["product_url", "scraped_at"])

    rows = []
    for url, g in df.groupby("product_url"):
        if len(g) < min_points:
            continue

        # IMPORTANT: features come from all history EXCEPT the most recent
        # point, and the target is that held-out most recent price. This
        # avoids leakage (predicting a price using a feature computed from
        # that same price) and mirrors how the model will be used in
        # production: given history so far, predict the next price.
        history = g.iloc[:-1]
        target_row = g.iloc[-1]
        price_series = history["price"].astype(float)

        rows.append({
            "product_url": url,
            "product_name": g["product_name"].iloc[-1] if "product_name" in g else None,
            "category": g["category"].iloc[-1] if "category" in g else None,
            "current_price": price_series.iloc[-1],
            "rating": history["rating"].iloc[-1] if "rating" in history else None,
            "num_reviews": history["num_reviews"].iloc[-1] if "num_reviews" in history else None,
            "discount_percent": history["discount_percent"].iloc[-1] if "discount_percent" in history else None,
            "price_mean": price_series.mean(),
            "price_std": price_series.std(ddof=0),
            "price_min": price_series.min(),
            "price_max": price_series.max(),
            "price_change_pct": (
                (price_series.iloc[-1] - price_series.iloc[0]) / price_series.iloc[0] * 100
                if price_series.iloc[0] else None
            ),
            "num_price_points": len(price_series),
            "target_price": target_row["price"],
        })

    return pd.DataFrame(rows)
