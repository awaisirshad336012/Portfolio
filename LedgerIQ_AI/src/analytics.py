import pandas as pd

def monthly_metrics(df):
    g = df.groupby(["month","type"])["amount_abs"].sum().unstack(fill_value=0)
    for col in ["Income","Expense"]:
        if col not in g: g[col] = 0
    out = g.rename(columns={"Income":"income","Expense":"expenses"})
    out["net"] = out["income"] - out["expenses"]
    return out.reset_index()

def category_metrics(df):
    return df.groupby(["category","type"])["amount_abs"].agg(["sum","count"]).reset_index().rename(columns={"sum":"amount_abs","count":"transactions"}).sort_values("amount_abs", ascending=False)

def recurring_expenses(df):
    x = df[df.type=="Expense"].copy()
    if x.empty: return pd.DataFrame(columns=["description","transactions","avg_amount","estimated_monthly"])
    g = x.groupby("description").agg(transactions=("description","size"), avg_amount=("amount_abs","mean"), last_date=("date","max"))
    g["estimated_monthly"] = g["avg_amount"] * g["transactions"] / max(df["month"].nunique(),1)
    return g[g["transactions"]>=2].reset_index().sort_values("estimated_monthly", ascending=False)

def client_profitability(df):
    x = df[df.client.astype(str).str.strip()!=""].copy()
    if x.empty: return pd.DataFrame()
    income = x[x.type=="Income"].groupby("client")["amount_abs"].sum()
    expense = x[x.type=="Expense"].groupby("client")["amount_abs"].sum()
    out = pd.DataFrame({"revenue":income,"cost":expense}).fillna(0)
    out["profit"] = out["revenue"] - out["cost"]
    return out.sort_values("profit", ascending=False).reset_index()
