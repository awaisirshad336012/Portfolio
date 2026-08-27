"""
rag_brain.py
------------
Retrieved chunks (context) aur user ke question ko LLM ko bhejta hai,
aur ek accurate, source-based answer generate karwata hai. Agar
document mein jawab na mile, model saaf keh deta hai "nahi mila"
(hallucination avoid karne ke liye).

OpenRouter (free models) use karta hai - koi cost nahi. OpenRouter ka
API OpenAI-compatible hai, isliye 'openai' python package se hi call
kar lete hain, bas base_url OpenRouter ka de dete hain.
"""

import os
from openai import OpenAI

SYSTEM_PROMPT = """Aap ek precise Document Q&A assistant hain. Aapko neeche kuch
document excerpts (context) diye jayenge, aur ek user question.

Rules:
1. Sirf diye gaye context ke andar se jawab dein - apni taraf se kuch mat banayein.
2. Agar context mein jawab nahi milta, saaf saaf keh dein: "Ye document mein
   ye information nahi mili."
3. Jawab ke sath, kaunse source/page se ye info aayi hai wo mention karein.
4. Jawab clear, concise aur direct hona chahiye.
5. User jis language (Urdu/English/Roman Urdu) mein poochay, usi mein jawab dein.
"""

# Free Models Router - OpenRouter khud har request ke liye best available
# free model (Llama, Qwen, etc.) automatically choose kar leta hai.
# Cost: $0.
DEFAULT_MODEL = "openrouter/free"


class RAGBrain:
    def __init__(self, api_key: str = None, model: str = DEFAULT_MODEL):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.environ.get("OPENROUTER_API_KEY"),
        )
        self.model = model

    def build_context(self, retrieved_chunks: list[dict]) -> str:
        """Retrieved chunks ko ek formatted context string mein convert karta hai."""
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, start=1):
            context_parts.append(
                f"[Excerpt {i} — Source: {chunk['source']}, Page: {chunk['page']}]\n{chunk['text']}"
            )
        return "\n\n".join(context_parts)

    def answer_question(self, question: str, retrieved_chunks: list[dict]) -> dict:
        """
        Question aur retrieved chunks lekar LLM se final answer
        generate karta hai. Returns answer text + sources used.
        """
        if not retrieved_chunks:
            return {
                "answer": "Koi relevant document mila hi nahi. Pehle koi document upload karein.",
                "sources": [],
            }

        context = self.build_context(retrieved_chunks)

        user_message = f"""Context (document excerpts):
{context}

Question: {question}

Upar diye gaye context ke hisab se is question ka jawab dein."""

        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )

        answer_text = response.choices[0].message.content or ""

        sources = list({f"{c['source']} (page {c['page']})" for c in retrieved_chunks})

        return {"answer": answer_text, "sources": sources}
