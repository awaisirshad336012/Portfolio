def generate_insights(df, summary, anomalies, forecast):
    out=[]
    if summary["revenue"]:
        ratio=summary["expenses"]/summary["revenue"]
        out.append(f"Expense-to-income ratio is {ratio:.0%}.")
        if ratio>.8: out.append("⚠️ Expenses are consuming most recorded income; review recurring costs.")
        elif ratio<.5: out.append("✅ Expense load is relatively low compared with recorded income.")
    exp=df[df.type=="Expense"]
    if not exp.empty:
        top=exp.groupby("category").amount_abs.sum().sort_values(ascending=False)
        out.append(f"Top expense category is **{top.index[0]}**, representing {top.iloc[0]/top.sum():.0%} of expenses.")
    if not anomalies.empty: out.append(f"🚨 {len(anomalies)} transaction(s) deserve review due to unusual amounts.")
    if not forecast.empty:
        out.append("📈 Baseline forecast is positive on average." if forecast.predicted_net.mean()>=0 else "⚠️ Baseline forecast is negative on average.")
    return out or ["Add more transaction history for deeper insights."]

def cost_optimization(df):
    exp=df[df.type=="Expense"]
    if exp.empty: return ["No expenses found."]
    g=exp.groupby("category").amount_abs.sum().sort_values(ascending=False)
    total=g.sum()
    out=[f"Review **{g.index[0]}** first; it represents {g.iloc[0]/total:.0%} of recorded expenses."]
    recurring=exp.groupby("description").amount_abs.agg(["count","mean"]).query("count >= 2").sort_values("mean",ascending=False)
    if not recurring.empty: out.append(f"Review recurring item **{recurring.index[0]}** (average {recurring.iloc[0]['mean']:.0f} per transaction).")
    return out
