"""
vectorstore.py

Vector Database operations.

This module manages the ChromaDB collection,
including:

- Add documents
- Store embeddings
- Similarity search
- Retrieve relevant documents
"""
import chromadb
from app.rag.embedding import get_embedding

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="india_news")


def add_document(doc_id: str, text: str, metadata: dict = None):
    embedding = get_embedding(text)

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )


# vector DB専用ファイル
from datetime import datetime, timedelta

def search(query_embedding, top_k: int = 5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=30,   # ← 少し多めに取得
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    output = []

    cutoff = datetime.now() - timedelta(days=30)

    for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):

        published_at = meta.get("published_at")

        if published_at:
            try:
                published_at = datetime.fromisoformat(
                    published_at.replace(" ", "T")
                )
            except Exception:
                continue
            if published_at < cutoff:
                continue
        output.append({
            "text": doc,
            "metadata": {
                **meta,
                "vector_distance": distance,
                "vector_score": 1 / (1 + distance)
            }
        })
    return output[:top_k]

#ChromaDBをリセットする機能
def reset_collection():
    """
    ChromaDBのコレクションを削除して再作成する。
    Phase2への移行時に一度だけ使用する。
    """
    global collection

    try:
        client.delete_collection("india_news")
    except Exception:
        pass

    collection = client.get_or_create_collection(name="india_news")

# def keyword_search(query: str, limit: int = 20):
#     sql = """
#     SELECT content, metadata
#     FROM chunks
#     WHERE content ILIKE %s
#     LIMIT %s
#     """

#     return db.execute(sql, (f"%{query}%", limit)).fetchall()
