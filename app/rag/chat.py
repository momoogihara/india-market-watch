"""
chat.py

RAG chat pipeline.

This module receives a user's question,
retrieves the most relevant articles from the Vector DB,
and generates an AI answer using OpenAI.

Flow:
Question
    ↓
Embedding
    ↓
Vector Search
    ↓
Relevant Articles
    ↓
GPT Response
"""
from openai import OpenAI
import os
from app.rag.vectorstore import search
from app.rag.qa import build_prompt

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat(query: str):
    docs = search(query)

    context = "\n\n".join(docs)

    prompt = f"""
You are an India market analyst AI.

Use the following news context to answer:

{context}

Question:
{query}

Answer in structured format:
- Summary
- Key Insights
- Market Impact
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "answer": res.choices[0].message.content,
        "sources": docs
    }


def ask(question: str):

    prompt = build_prompt(question)

    response = client.chat.completions.create(
        model="gpt-5.5",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful financial analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
