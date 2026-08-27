"""
Basic sanity tests. Run with: pytest tests/ -v
"""

import os
import sys
import tempfile

import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_pipeline.cleaning import clean_products
from data_pipeline.transformation import add_derived_columns
from data_pipeline.feature_engineering import build_features
from analysis.price_analysis import trend_summary


def test_clean_products_drops_missing_price():
    records = [
        {"product_url": "a", "price": 100, "original_price": 120, "discount_percent": 10, "rating": 4.5},
        {"product_url": "b", "price": None, "original_price": 120, "discount_percent": 10, "rating": 4.5},
    ]
    df = clean_products(records)
    assert len(df) == 1
    assert df.iloc[0]["product_url"] == "a"


def test_clean_products_drops_duplicates():
    records = [
        {"product_url": "a", "price": 100, "original_price": 120, "discount_percent": 10, "rating": 4.5},
        {"product_url": "a", "price": 100, "original_price": 120, "discount_percent": 10, "rating": 4.5},
    ]
    df = clean_products(records)
    assert len(df) == 1


def test_clean_products_nulls_bad_rating():
    records = [
        {"product_url": "a", "price": 100, "original_price": 120, "discount_percent": 10, "rating": 9.9},
    ]
    df = clean_products(records)
    assert pd.isna(df.iloc[0]["rating"])


def test_add_derived_columns_computes_implied_discount():
    df = pd.DataFrame([{"price": 90, "original_price": 100, "category": " Laptop "}])
    out = add_derived_columns(df)
    assert out.iloc[0]["implied_discount_pct"] == 10.0
    assert out.iloc[0]["category"] == "laptop"


def test_build_features_requires_min_points():
    history = pd.DataFrame([
        {"product_url": "a", "product_name": "X", "category": "laptop", "price": 100,
         "rating": 4, "num_reviews": 5, "discount_percent": 5, "scraped_at": "2026-01-01"},
        {"product_url": "a", "product_name": "X", "category": "laptop", "price": 95,
         "rating": 4, "num_reviews": 5, "discount_percent": 5, "scraped_at": "2026-01-02"},
    ])
    # only 2 points, default min_points=3 -> should be dropped
    features = build_features(history, min_points=3)
    assert features.empty

    features2 = build_features(history, min_points=2)
    assert len(features2) == 1
    assert features2.iloc[0]["target_price"] == 95  # held-out last point


def test_trend_summary_detects_falling_price():
    df = pd.DataFrame({
        "price": [100, 95, 90, 85],
        "scraped_at": pd.date_range("2026-01-01", periods=4),
    })
    summary = trend_summary(df)
    assert summary["trend"] == "falling"
    assert summary["pct_change"] < 0


def test_trend_summary_handles_empty():
    summary = trend_summary(pd.DataFrame())
    assert summary["trend"] == "insufficient_data"
