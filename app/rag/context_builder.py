def build_context(chunks: list[dict]) -> str:
    context = ""

    for i, c in enumerate(chunks, 1):
        meta = c.get("metadata", {})

        title = meta.get("title", "No Title")
        date = meta.get("published_at", "Unknown Date")
        source = meta.get("source", "unknown")

        context += f"""
[{i}]
Title: {title}
Date: {date}
Source: {source}

Content:
{c['text']}
----------------------
"""

    return context