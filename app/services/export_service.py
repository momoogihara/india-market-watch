import os
import pandas as pd

from app.models import Article


def export_articles_csv(db):

    articles = db.query(Article).all()

    data = []

    for a in articles:

        data.append({
            "id": a.id,
            "title": a.title,
            "source": a.source,
            "sector": a.sector,
            "sentiment": a.sentiment,
            "published_at": a.published_at,
            "created_at": a.created_at
        })

    df = pd.DataFrame(data)

    os.makedirs("exports", exist_ok=True)

    file_path = "exports/articles.csv"

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )

    return file_path