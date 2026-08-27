"""
app.py
------
RAG Document Q&A System - Streamlit dashboard.
User document upload karta hai, system usse "padh" leta hai, aur phir
user document ke bare mein sawal poochta hai — jawab hamesha document
ke andar se hi aata hai, source citation ke sath.
"""

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from modules.document_loader import load_document_text, chunk_text
from modules.vector_store import VectorStore
from modules.rag_brain import RAGBrain

load_dotenv()

st.set_page_config(page_title="InsightDoc", page_icon="📄", layout="wide")


# ---------- Session state setup ----------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()

if "rag_brain" not in st.session_state:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    st.session_state.rag_brain = RAGBrain(api_key=api_key) if api_key else None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []


# ---------- Sidebar: API key + document upload ----------
with st.sidebar:
    st.title("📄 InsightDoc")
    st.caption("Apne documents se seedha baat karein.")

    st.divider()

    # API key check
    if not os.environ.get("OPENROUTER_API_KEY"):
        st.warning("OPENROUTER_API_KEY set nahi hai.")
        manual_key = st.text_input("OpenRouter API key dalein:", type="password")
        if manual_key:
            os.environ["OPENROUTER_API_KEY"] = manual_key
            st.session_state.rag_brain = RAGBrain(api_key=manual_key)
            st.success("API key set ho gayi!")

    st.divider()
    st.subheader("📤 Document Upload")

    uploaded_files = st.file_uploader(
        "PDF ya TXT files upload karein",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )

    if uploaded_files and st.button("Process Documents", use_container_width=True):
        with st.spinner("Documents padhe ja rahe hain aur samjhe ja rahe hain..."):
            for uploaded_file in uploaded_files:
                if uploaded_file.name in st.session_state.processed_files:
                    continue

                # Temp file mein save karo taake loader use kar sake
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    tmp_path = tmp.name

                text = load_document_text(tmp_path)
                chunks = chunk_text(text)
                st.session_state.vector_store.add_chunks(chunks, source_name=uploaded_file.name)
                st.session_state.processed_files.append(uploaded_file.name)

                os.unlink(tmp_path)

        st.success(f"{len(uploaded_files)} document(s) process ho gaye!")

    if st.session_state.processed_files:
        st.divider()
        st.subheader("✅ Processed Documents")
        for fname in st.session_state.processed_files:
            st.text(f"• {fname}")

        st.caption(f"Total chunks stored: {st.session_state.vector_store.document_count()}")

        if st.button("🗑️ Sab Clear Karein", use_container_width=True):
            st.session_state.vector_store.clear()
            st.session_state.processed_files = []
            st.session_state.chat_history = []
            st.rerun()


# ---------- Main area: Chat interface ----------
st.header("💬 Apne Documents Se Sawal Poochein")

if not st.session_state.processed_files:
    st.info("👈 Pehle sidebar se koi document upload aur process karein.")
else:
    # Purani chat history dikhao
    for entry in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(entry["question"])
        with st.chat_message("assistant"):
            st.write(entry["answer"])
            if entry["sources"]:
                st.caption("📌 Sources: " + ", ".join(entry["sources"]))

    # Naya question input
    question = st.chat_input("Apna sawal yahan likhein...")

    if question:
        if st.session_state.rag_brain is None:
            st.error("Pehle sidebar mein OpenRouter API key dalein.")
        else:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Document mein dhoond raha hun..."):
                    retrieved = st.session_state.vector_store.search(question, top_k=4)
                    result = st.session_state.rag_brain.answer_question(question, retrieved)

                st.write(result["answer"])
                if result["sources"]:
                    st.caption("📌 Sources: " + ", ".join(result["sources"]))

            st.session_state.chat_history.append({
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"],
            })
