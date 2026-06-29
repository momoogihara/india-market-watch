from app.repositories.article_repository import create, update_all_fields
from app.rag.chunk import chunk_text
from app.rag.embedding import get_embedding
from app.rag.vectorstore import add_document


def index_document(db, data):
    # 1. DB保存
    article = create(db, data)

    # 2. chunk化
    chunks = chunk_text(data.content)

    # 3. embedding + vectorstore登録
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        add_document(
            doc_id=article.id,
            chunk_index=i,
            text=chunk,
            embedding=embedding,
        )

    # 4. embeddedフラグ更新（修正済み関数使用）
    update_all_fields(
        db,
        article.id,
        summary=article.ai_summary,
        sentiment=article.sentiment,
        sector=article.sector
    )

    return article