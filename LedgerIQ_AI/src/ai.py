import os, json, urllib.request

def generate_ai_cfo(df, summary, insights, optimization, question):
    key=os.getenv("OPENROUTER_API_KEY")
    model=os.getenv("OPENROUTER_MODEL","openai/gpt-4o-mini")
    context=f"""Revenue: {summary['revenue']:.2f}
Expenses: {summary['expenses']:.2f}
Net cashflow: {summary['net_cashflow']:.2f}
Insights: {insights}
Optimization suggestions: {optimization}
User question: {question}"""
    if not key:
        return "**Local CFO fallback**\n\n" + "\n".join("- "+x for x in insights+optimization) + "\n\nSet OPENROUTER_API_KEY to enable LLM answers."
    payload=json.dumps({"model":model,"messages":[{"role":"system","content":"You are LedgerIQ's concise financial intelligence assistant. Do not claim fraud or give regulated financial advice. Use only supplied facts."},{"role":"user","content":context}],"temperature":.2}).encode()
    req=urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=payload,headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"},method="POST")
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI provider unavailable: {e}\n\n" + "\n".join("- "+x for x in insights)
