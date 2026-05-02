"""
ingest_docs.py
--------------
One-time ingestion script. Reads every .txt file from data/, splits the
content into small chunks, embeds them with sentence-transformers, and
stores them in a persistent ChromaDB collection.

Run once before launching the app:
    python -m rag.ingest_docs
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# --- Config -------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR = Path(__file__).resolve().parent.parent / "chroma_store"
COLLECTION_NAME = "machine_knowledge"
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 400        # characters per chunk
CHUNK_OVERLAP = 50      # characters of overlap


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Simple character-based splitter — no extra dependencies."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def ingest():
    print(f"[ingest] reading .txt files from: {DATA_DIR}")
    txt_files = sorted(DATA_DIR.glob("*.txt"))
    if not txt_files:
        print("[ingest] No .txt files found in data/. Add some and re-run.")
        return

    DB_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_DIR))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    # Recreate the collection so re-running ingestion gives a clean state.
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(
        name=COLLECTION_NAME, embedding_function=embed_fn
    )

    total_chunks = 0
    for path in txt_files:
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        if not chunks:
            continue

        ids = [f"{path.stem}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": path.name, "chunk_index": i} for i in range(len(chunks))]

        collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        total_chunks += len(chunks)
        print(f"[ingest] {path.name} -> {len(chunks)} chunks")

    print(f"[ingest] done. {total_chunks} chunks stored in {DB_DIR}")


if __name__ == "__main__":
    ingest()
