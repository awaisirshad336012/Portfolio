"""
Phase 5 - ML training.

Model 1 — Price Prediction (regression): predicts next price from
  current price + history-derived features.
Model 2 — Buy/Wait (classification): BUY if predicted price is not
  meaningfully below current price, WAIT if it is (i.e. the model
  expects the price to drop).

Both are trained on data/feature_engineering.build_features() output.
With the synthetic data generator, this trains on demo data; swap in
real scraped history and nothing else changes.

Usage:
    python -m models.train
"""

import logging

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

from database.database import fetch_all_products, get_connection
from data_pipeline.feature_engineering import build_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MODEL_DIR = "models/saved_models"
FEATURE_COLUMNS = [
    "current_price", "rating", "num_reviews", "discount_percent",
    "price_mean", "price_std", "price_min", "price_max",
    "price_change_pct", "num_price_points", "category_encoded",
]

# A "WAIT" label means the model expects the price to fall by at least
# this % — otherwise "BUY" (waiting longer isn't expected to help much).
WAIT_THRESHOLD_PCT = 3.0


def _load_history_df() -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql_query(
            """
            SELECT h.product_url, p.product_name, p.category, h.price, h.original_price,
                   h.discount_percent, h.rating, h.num_reviews, h.availability, h.scraped_at
            FROM price_history h
            JOIN products p ON p.product_url = h.product_url
            """,
            conn,
        )
    return df


def prepare_training_data() -> tuple[pd.DataFrame, pd.Series, LabelEncoder]:
    history_df = _load_history_df()
    features_df = build_features(history_df)

    if features_df.empty:
        raise ValueError(
            "No products have enough price history to train on yet. "
            "Run the scraper repeatedly over time, or "
            "`python -m scripts.generate_synthetic_data` for a demo dataset."
        )

    encoder = LabelEncoder()
    features_df["category_encoded"] = encoder.fit_transform(features_df["category"].fillna("unknown"))
    features_df = features_df.fillna(features_df.median(numeric_only=True))

    X = features_df[FEATURE_COLUMNS]
    y = features_df["target_price"]
    return X, y, encoder, features_df


def train_price_model(X: pd.DataFrame, y: pd.Series) -> RandomForestRegressor:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    logger.info(f"Price model — MAE: {mae:,.2f}, R²: {r2:.3f} (on {len(X_test)} held-out rows)")

    return model


def train_buy_wait_model(X: pd.DataFrame, y_price: pd.Series, price_model: RandomForestRegressor):
    """
    Derive BUY/WAIT labels from the price model's own predictions vs.
    current_price, then train a classifier on the same features. This
    keeps the two models consistent with each other.
    """
    predicted = price_model.predict(X)
    current = X["current_price"].values
    pct_expected_change = (predicted - current) / current * 100

    labels = pd.Series(
        ["WAIT" if pct <= -WAIT_THRESHOLD_PCT else "BUY" for pct in pct_expected_change],
        index=X.index,
    )

    if labels.nunique() < 2:
        logger.warning("Only one class present in buy/wait labels — classifier will be trivial. "
                        "Needs more varied price history to be meaningful.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42,
        stratify=labels if labels.nunique() > 1 else None,
    )

    clf = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    logger.info(f"Buy/Wait model — accuracy: {acc:.3f}")
    logger.info("\n" + classification_report(y_test, preds, zero_division=0))

    return clf


def main():
    X, y, encoder, features_df = prepare_training_data()
    logger.info(f"Training on {len(X)} products.")

    price_model = train_price_model(X, y)
    buy_wait_model = train_buy_wait_model(X, y, price_model)

    joblib.dump(price_model, f"{MODEL_DIR}/price_model.joblib")
    joblib.dump(buy_wait_model, f"{MODEL_DIR}/buy_wait_model.joblib")
    joblib.dump(encoder, f"{MODEL_DIR}/category_encoder.joblib")
    joblib.dump(FEATURE_COLUMNS, f"{MODEL_DIR}/feature_columns.joblib")

    logger.info(f"Saved models to {MODEL_DIR}/")


if __name__ == "__main__":
    main()
