"""
Phase 6 - E-commerce Price Intelligence Dashboard.

Run from the project root:
    streamlit run app/app.py

Reads from the database (data/processed/price_intelligence.db) and,
if trained models exist, shows price predictions + buy/wait
recommendations per product.
"""

import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Allow running via `streamlit run app/app.py` from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database import fetch_latest_snapshot, fetch_price_history, get_connection
from data_pipeline.feature_engineering import build_features
from analysis.price_analysis import product_price_trend, trend_summary

st.set_page_config(page_title="E-commerce Price Intelligence", layout="wide", page_icon="🛒")


@st.cache_data(ttl=60)
def load_snapshot() -> pd.DataFrame:
    rows = fetch_latest_snapshot()
    return pd.DataFrame([dict(r) for r in rows])


@st.cache_resource
def try_load_models():
    try:
        from models.predict import load_models
        return load_models()
    except FileNotFoundError:
        return None


st.title("🛒 E-commerce Price Intelligence")

snapshot_df = load_snapshot()

if snapshot_df.empty:
    st.warning(
        "No data in the database yet.\n\n"
        "Run the scraper (`python -m scraper.selenium_scraper \"laptop\" --pages 1`) "
        "or generate demo data with `python -m scripts.generate_synthetic_data`, "
        "then refresh this page."
    )
    st.stop()

is_demo = st.session_state.get("is_demo", None)
# Heuristic: synthetic data always uses this seller naming pattern
if snapshot_df["seller"].astype(str).str.contains("Official Store").any():
    st.info("📊 Showing **demo/synthetic data** — swap in real scraped data anytime; "
            "everything below updates automatically once the database has real rows.")

# --- Overview ---
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Products Tracked", len(snapshot_df))
col2.metric("Avg Price", f"Rs. {snapshot_df['price'].mean():,.0f}")
col3.metric("Avg Discount", f"{snapshot_df['discount_percent'].mean():.1f}%")
col4.metric("Avg Rating", f"{snapshot_df['rating'].mean():.1f} ⭐")

# --- Price trends by category ---
st.subheader("Price Trends")
category_filter = st.multiselect(
    "Filter by category", options=sorted(snapshot_df["category"].dropna().unique()),
)
filtered_df = snapshot_df[snapshot_df["category"].isin(category_filter)] if category_filter else snapshot_df

col_a, col_b = st.columns(2)
with col_a:
    fig = px.histogram(filtered_df, x="price", nbins=25, title="Price Distribution")
    st.plotly_chart(fig, use_container_width=True)
with col_b:
    avg_by_cat = filtered_df.groupby("category")["price"].mean().reset_index()
    fig2 = px.bar(avg_by_cat, x="category", y="price", title="Avg Price by Category")
    st.plotly_chart(fig2, use_container_width=True)

# --- Product analysis ---
st.subheader("Product Analysis")
product_name_to_url = dict(zip(filtered_df["product_name"], filtered_df["product_url"]))
selected_name = st.selectbox("Select a product", options=sorted(product_name_to_url.keys()))
selected_url = product_name_to_url[selected_name]

history_df = product_price_trend(selected_url)

if not history_df.empty:
    fig3 = px.line(history_df, x="scraped_at", y="price", title=f"Price History — {selected_name}", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    summary = trend_summary(history_df)
    col_x, col_y, col_z = st.columns(3)
    col_x.metric("Trend", summary.get("trend", "n/a").title())
    col_y.metric("Change over period", f"{summary.get('pct_change', 0):+.1f}%")
    col_z.metric("Current Price", f"Rs. {summary.get('current_price', 0):,.0f}")

# --- ML recommendation ---
st.subheader("🤖 Buy / Wait Recommendation")
models = try_load_models()

if models is None:
    st.info("No trained models found yet. Run `python -m models.train` first "
            "(needs products with at least 3 price history points).")
else:
    price_model, buy_wait_model, encoder, feature_columns = models

    with get_connection() as conn:
        full_history = pd.read_sql_query(
            """
            SELECT h.product_url, p.product_name, p.category, h.price, h.original_price,
                   h.discount_percent, h.rating, h.num_reviews, h.availability, h.scraped_at
            FROM price_history h JOIN products p ON p.product_url = h.product_url
            WHERE h.product_url = ?
            """,
            conn, params=(selected_url,),
        )

    features_df = build_features(full_history, min_points=2)

    if features_df.empty:
        st.warning("Not enough price history for this product yet to generate a prediction "
                    "(needs at least a couple of tracked snapshots over time).")
    else:
        from models.predict import predict_for_row
        row = features_df.iloc[-1].drop("target_price")
        result = predict_for_row(row, price_model, buy_wait_model, encoder, feature_columns)

        rec = result["recommendation"]
        color = "🟢" if rec == "BUY" else "🟡"

        col_p, col_q = st.columns([1, 2])
        with col_p:
            st.markdown(f"### {color} {rec}")
            st.caption(f"Confidence: {result['confidence']*100:.0f}%")
        with col_q:
            st.write(f"**Current Price:** Rs. {result['current_price']:,.0f}")
            st.write(f"**Predicted Price:** Rs. {result['predicted_price']:,.0f}")
            st.write(f"**Expected Change:** {result['expected_change_pct']:+.1f}%")

# --- Full table ---
with st.expander("📋 View all tracked products"):
    st.dataframe(
        filtered_df[["product_name", "category", "brand", "price", "discount_percent", "rating", "num_reviews"]],
        use_container_width=True,
    )
