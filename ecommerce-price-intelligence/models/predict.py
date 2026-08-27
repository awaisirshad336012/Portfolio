"""
Phase 5 - ML inference.

Loads the trained models and produces a prediction + BUY/WAIT
recommendation for a single product, given its feature row.
"""

import joblib
import pandas as pd

MODEL_DIR = "models/saved_models"


def load_models():
    price_model = joblib.load(f"{MODEL_DIR}/price_model.joblib")
    buy_wait_model = joblib.load(f"{MODEL_DIR}/buy_wait_model.joblib")
    encoder = joblib.load(f"{MODEL_DIR}/category_encoder.joblib")
    feature_columns = joblib.load(f"{MODEL_DIR}/feature_columns.joblib")
    return price_model, buy_wait_model, encoder, feature_columns


def predict_for_row(feature_row: pd.Series, price_model, buy_wait_model, encoder, feature_columns) -> dict:
    """
    `feature_row` should have the same columns as
    data_pipeline.feature_engineering.build_features() output
    (minus target_price), for a single product.
    """
    row = feature_row.copy()
    category = row.get("category", "unknown")
    try:
        row["category_encoded"] = encoder.transform([category])[0]
    except ValueError:
        row["category_encoded"] = -1  # unseen category at inference time

    X = pd.DataFrame([row])[feature_columns].fillna(0)

    predicted_price = float(price_model.predict(X)[0])
    recommendation = buy_wait_model.predict(X)[0]
    confidence = float(buy_wait_model.predict_proba(X).max())

    current_price = float(row["current_price"])
    expected_change_pct = round((predicted_price - current_price) / current_price * 100, 2) if current_price else None

    return {
        "current_price": current_price,
        "predicted_price": round(predicted_price, 2),
        "expected_change_pct": expected_change_pct,
        "recommendation": recommendation,
        "confidence": round(confidence, 3),
    }
