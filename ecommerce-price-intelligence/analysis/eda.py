"""
Phase 3 - EDA.

Summary stats and simple plots over the latest product snapshot +
full price history, pulled straight from the database.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt

from database.database import fetch_latest_snapshot, fetch_all_products


def load_snapshot_df() -> pd.DataFrame:
    rows = fetch_latest_snapshot()
    return pd.DataFrame([dict(r) for r in rows])


def summary_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    return {
        "num_products": len(df),
        "num_categories": df["category"].nunique(),
        "avg_price": round(df["price"].mean(), 2),
        "median_price": round(df["price"].median(), 2),
        "avg_discount_pct": round(df["discount_percent"].mean(), 2),
        "avg_rating": round(df["rating"].mean(), 2),
        "price_by_category": df.groupby("category")["price"].mean().round(2).to_dict(),
    }


def plot_price_distribution(df: pd.DataFrame, save_path: str = None):
    fig, ax = plt.subplots(figsize=(8, 5))
    df["price"].hist(bins=30, ax=ax)
    ax.set_title("Price Distribution")
    ax.set_xlabel("Price")
    ax.set_ylabel("Count")
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


def plot_discount_by_category(df: pd.DataFrame, save_path: str = None):
    fig, ax = plt.subplots(figsize=(8, 5))
    df.groupby("category")["discount_percent"].mean().sort_values().plot(kind="barh", ax=ax)
    ax.set_title("Average Discount % by Category")
    ax.set_xlabel("Discount %")
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    return fig


if __name__ == "__main__":
    df = load_snapshot_df()
    if df.empty:
        print("No data in the database yet. Run the scraper or "
              "`python -m scripts.generate_synthetic_data` first.")
    else:
        stats = summary_stats(df)
        for k, v in stats.items():
            print(f"{k}: {v}")
