import pandas as pd
import numpy as np

KEYWORDS = {
    "rent":"Rent","office":"Office","software":"Software","subscription":"Software",
    "salary":"Payroll","payroll":"Payroll","marketing":"Marketing","advert":"Marketing",
    "ads":"Marketing","travel":"Travel","fuel":"Travel","food":"Meals","restaurant":"Meals",
    "invoice":"Revenue","client payment":"Revenue","payment received":"Revenue","sales":"Revenue",
    "refund":"Refund","utilities":"Utilities","internet":"Utilities","aws":"Infrastructure",
    "cloud":"Infrastructure","canva":"Software"
}

def infer_category(description, amount):
    text = str(description).lower()
    for key, category in KEYWORDS.items():
        if key in text:
            return category
    return "Other Income" if amount >= 0 else "Other Expense"

def prepare_transactions(df):
    df = df.copy()
    required = {"date","description","amount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(sorted(missing)))
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["description"] = df["description"].fillna("Unknown transaction").astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date","amount"]).drop_duplicates().reset_index(drop=True)
    df["amount_abs"] = df["amount"].abs()
    df["type"] = np.where(df["amount"] >= 0, "Income", "Expense")
    if "category" not in df.columns:
        df["category"] = [infer_category(d,a) for d,a in zip(df.description, df.amount)]
    else:
        df["category"] = df["category"].fillna("").astype(str)
        empty = df["category"].str.strip().eq("")
        df.loc[empty,"category"] = [infer_category(d,a) for d,a in zip(df.loc[empty,"description"], df.loc[empty,"amount"])]
    if "client" not in df.columns:
        df["client"] = ""
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df.sort_values("date").reset_index(drop=True)

def summarize(df):
    income = df.loc[df.type=="Income","amount_abs"].sum()
    expense = df.loc[df.type=="Expense","amount_abs"].sum()
    return {"revenue":float(income),"expenses":float(expense),"net_cashflow":float(income-expense)}
