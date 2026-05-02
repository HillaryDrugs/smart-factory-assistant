"""
retriever.py
------------
Thin wrapper around the ChromaDB collection created by ingest_docs.py.
Exposes a single function: retrieve_context(query, top_k).

Designed to fail gracefully — if the DB has not been built yet,
it returns an empty list instead of crashing the pipeline.
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

DB_DIR = Path(__file__).resolve().parent.parent / "chroma_store"
COLLECTION_NAME = "machine_knowledge"
EMBED_MODEL = "all-MiniLM-L6-v2"

# Cache the client + collection so we don't re-load the embedding model on
# every call. Initialized lazily on first use.
_collection = None


def _get_collection():
    global _collection
    if _collection is not None:
        return _collection

    if not DB_DIR.exists():
        return None

    try:
        client = chromadb.PersistentClient(path=str(DB_DIR))
        embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL
        )
        _collection = client.get_collection(
            name=COLLECTION_NAME, embedding_function=embed_fn
        )
        return _collection
    except Exception as e:
        print(f"[retriever] could not load collection: {e}")
        return None


def retrieve_context(query: str, top_k: int = 3):
    """
    Retrieve the top_k most relevant chunks for a query.

    Args:
        query: natural-language search string
        top_k: number of chunks to return

    Returns:
        list of dicts: [{"text": ..., "source": ..., "score": ...}, ...]
        Empty list if the DB is missing or the query yields nothing.
    """
    collection = _get_collection()
    if collection is None:
        return []

    try:
        results = collection.query(query_texts=[query], n_results=top_k)
    except Exception as e:
        print(f"[retriever] query failed: {e}")
        return []

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    output = []
    for text, meta, dist in zip(docs, metas, dists):
        output.append({
            "text": text,
            "source": meta.get("source", "unknown") if meta else "unknown",
            "score": round(1 - float(dist), 3),  # rough similarity score
        })
    return output
