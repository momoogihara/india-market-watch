
from fastapi import HTTPException
from app.repositories import article_repository
from app.services.rss_service import fetch_articles_from_rss
from app.schemas import ArticleCreate
from app.services.ai_service import AIService
from app.models import Article
import json
import re

def get_articles(db):
    return article_repository.get_all(db)

def create_article(db,article):

    existing_article = article_repository.get_by_title(db, article.title)

    if existing_article:
        raise HTTPException(
            status_code=400,
            detail="Article title already exists"
        )
    existing_url = article_repository.get_by_url(
        db,
        article.source_url
    )

    if existing_url:
        raise HTTPException(
            status_code=400,
            detail="Article URL already exists"
        )
    
    return article_repository.create(
        db,
        article
    )


# Day8追加部分 RSS
def import_rss_articles(db):
    #失敗カウンタ
    saved_count = 0
    failed_count = 0
    
    articles = fetch_articles_from_rss()
    
    # 件数制限_指定件数に制御
    articles = articles[:100]
    #articles = fetch_articles_from_rss()
    
    saved_count = 0
    for a in articles:

        title = a.get("title")
        if not title or title.strip().lower() == "string":
            continue

        # URLが無い記事はスキップ
        if not a.get("source_url"):
            continue

        exists = article_repository.get_by_url(db,a["source_url"])

        if exists:
            print("SKIP EXISTS:", a["source_url"])
            continue
        
        article = article_repository.create(db, ArticleCreate(**a))
        
        #記事単位で例外処理
        try:
            #AI応答確認
            result = AIService.analyze_article(article.content)
            print("AI RESULT:", result)

            #JSON変換後
            data = AIService.safe_parse_ai_response(result)
            print("PARSED DATA:", data)

            # data = {
            #     "summary": data.get("summary", ""),
            #     "sentiment": data.get("sentiment", "Neutral"),
            #     "sector": data.get("sector", "Other")
            # }

            article_repository.update_all_fields(
                db,
                article.id,
                summary=data["summary"],
                sentiment=data["sentiment"],
                sector=data["sector"]
            )

            saved_count += 1

        except Exception as e:

            print("=" * 80)
            print("ARTICLE PROCESS ERROR")
            print("TITLE:", article.title)
            print("ERROR:", e)


            failed_count += 1

            continue

    return {
            "fetched": len(articles),
            "saved": saved_count,
            "failed": failed_count
        }
#[レポート用サービス(report_service.py)を新規作成したため不要]
# def generate_daily_report(db):

#     articles = (
#         db.query(Article)
#         .order_by(Article.created_at.desc())
#         .limit(50)
#         .all()
#     )
#     sentiment_count = {
#         "Bullish": 0,
#         "Bearish": 0,
#         "Neutral": 0
#     }

#     for a in articles:
#         if a.sentiment in sentiment_count:
#             sentiment_count[a.sentiment] += 1

#     if not articles:
#         return {"message": "No articles found"}

#     return {
#         "sentiment": sentiment_count,
#         "total_articles": len(articles),
#         "titles": [a.title for a in articles]
#     }

# #集計用関数DAY16
# def generate_market_trend(db):

#     stats = article_repository.get_sector_sentiment_stats(db)

#     sector_data = {}

#     for row in stats:

#         sector = row["sector"]
#         sentiment = row["sentiment"]
#         count = row["count"]

#         if sector not in sector_data:
#             sector_data[sector] = {
#                 "Bullish": 0,
#                 "Bearish": 0,
#                 "Neutral": 0
#             }

#         sector_data[sector][sentiment] = count

#     result = {}

#     for sector, values in sector_data.items():

#         bullish = values["Bullish"]
#         bearish = values["Bearish"]
#         neutral = values["Neutral"]

#         if bullish > bearish:
#             trend = "Bullish"

#         elif bearish > bullish:
#             trend = "Bearish"

#         else:
#             trend = "Neutral"

#         result[sector] = {
#             "trend": trend,
#             "bullish": bullish,
#             "bearish": bearish,
#             "neutral": neutral
#         }

#     return result



# def generate_sector_report(db):

#     articles = db.query(Article).all()

#     sector_map = {}

#     for a in articles:
#         sector = a.sector or "Other"
#         sentiment = a.sentiment or "Neutral"

#         if sector not in sector_map:
#             sector_map[sector] = {
#                 "Bullish": 0,
#                 "Bearish": 0,
#                 "Neutral": 0
#             }

#         if sentiment in sector_map[sector]:
#             sector_map[sector][sentiment] += 1

#     return {
#         "sectors": sector_map
#     }


#[補完処理のため不要]import時に100%埋まる/NULLが基本発生しない設計/APIとして呼ばれてない
# def generate_missing_categories(db):

#     articles = (
#         db.query(Article)
#         .filter(Article.category == None)
#         .all()
#     )

#     count = 0

#     for article in articles:
#         category = AIService.classify(article.content)
#         article_repository.update_category(db, article.id, category)
#         count += 1

#     return {"updated": count}

# def generate_missing_summaries(db):

#     articles = (
#         db.query(Article)
#         .filter(Article.ai_summary == None)
#         .all()
#     )

#     updated_count = 0

#     for article in articles:

#         summary = AIService.summarize(article.content)
#         category = AIService.classify(article.content)
#         article_repository.update_summary(db,article.id,summary)

#         updated_count += 1

#     return {
#         "updated": updated_count
#     }

# def generate_missing_sentiment(db):

#     articles = (
#         db.query(Article)
#         .filter(Article.sentiment == None)
#         .all()
#     )

#     count = 0

#     for article in articles:
#         sentiment = AIService.analyze_sentiment(article.content)
#         article_repository.update_sentiment(db, article.id, sentiment)
#         count += 1

#     return {"updated": count}