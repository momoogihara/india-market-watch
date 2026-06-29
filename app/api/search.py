from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embedding import get_embedding
from app.rag.vectorstore import search as vector_search
from app.rag.rerank import rerank
from app.rag.context_builder import build_context
from app.rag.scoring import apply_hybrid_score
from app.services.ai_service import AIService

from sqlalchemy import text
from app.db import engine

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
async def search(req: SearchRequest):
    query = req.query

    # 1. embedding
    query_embedding = get_embedding(query)

    # 2. vector search
    vector_results = vector_search(query_embedding, top_k=10)
    #デバッグ用
    # for r in vector_results:
    #    print(r["metadata"])
    # 3. keyword search
    keyword_results = keyword_search(query, limit=30)

    # merge
    results = vector_results + keyword_results

    # Hybrid Score
    results = apply_hybrid_score(results)

    # 5. deduplicate
    results = deduplicate(results)

    # 6. rerank（重要）
    results = rerank(query, results)

    # 7. context build
    context = build_context(results)

    # 8. LLM answer
    answer = AIService.generate_answer(query=query, context=context)

    return {
        "answer": answer,
        "sources": results
    }
   

# def keyword_search(query: str, limit: int = 10):
#     sql = text("""
#         SELECT id, content
#         FROM articles
#         WHERE content ILIKE :q
#         LIMIT :limit
#     """)

#     with engine.connect() as conn:
#         result = conn.execute(sql, {
#             "q": f"%{query}%",
#             "limit": limit
#         })

#         rows = result.fetchall()

#     return [
#         {
#             "text": r.content,
#             "metadata": {
#                 "article_id": r.id
#             }
#         }
#         for r in rows
#     ]
def keyword_search(query: str, limit: int = 10):
    sql = text("""
        SELECT
            id,
            title,
            content,
            published_at,
            ts_rank(
                to_tsvector(
                    'english',
                    title || ' ' || coalesce(ai_summary, '') || ' ' || content
                ),
                plainto_tsquery('english', :query)
            ) AS rank
        FROM articles
        WHERE to_tsvector(
                'english',
                title || ' ' || coalesce(ai_summary, '') || ' ' || content
              )
              @@ plainto_tsquery('english', :query)
          AND published_at >= NOW() - INTERVAL '30 days'
        ORDER BY rank DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(
            sql,
            {
                "query": query,
                "limit": limit
            }
        )

        rows = result.fetchall()

    return [
        {
            "text": row.content,
            "metadata": {
                "article_id": row.id,
                "title": row.title,
                "published_at": row.published_at,
                "keyword_rank": float(row.rank)
            }
        }
        for row in rows
    ]

def deduplicate(results):
    seen = set()
    unique = []

    for r in results:
        key = r.get("metadata", {}).get("article_id")

        if key in seen:
            continue

        seen.add(key)
        unique.append(r)

    return unique

