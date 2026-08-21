# LedgerIQ — AI-Powered Financial Intelligence

LedgerIQ turns raw business transactions into financial intelligence.

## Product workflow

CSV → Validation/Cleaning → Smart Categorization → Analytics → Duplicate Review → Anomaly/Risk Detection → Budgets → Recurring Expenses → Cashflow Forecast → Cost Optimization → AI CFO → Reports

## Features

- Premium dark fintech dashboard
- CSV upload
- Data validation and duplicate cleanup
- Automatic category inference
- Revenue, expenses and net cashflow KPIs
- Monthly trend analysis
- Expense/category analytics
- Client profitability when a `client` column is supplied
- Recurring expense detection
- Exact duplicate candidates
- Isolation Forest anomaly detection
- Review-oriented risk scoring
- Budget monitoring
- 7–90 day baseline cashflow forecasting
- Cost optimization recommendations
- AI CFO with OpenRouter-compatible endpoint
- CSV and text report export

## CSV schema

Required:
`date, description, amount`

Optional:
`category, client, type`

Positive `amount` = income. Negative `amount` = expense.

## Run

```powershell
cd "C:\Users\awais\OneDrive\Documents\My-projects\LedgerIQ_AI"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then use **Load demo data** or upload your own CSV.

## AI

Copy `.env.example` to `.env`, set `OPENROUTER_API_KEY`, and configure your environment so the app can read the variables. The app works without an API key using a local fallback.

## Important product language

LedgerIQ detects anomalies and risk signals; it does **not** prove fraud and is not financial advice.
