"""
Database layer — SQLite for now (swap to Postgres later by changing
only this file; callers use the same functions).

Two tables:
  products       — one row per unique product (latest known snapshot)
  price_history  — one row per (product, scraped_at) — the time series
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "price_intelligence.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    product_url      TEXT PRIMARY KEY,
    product_name      TEXT NOT NULL,
    category          TEXT,
    brand             TEXT,
    seller            TEXT,
    first_seen_at     TEXT NOT NULL,
    last_seen_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS price_history (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    product_url       TEXT NOT NULL REFERENCES products(product_url),
    price             REAL,
    original_price    REAL,
    discount_percent  REAL,
    rating            REAL,
    num_reviews       INTEGER,
    availability      TEXT,
    scraped_at        TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_price_history_url ON price_history(product_url);
CREATE INDEX IF NOT EXISTS idx_price_history_time ON price_history(scraped_at);
"""


@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def upsert_products(products: Iterable[dict]) -> int:
    """
    Insert/update product master rows + append a price_history row for
    each. `products` are dicts matching scraper.schema.Product.to_dict().
    Returns the number of records written.
    """
    count = 0
    with get_connection() as conn:
        cur = conn.cursor()
        for p in products:
            cur.execute(
                """
                INSERT INTO products (product_url, product_name, category, brand, seller,
                                       first_seen_at, last_seen_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(product_url) DO UPDATE SET
                    product_name = excluded.product_name,
                    category     = excluded.category,
                    brand        = COALESCE(excluded.brand, products.brand),
                    seller       = COALESCE(excluded.seller, products.seller),
                    last_seen_at = excluded.last_seen_at
                """,
                (p["product_url"], p["product_name"], p.get("category"), p.get("brand"),
                 p.get("seller"), p["scraped_at"], p["scraped_at"]),
            )
            cur.execute(
                """
                INSERT INTO price_history (product_url, price, original_price, discount_percent,
                                            rating, num_reviews, availability, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (p["product_url"], p.get("price"), p.get("original_price"),
                 p.get("discount_percent"), p.get("rating"), p.get("num_reviews"),
                 p.get("availability"), p["scraped_at"]),
            )
            count += 1
    return count


def fetch_all_products() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM products").fetchall()


def fetch_price_history(product_url: str) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM price_history WHERE product_url = ? ORDER BY scraped_at",
            (product_url,),
        ).fetchall()


def fetch_latest_snapshot() -> list[sqlite3.Row]:
    """One row per product: its most recent price_history entry joined with product info."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT p.product_url, p.product_name, p.category, p.brand, p.seller,
                   h.price, h.original_price, h.discount_percent, h.rating,
                   h.num_reviews, h.availability, h.scraped_at
            FROM products p
            JOIN price_history h ON h.product_url = p.product_url
            WHERE h.scraped_at = (
                SELECT MAX(scraped_at) FROM price_history h2 WHERE h2.product_url = p.product_url
            )
            """
        ).fetchall()


if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")
