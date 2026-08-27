# 🛒 E-commerce Price Intelligence

Scrapes product data from Daraz.pk, tracks price history over time, predicts
future prices with ML, and recommends **Buy** or **Wait** — surfaced through
a Streamlit dashboard.

## ⚠️ Current status (read this first)

| Phase | Status |
|---|---|
| 1. Scraping | 🟡 Selenium gets past bot detection and finds real product cards; field-extraction selectors were just rewritten against real captured HTML but **not yet reverified** — run it and check |
| 2. Data cleaning/pipeline | ✅ Built & tested |
| 3. EDA | ✅ Built & tested |
| 4. Historical tracking | ✅ Database supports it — needs the scraper run repeatedly over time (e.g. daily) to build real history |
| 5. ML (price prediction + buy/wait) | ✅ Built & tested end-to-end on demo data |
| 6. Dashboard | ✅ Built & verified running (serves HTTP 200, no runtime errors) |
| 7. Tests | ✅ 7/7 passing |

**Everything downstream of scraping (database → cleaning → EDA → ML →
dashboard) is confirmed working, using a synthetic data generator as a
stand-in until the live Daraz scraper is fully verified.** Once the scraper
reliably pulls real products, swap it in — no other code changes needed,
since everything reads from the same database.

## Quick start (see it working right now, with demo data)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m scripts.generate_synthetic_data   # populates the database with demo data
python -m models.train                       # trains both ML models
streamlit run app/app.py                     # opens the dashboard
```

## Using real scraped data instead

```bash
python -m scripts.scrape_and_store "laptop" --pages 2
```

This runs the Selenium scraper and writes results straight into the same
database the synthetic generator uses — so once the scraper is confirmed
pulling real products, everything downstream (EDA, `models/train.py`, the
dashboard) picks it up automatically with zero other code changes. Run it
repeatedly over time (daily is reasonable) to build real price history.

## Problem

Online stores have thousands of products and prices change constantly. This
project answers: *"What's happening with product prices, and is a product
likely to get cheaper soon?"*

## Architecture

```
Daraz.pk → Selenium + BeautifulSoup scraper
         → Cleaning → Transformation → SQLite database
         → EDA + Feature Engineering
         → ML: Price Prediction (RandomForestRegressor) + Buy/Wait (RandomForestClassifier)
         → Streamlit Dashboard
```

## Data collected per product

Name, Category, Brand, Price, Original Price, Discount %, Rating,
Number of Reviews, Availability, Seller, Product URL, Scraped Date
— plus historical price snapshots over time (`price_history` table).

## Tech stack

| Layer | Tools |
|---|---|
| Scraping | Requests, BeautifulSoup, Selenium |
| Data | Pandas, NumPy, SQLite |
| ML | Scikit-learn (RandomForest), joblib |
| Viz | Matplotlib, Plotly |
| App | Streamlit |
| Testing | Pytest |

## Project structure

```
ecommerce-price-intelligence/
├── data/                    # raw / processed (incl. SQLite DB) / historical
├── scraper/                 # requests, beautifulsoup, selenium scrapers + schema
├── database/                 # SQLite schema + read/write functions
├── data_pipeline/             # cleaning, transformation, feature engineering
├── analysis/                  # EDA, price trend analysis
├── models/                    # train.py, predict.py, saved_models/
├── app/                        # app.py (real dashboard), debug_viewer.py (throwaway HTML inspector)
├── scripts/                    # generate_synthetic_data.py (demo data)
├── tests/                       # pytest suite
├── requirements.txt
└── README.md
```

## ML models — how they work

**Price Prediction** (`models/train.py::train_price_model`) — a
RandomForestRegressor trained on each product's history-derived features
(rolling mean/std/min/max price, rating, discount, review count) to predict
the *next* observed price. Held-out test MAE and R² are logged on every
training run.

**Buy/Wait** (`models/train.py::train_buy_wait_model`) — a
RandomForestClassifier trained on the same features. Labels are derived
from the price model's own predictions: if the predicted price is ≥3%
below the current price, label is `WAIT`; otherwise `BUY`. This keeps the
two models consistent with each other.

Both require at least a few historical price points per product to train
meaningfully — this is why historical tracking (running the scraper
repeatedly over time) matters, not just a single scrape.

## A note on scraping ethics

Daraz's `robots.txt` blocks checkout/cart/account pages, not product or
category listings, so scraping those is permitted. A plain `requests` call
gets blocked (403) by Daraz's bot detection, which is why this project uses
Selenium (a real browser) instead. Scraping still uses reasonable delays
between requests to avoid overloading their servers. If a source ever
blocks scraping entirely, switch to a permitted source or dataset.

## Running tests

```bash
pytest tests/ -v
```
