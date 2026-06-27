from app.rag.vectorstore import search

def build_context(query: str, k: int = 5):
    docs = search(query, k)

    context = ""

    for i, doc in enumerate(docs, start=1):
        context += f"[Document {i}]\n"
        context += doc["text"]
        context += "\n\n"

    return context

def build_prompt(question: str):

    context = build_context(question)

    return f"""
You are an expert news analyst.

Answer the user's question only using the context below.

Context:

{context}

Question:
{question}

Answer:
"""