import re
import tiktoken
from typing import List, Dict

encoder = tiktoken.get_encoding("cl100k_base")


def split_sentences(text: str) -> List[str]:
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]


def chunk_text(
    text: str,
    chunk_size: int = 120,
    overlap: int = 80,
) -> List[str]:

    sentences = split_sentences(text)

    chunks = []
    current_chunk = []
    current_tokens = 0

    for sentence in sentences:
        tokens = len(encoder.encode(sentence))

        # 1文が大きすぎる場合
        if tokens > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_tokens = 0

            chunks.append(sentence)
            continue

        # 上限超えそうならflush
        if current_tokens + tokens > chunk_size:
            chunks.append(" ".join(current_chunk))

            # overlap（直前2文残す）
            current_chunk = current_chunk[-2:] if len(current_chunk) > 2 else current_chunk
            current_tokens = sum(len(encoder.encode(s)) for s in current_chunk)

        current_chunk.append(sentence)
        current_tokens += tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def article_to_chunks(article: Dict) -> List[Dict]:
    """
    DB記事 → Chroma用chunkへ変換
    """

    content = article.get("content") or ""
    chunks = chunk_text(content)

    results = []

    for index, chunk in enumerate(chunks):
        results.append({
            "id": f"{article['id']}_chunk_{index}",
            "document": chunk,
            "metadata": {
                "article_id": article["id"],
                "chunk_index": index,
                "source": article.get("source"),
                "published_at": article.get("published_at"),
            }
        })

    return results