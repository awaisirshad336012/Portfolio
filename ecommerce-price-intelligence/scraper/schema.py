"""
Defines the shape of a single scraped product record.

Every scraper (requests/BS4 now, Selenium/Scrapy later) should
produce dicts matching this schema so downstream code (cleaning,
database, ML) doesn't care which scraper produced the data.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    product_name: str
    category: str
    brand: Optional[str]
    price: Optional[float]
    original_price: Optional[float]
    discount_percent: Optional[float]
    rating: Optional[float]
    num_reviews: Optional[int]
    availability: Optional[str]
    seller: Optional[str]
    product_url: str
    scraped_at: str = None  # ISO timestamp, set automatically if missing

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)
