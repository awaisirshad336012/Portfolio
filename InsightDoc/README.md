# 📄 InsightDoc — RAG-based Document Q&A System

Apne documents (PDF/TXT) upload karein aur unse plain language mein sawal poochein — jawab hamesha document ke andar se hi milega, source citation (file + page number) ke sath. Hallucination-free, accurate answers.

Ye project **Retrieval-Augmented Generation (RAG)** architecture par bana hai:

```
Documents → Chunking → Embeddings → Chroma Vector DB (storage)
                                          ↓
User Question → Embedding → Similarity Search → Relevant Chunks Retrieve
                                          ↓
          Retrieved Chunks + Question → Claude API → Final Answer (with sources)
```

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2, free, local) |
| Vector Database | ChromaDB (free, local, no cloud setup) |
| LLM | OpenRouter Free Models Router (100% free, no billing needed) |
| UI | Streamlit |
| Document Parsing | PyPDF |

---

## 📁 Project Structure

```
rag_qa_system/
├── app.py                      # Streamlit dashboard (main entry point)
├── modules/
│   ├── document_loader.py      # PDF/TXT loading + chunking
│   ├── vector_store.py         # Embeddings + Chroma storage/retrieval
│   └── rag_brain.py            # Claude API se answer generation
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Setup Guide (Step-by-Step)

### 1. Python environment banayein (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Dependencies install karein

```bash
pip install -r requirements.txt
```

> Note: `sentence-transformers` pehli baar chalne par embedding model (~80MB) download karega — internet chahiye hoga, sirf ek dafa.

### 3. API Key set karein (100% Free)

`.env.example` ko `.env` mein rename karein aur apni OpenRouter API key dalein:

```bash
cp .env.example .env
```

`.env` file mein:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
```

**Key kaise milegi (free, koi credit card nahi chahiye):**
1. [openrouter.ai](https://openrouter.ai) pe jayein, sign up karein
2. Right-top corner mein apni profile pe click karein → **Keys**
3. **Create Key** dabayein, naam dein, copy kar lein (`sk-or-v1-...` se start hoti hai)

Ye project `openrouter/free` model use karta hai — OpenRouter khud har request ke liye ek free model (Llama, Qwen, etc.) automatically select kar leta hai. Cost: **$0**.

> Agar `.env` set nahi karte, app khud sidebar mein key maang legi.
>
> Note: Free models ki speed/quality paid models jitni consistent nahi hoti, aur rate limits kam hoti hain (bohat zyada requests fast fast na bhejein).

### 4. App run karein

```bash
streamlit run app.py
```

Browser mein `http://localhost:8501` khul jayega.

---

## 💡 Kaise Use Karein

1. Sidebar mein PDF ya TXT files upload karein
2. "Process Documents" button dabayein — system document ko padh kar samajh lega
3. Chat box mein document ke bare mein koi bhi sawal poochein
4. Jawab ke sath dekhein ke wo kaunse document/page se aya hai

---

## 🧠 Kaam Kaise Karta Hai (Technical Overview)

1. **Chunking:** Document ko ~800-word chunks mein toda jata hai, 150-word overlap ke sath (taake context na toote)
2. **Embeddings:** Har chunk `all-MiniLM-L6-v2` model se ek vector (numbers ki list) mein convert hota hai jo uska "meaning" represent karta hai
3. **Storage:** Ye vectors Chroma mein source file aur page number ke metadata ke sath save hote hain
4. **Retrieval:** User ke question ka bhi embedding banta hai, aur Chroma sabse "meaning mein similar" top-4 chunks nikaal deta hai
5. **Generation:** Retrieved chunks + question Claude ko diye jate hain, jo sirf usi context ke andar se answer banata hai — agar jawab context mein na ho to saaf keh deta hai "nahi mila" (hallucination avoid)

---

## ⚙️ Customization Ideas (Future Features)

- [ ] Multiple document formats (DOCX, CSV) support
- [ ] Chat memory (previous questions ka context yaad rakhna)
- [ ] Multi-turn conversation with follow-up questions
- [ ] Highlight exact matching sentence in source, not just chunk
- [ ] Deploy on Streamlit Cloud for live demo link

---

## 📌 Portfolio Notes

Ye project **Enterprise AI OS** ka core RAG engine hai — GenAI, Vector Databases, aur LLM-based applications ki practical understanding demonstrate karta hai. Case study likhte waqt highlight karein:
- **Problem:** Lambe documents mein manually info dhoondna time-consuming hai
- **Solution:** Semantic search + LLM se instant, accurate, source-cited answers
- **Architecture:** Chunking → Embeddings → Vector DB → Retrieval → LLM Generation
- **Result:** Hallucination-free Q&A system jo kisi bhi document set par kaam karta hai
