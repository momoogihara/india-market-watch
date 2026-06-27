from app.db import SessionLocal
from app.models import Article
from app.rag.vectorstore import add_document
from app.rag.chunk import article_to_chunks
from app.rag.vectorstore import search

def sync_all_articles_to_chroma():
    db = SessionLocal()

    articles = db.query(Article).filter(Article.embedded.is_(False)).all()
    print(f"🔥 total unembedded articles: {len(articles)}")

    count = 0
    for article in articles:
        try:
            print(f"processing: {article.id}")
            
            # # ✔ Chroma登録（1回だけ）
            # add_document(
            #     doc_id=str(article.id),
            #     text=article.content,
            #     metadata={
            #         "article_id": article.id,
            #         "source": "postgres",
            #         "published_at": str(article.published_at)
            #     }
            # )
            #add_document() をループ化
            chunks = article_to_chunks(
                {
                    "id": article.id,
                    "content": article.content,
                    "source": "postgres",
                    "published_at": str(article.published_at),
                }
            )
            print(f"  -> {len(chunks)} chunks")
            for chunk in chunks:
                add_document(
                    doc_id=chunk["id"],
                    text=chunk["document"],
                    metadata=chunk["metadata"],
                )

            # 全チャンク成功後
            article.embedded = True
            db.commit()

            count += 1
            
        except Exception as e:
            print(f"skip {article.id}: {e}")

    print(f"✅ synced: {count}")

    if __name__ == "__main__":
     sync_all_articles_to_chroma()
