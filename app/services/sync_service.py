from app.db import SessionLocal
from app.repositories.article_repository import get_by_url, create
from app.services.rss_service import fetch_articles_from_rss


def sync_rss_to_vector():
    db = SessionLocal()

    articles = fetch_articles_from_rss()

    inserted = 0
    skipped = 0

    for a in articles:
        # 重複チェック（超重要）
        exists = get_by_url(db, a["source_url"])

        if exists:
            skipped += 1
            continue

        create(db, a)
        inserted += 1

    db.close()

    return {
        "inserted": inserted,
        "skipped": skipped,
        "total": len(articles)
    }