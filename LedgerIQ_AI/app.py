from pathlib import Path
import pandas as pd
import streamlit as st

from src.pipeline import prepare_transactions, summarize
from src.analytics import monthly_metrics, category_metrics, recurring_expenses, client_profitability
from src.anomaly import detect_anomalies, risk_score
from src.forecast import forecast_cashflow
from src.insights import generate_insights, cost_optimization
from src.ai import generate_ai_cfo
from src.budget import budget_status, DEFAULT_BUDGETS

BASE_DIR = Path(__file__).resolve().parent
DEMO_DATA = BASE_DIR / "data" / "demo_transactions.csv"

st.set_page_config(page_title="LedgerIQ", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0b1120; }
[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1e293b; }
.block-container { padding-top: 2rem; max-width: 1400px; }
h1,h2,h3 { color: #f8fafc; }
.metric-card { background:#111827; border:1px solid #1e293b; padding:18px; border-radius:16px; }
.metric-label { color:#94a3b8; font-size:13px; }
.metric-value { color:#f8fafc; font-size:27px; font-weight:700; }
.small-muted { color:#94a3b8; }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# ◈ LedgerIQ")
st.sidebar.caption("AI-Powered Financial Intelligence")
page = st.sidebar.radio("Navigation", ["Dashboard", "Transactions", "Analytics", "Risk Center", "Forecast", "Budgets", "AI CFO", "Reports"])
st.sidebar.divider()
uploaded = st.sidebar.file_uploader("Upload transaction CSV", type=["csv"])

if st.sidebar.button("Load demo data", use_container_width=True):
    st.session_state["force_demo"] = True

def load_raw():
    if uploaded is not None:
        return pd.read_csv(uploaded)
    return pd.read_csv(DEMO_DATA)

try:
    raw = load_raw()
    df = prepare_transactions(raw)
except Exception as exc:
    st.error(f"Data could not be processed: {exc}")
    st.info("Required columns: date, description, amount. Optional: category, client, type.")
    st.stop()

summary = summarize(df)
monthly = monthly_metrics(df)
categories = category_metrics(df)
anomalies = detect_anomalies(df)
forecast = forecast_cashflow(df)
recurring = recurring_expenses(df)
clients = client_profitability(df)
insights = generate_insights(df, summary, anomalies, forecast)
optimization = cost_optimization(df)
budgets = budget_status(df, DEFAULT_BUDGETS)

def money(x):
    return f"${x:,.0f}"

def metric(label, value, help_text=""):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="small-muted">{help_text}</div></div>', unsafe_allow_html=True)

if page == "Dashboard":
    st.title("Good morning 👋")
    st.caption("Here's your current financial health.")
    cols = st.columns(4)
    with cols[0]: metric("Revenue", money(summary["revenue"]), "Recorded income")
    with cols[1]: metric("Expenses", money(summary["expenses"]), "Recorded spending")
    with cols[2]: metric("Net cashflow", money(summary["net_cashflow"]), "Revenue minus expenses")
    with cols[3]: metric("Transactions", f"{len(df):,}", "Cleaned records")
    st.subheader("Cashflow trend")
    st.line_chart(monthly.set_index("month")[["income", "expenses", "net"]])
    left, right = st.columns(2)
    with left:
        st.subheader("Expense breakdown")
        exp = categories[categories["type"] == "Expense"].set_index("category")["amount_abs"].sort_values(ascending=False)
        st.bar_chart(exp)
    with right:
        st.subheader("Attention required")
        for item in insights[:4]:
            st.markdown(f"- {item}")
    st.subheader("Top recurring expenses")
    st.dataframe(recurring.head(8), width="stretch", hide_index=True)

elif page == "Transactions":
    st.title("Transactions")
    q = st.text_input("Search description, client or category")
    category = st.selectbox("Category", ["All"] + sorted(df["category"].unique()))
    view = df.copy()
    if q:
        view = view[view.astype(str).apply(lambda c: c.str.contains(q, case=False, na=False)).any(axis=1)]
    if category != "All":
        view = view[view["category"] == category]
    st.dataframe(view, width="stretch", hide_index=True)
    st.download_button("Download cleaned CSV", view.to_csv(index=False), "ledgeriq_cleaned.csv", "text/csv")

elif page == "Analytics":
    st.title("Analytics")
    st.subheader("Monthly performance")
    st.dataframe(monthly, width="stretch", hide_index=True)
    st.line_chart(monthly.set_index("month")[["income", "expenses", "net"]])
    st.subheader("Category analysis")
    st.dataframe(categories, width="stretch", hide_index=True)
    st.subheader("Client profitability")
    if clients.empty:
        st.info("Add a 'client' column to analyze client profitability.")
    else:
        st.dataframe(clients, width="stretch", hide_index=True)

elif page == "Risk Center":
    st.title("Risk Center")
    st.caption("Risk scores identify transactions worth reviewing. They do not prove fraud.")

    if anomalies.empty:
        st.success("No strong anomalies detected.")
    else:
        display = anomalies.copy()
        display["risk_score"] = display.apply(risk_score, axis=1)
        display["risk_level"] = pd.cut(display["risk_score"], [-1, 39, 69, 100], labels=["Low", "Medium", "High"])
        st.dataframe(display, width="stretch", hide_index=True)

    st.subheader("Duplicate candidates")
    dup = df[
        df.duplicated(subset=["date", "description", "amount"], keep=False)
    ].sort_values(["date", "description", "amount"])

    # FIX: use a normal if/else block instead of a bare conditional expression.
    # This prevents Streamlit from rendering DeltaGenerator documentation.
    if not dup.empty:
        st.dataframe(dup, width="stretch", hide_index=True)
    else:
        st.success("No exact duplicate candidates found.")

elif page == "Forecast":
    st.title("Cashflow Forecast")
    horizon = st.slider("Forecast horizon (days)", 7, 90, 30)
    fc = forecast_cashflow(df, horizon)
    if fc.empty:
        st.info("Not enough transaction history to generate a forecast.")
    else:
        st.line_chart(fc.set_index("date")[["predicted_net"]])
        st.dataframe(fc, width="stretch", hide_index=True)
        avg = fc["predicted_net"].mean()
        if avg >= 0:
            st.success(f"Baseline predicted average daily net cashflow: {money(avg)}")
        else:
            st.warning(f"Baseline predicted average daily net cashflow: {money(avg)}")

elif page == "Budgets":
    st.title("Budget Monitor")
    st.caption("Edit budgets in the source configuration for persistent defaults.")
    b = budgets.copy()
    st.dataframe(b, width="stretch", hide_index=True)
    for _, row in b.iterrows():
        pct = min(max(row["used_pct"], 0), 1)
        st.write(f"**{row['category']}** — {money(row['spent'])} / {money(row['budget'])}")
        st.progress(pct)

elif page == "AI CFO":
    st.title("✦ AI CFO")
    st.caption("Ask for an executive interpretation of the financial data.")
    question = st.text_area("Ask a question", "Why did expenses increase, what is my biggest risk, and where can I reduce costs?")
    if st.button("Analyze with AI CFO", type="primary"):
        with st.spinner("Preparing financial context..."):
            answer = generate_ai_cfo(df, summary, insights, optimization, question)
        st.markdown(answer)
    st.divider()
    st.subheader("Rule-based recommendations")
    for item in optimization:
        st.markdown(f"- {item}")

elif page == "Reports":
    st.title("Executive Financial Report")
    st.caption("A decision-ready overview of your financial performance, risks, and opportunities.")

    forecast_average = float(forecast["predicted_net"].mean()) if not forecast.empty else 0
    expense_ratio = (summary["expenses"] / summary["revenue"] * 100) if summary["revenue"] else 0

    # Executive KPI cards
    st.subheader("Financial Overview")
    cols = st.columns(5)
    with cols[0]:
        metric("Revenue", money(summary["revenue"]), "Total recorded income")
    with cols[1]:
        metric("Expenses", money(summary["expenses"]), "Total recorded spending")
    with cols[2]:
        metric("Net Cashflow", money(summary["net_cashflow"]), "Revenue minus expenses")
    with cols[3]:
        metric("Expense Ratio", f"{expense_ratio:.0f}%", "Expenses as % of revenue")
    with cols[4]:
        metric("Anomalies", f"{len(anomalies):,}", "Transactions requiring review")

    st.divider()

    # Performance charts
    left, right = st.columns(2)
    with left:
        st.subheader("Cashflow Trend")
        st.line_chart(monthly.set_index("month")[["income", "expenses", "net"]])
    with right:
        st.subheader("Expense Breakdown")
        exp = categories[categories["type"] == "Expense"].set_index("category")["amount_abs"].sort_values(ascending=False)
        if not exp.empty:
            st.bar_chart(exp)
        else:
            st.info("No expense categories available.")

    st.divider()

    # AI / rule-based insights
    left, right = st.columns(2)
    with left:
        st.subheader("✦ AI Financial Insights")
        if insights:
            for item in insights:
                st.markdown(f"- {item}")
        else:
            st.info("No insights available yet.")

    with right:
        st.subheader("Cost Optimization")
        if optimization:
            for item in optimization:
                st.markdown(f"- {item}")
        else:
            st.success("No immediate cost optimization recommendations.")

    st.divider()

    # Forecast and anomaly summary
    left, right = st.columns(2)
    with left:
        st.subheader("Cashflow Forecast")
        if not forecast.empty:
            forecast_chart = forecast.set_index("date")[["predicted_net"]]
            st.line_chart(forecast_chart)
            if forecast_average >= 0:
                st.success(f"Positive baseline forecast: {money(forecast_average)} average daily net cashflow")
            else:
                st.warning(f"Negative baseline forecast: {money(forecast_average)} average daily net cashflow")
        else:
            st.info("Not enough history to generate a forecast.")

    with right:
        st.subheader("Risk Summary")
        if anomalies.empty:
            st.success("No strong anomalies detected.")
        else:
            st.warning(f"{len(anomalies):,} transaction(s) require review for unusual activity.")
            display = anomalies.copy()
            display["risk_score"] = display.apply(risk_score, axis=1)
            display["risk_level"] = pd.cut(display["risk_score"], [-1, 39, 69, 100], labels=["Low", "Medium", "High"])
            st.dataframe(display.head(10), width="stretch", hide_index=True)

    st.divider()

    st.subheader("Top Recurring Expenses")
    if recurring.empty:
        st.info("No recurring expenses detected.")
    else:
        st.dataframe(recurring.head(8), width="stretch", hide_index=True)

    st.divider()

    # Export section
    st.subheader("Export Report")
    executive_summary = [
        "LEDGERIQ — EXECUTIVE FINANCIAL REPORT",
        "",
        f"Revenue: {money(summary['revenue'])}",
        f"Expenses: {money(summary['expenses'])}",
        f"Net Cashflow: {money(summary['net_cashflow'])}",
        f"Expense Ratio: {expense_ratio:.1f}%",
        f"Anomalies: {len(anomalies)}",
        f"Forecast Average Daily Net Cashflow: {money(forecast_average)}",
        "",
        "AI FINANCIAL INSIGHTS",
        *[f"- {item}" for item in insights],
        "",
        "COST OPTIMIZATION",
        *[f"- {item}" for item in optimization],
    ]

    export_cols = st.columns(2)
    with export_cols[0]:
        st.download_button(
            "Export Transactions",
            df.to_csv(index=False),
            "ledgeriq_report_data.csv",
            "text/csv",
            use_container_width=True,
        )
    with export_cols[1]:
        st.download_button(
            "Export Executive Summary",
            "\n".join(executive_summary),
            "ledgeriq_executive_summary.txt",
            "text/plain",
            use_container_width=True,
        )
