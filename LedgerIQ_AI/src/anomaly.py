import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    if len(df) < 10:
        return pd.DataFrame(columns=list(df.columns)+["anomaly_score"])
    model = IsolationForest(n_estimators=250, contamination="auto", random_state=42)
    x = df[["amount_abs"]].astype(float)
    labels = model.fit_predict(x)
    scores = -model.score_samples(x)
    out = df.copy()
    out["anomaly_score"] = scores
    out["is_anomaly"] = labels == -1
    threshold = out.anomaly_score.quantile(.90)
    return out[(out.is_anomaly) | (out.anomaly_score >= threshold)].sort_values("anomaly_score", ascending=False)

def risk_score(row):
    score = float(min(100, max(0, row.get("anomaly_score",0)*100)))
    amount = float(row.get("amount_abs",0))
    if amount > 5000: score = min(100, score+15)
    return round(score)
