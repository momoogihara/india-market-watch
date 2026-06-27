from app.rag.chunk import chunk_text, article_to_chunks

text = """
Toyota announced a major investment in electric vehicles.
The company plans to build new battery factories in India.
Analysts expect strong growth in the EV market over the next decade.
""" * 50

# chunk_text() のテスト
chunks = chunk_text(text)
print(f"Number of chunks: {len(chunks)}")

# article_to_chunks() のテスト
article = {
    "id": 1,
    "content": text,
    "source": "rss",
    "published_at": "2026-06-23"
}

chunk_data = article_to_chunks(article)

print(f"Chunk records: {len(chunk_data)}")
print(chunk_data[0])