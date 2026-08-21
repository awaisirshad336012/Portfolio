import pandas as pd
from src.pipeline import prepare_transactions, summarize

def test_pipeline():
    df = prepare_transactions(pd.DataFrame({
        "date":["2026-01-01","2026-01-02"],
        "description":["Client payment","Office rent"],
        "amount":[1000,-300],
    }))
    assert len(df) == 2
    s = summarize(df)
    assert s["revenue"] == 1000
    assert s["expenses"] == 300
    assert s["net_cashflow"] == 700
