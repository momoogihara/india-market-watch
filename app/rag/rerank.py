from openai import OpenAI
import json
import re

client = OpenAI()


def safe_json_load(text: str):
    try:
        return json.loads(text)
    except Exception:
        # JSONだけ抜き出す
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return []

        return []


def rerank(query: str, chunks: list[dict]) -> list[dict]:
    """
    chunks:
      [
        {"text": "...", "metadata": {...}},
        ...
      ]
    """

    prompt = f"""
You are a search ranking system.

Task:
Rank documents by relevance to the query.

Return ONLY valid JSON array.

No markdown.
No explanation.
No extra text.

Format:
[
  {{"index": 0, "score": 0.0}}
]

Query:
{query}

Documents:
"""

    for i, c in enumerate(chunks):
        prompt += f"\n[{i}] {c['text']}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON generator. Output ONLY valid JSON. No explanation. No markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    rankings = safe_json_load(content)

    # fallback: JSON壊れてた場合
    if not rankings:
        return chunks[:5]

    # score順ソート
    ranked = sorted(rankings, key=lambda x: x.get("score", 0), reverse=True)

    # indexベースで再構築
    output = []
    for r in ranked:
        idx = r.get("index")
        if idx is None or idx >= len(chunks):
            continue
        output.append(chunks[idx])

    return output[:5]