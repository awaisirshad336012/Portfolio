"""
Phase 3/4 - Price analysis.

Trend and volatility metrics per product, computed directly from
price_history — independent of the ML models (models/ predicts a
*future* price; this module describes the *observed* history).
"""

import pandas as pd

from database.database import fetch_price_history


def product_price_trend(product_url: str) -> pd.DataFrame:
    """Return the price history for one product as a tidy DataFrame."""
    rows = fetch_price_history(product_url)
    df = pd.DataFrame([dict(r) for r in rows])
    if not df.empty:
        df["scraped_at"] = pd.to_datetime(df["scraped_at"])
    return df


def trend_summary(df: pd.DataFrame) -> dict:
    """Simple, explainable trend stats — no ML involved."""
    if df.empty or len(df) < 2:
        return {"trend": "insufficient_data"}

    first, last = df["price"].iloc[0], df["price"].iloc[-1]
    pct_change = (last - first) / first * 100 if first else 0
    volatility = df["price"].std()

    if pct_change < -2:
        direction = "falling"
    elif pct_change > 2:
        direction = "rising"
    else:
        direction = "stable"

    return {
        "trend": direction,
        "pct_change": round(pct_change, 2),
        "volatility": round(volatility, 2) if volatility == volatility else 0,  # NaN check
        "current_price": last,
        "lowest_price": df["price"].min(),
        "highest_price": df["price"].max(),
    }
