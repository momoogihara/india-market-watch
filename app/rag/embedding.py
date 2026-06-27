"""
embedding.py

Generate OpenAI embeddings.

This module converts text into embedding vectors,
which are used for semantic similarity search
inside the Vector Database.
"""
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return res.data[0].embedding