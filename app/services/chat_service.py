from app.rag.chat import ask


def chat(query: str) -> str:
    """
    Execute chat using the RAG engine.
    """
    return ask(query)