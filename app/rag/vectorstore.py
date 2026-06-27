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


def search(query: str, k: int = 5):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )

    docs = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        docs.append({
            "text": document,
            "metadata": metadata,
        })

    return docs
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