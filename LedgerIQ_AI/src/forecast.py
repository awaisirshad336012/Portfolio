import pandas as pd

def forecast_cashflow(df, horizon=30):
    daily = df.groupby("date")["amount"].sum()
    if daily.empty: return pd.DataFrame(columns=["date","predicted_net"])
    idx = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(idx, fill_value=0.0)
    recent = daily.tail(min(14,len(daily)))
    base = recent.mean()
    weekday = daily.groupby(daily.index.dayofweek).mean()
    global_mean = daily.mean()
    dates = pd.date_range(daily.index.max()+pd.Timedelta(days=1), periods=horizon)
    preds = [0.5*base + 0.5*weekday.get(d.dayofweek, global_mean) for d in dates]
    return pd.DataFrame({"date":dates,"predicted_net":preds})
