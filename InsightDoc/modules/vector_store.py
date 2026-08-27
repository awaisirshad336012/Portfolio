"""
vector_store.py
----------------
Chunks ko embeddings mein convert karta hai aur Chroma (local vector
database) mein store karta hai. Question aane par sabse relevant
chunks retrieve karta hai (meaning-based similarity search).
"""

import chromadb
from sentence_transformers import SentenceTransformer

# Free, chhota aur fast embedding model - local machine par chalta hai,
# koi API cost nahi.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


class VectorStore:
    def __init__(self, persist_dir: str = "./chroma_db", collection_name: str = "documents"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def add_chunks(self, chunks: list[dict], source_name: str):
        """
        Chunks ki list ko embed karke Chroma mein save karta hai.
        Har chunk ke sath source document ka naam aur page number
        metadata ke tor par save hota hai (citation ke liye zaroori).
        """
        if not chunks:
            return

        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.encode(texts, show_progress_bar=False).tolist()

        # Existing chunks count le lo taake IDs unique rahein (multiple
        # documents ek collection mein add ho sakein bina overwrite ke)
        existing_count = self.collection.count()

        ids = [f"{source_name}_{existing_count + i}" for i in range(len(chunks))]
        metadatas = [{"source": source_name, "page": c["page"]} for c in chunks]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        """
        Query se sabse similar chunks dhoond kar return karta hai,
        source aur page number ke sath (citation ke liye).
        """
        query_embedding = self.embedder.encode([query]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
        )

        retrieved = []
        if results["documents"] and results["documents"][0]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                retrieved.append({
                    "text": doc,
                    "source": meta.get("source", "unknown"),
                    "page": meta.get("page", "?"),
                })

        return retrieved

    def document_count(self) -> int:
        return self.collection.count()

    def clear(self):
        """Poori collection delete karke naya session shuru karta hai."""
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(name=self.collection.name)
