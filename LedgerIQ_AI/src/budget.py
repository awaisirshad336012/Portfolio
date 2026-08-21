import pandas as pd
DEFAULT_BUDGETS = {"Marketing":5000,"Software":2500,"Travel":2000,"Meals":1000,"Office":1500,"Infrastructure":3000,"Utilities":1200,"Payroll":15000,"Rent":5000}

def budget_status(df, budgets):
    rows=[]
    exp=df[df.type=="Expense"]
    spent=exp.groupby("category").amount_abs.sum()
    for cat,budget in budgets.items():
        s=float(spent.get(cat,0))
        rows.append({"category":cat,"budget":budget,"spent":s,"remaining":budget-s,"used_pct":s/budget if budget else 0,"status":"Over budget" if s>budget else "On track"})
    return pd.DataFrame(rows).sort_values("used_pct",ascending=False)
