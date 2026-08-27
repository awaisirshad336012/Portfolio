"""
document_loader.py
-------------------
Documents (PDF ya TXT) ko load karta hai aur unhe chhote, overlapping
chunks mein todta hai taake embeddings behtar aur precise banein.
"""

import os
from pypdf import PdfReader


def load_document_text(file_path: str) -> str:
    """
    Ek file (PDF ya TXT) se poora text nikal kar return karta hai.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            # Har page ka marker rakhte hain taake baad mein source
            # citation (kaunse page se jawab aya) diya ja sake.
            text += f"\n\n[PAGE {page_num}]\n{page_text}"
        return text

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file type: {ext}. Sirf .pdf aur .txt supported hain.")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[dict]:
    """
    Lambe text ko chhote chunks mein todta hai, thoda overlap ke sath
    taake context na toote (ek sentence do chunks mein na bat jaye
    bina context ke).

    Returns: list of dicts -> {"text": chunk, "page": page_number}
    """
    chunks = []
    current_page = 1

    # Page markers ke hisab se text ko split karte hain taake har
    # chunk ke sath uska sahi page number attach rahe.
    segments = text.split("[PAGE ")
    if len(segments) == 1:
        # TXT file jisme page markers nahi hain
        segments = [text]

    for segment in segments:
        if not segment.strip():
            continue

        page_num = current_page
        if "]" in segment[:6]:
            try:
                page_num = int(segment.split("]")[0])
                segment = segment.split("]", 1)[1]
            except (ValueError, IndexError):
                pass

        current_page = page_num
        words = segment.split()

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_str = " ".join(chunk_words).strip()

            if len(chunk_str) > 30:  # bohat chhote/khali chunks skip karo
                chunks.append({"text": chunk_str, "page": page_num})

            start += chunk_size - overlap  # overlap ke sath aage badho

    return chunks
