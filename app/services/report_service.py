from app.repositories import article_repository
from app.models import Article
from app.services.ai_service import AIService
from app.services import market_report_service

def generate_daily_report(db):

    articles = (
        db.query(Article)
        .order_by(Article.created_at.desc())
        .limit(50)
        .all()
    )

    sentiment_count = {
        "Bullish": 0,
        "Bearish": 0,
        "Neutral": 0
    }

    for a in articles:
        if a.sentiment in sentiment_count:
            sentiment_count[a.sentiment] += 1

    if not articles:
        return {"message": "No articles found"}

    return {
        "sentiment": sentiment_count,
        "total_articles": len(articles),
        "titles": [a.title for a in articles]
    }

def generate_sector_report(db):

    articles = db.query(Article).all()

    sector_map = {}

    for a in articles:

        sector = a.sector or "Other"
        sentiment = a.sentiment or "Neutral"

        if sector not in sector_map:
            sector_map[sector] = {
                "Bullish": 0,
                "Bearish": 0,
                "Neutral": 0
            }

        if sentiment in sector_map[sector]:
            sector_map[sector][sentiment] += 1

    return {
        "sectors": sector_map
    }

def generate_market_trend(db):

    stats = article_repository.get_sector_sentiment_stats(db)

    sector_data = {}

    for row in stats:

        sector = row["sector"]
        sentiment = row["sentiment"]
        count = row["count"]

        if sector not in sector_data:
            sector_data[sector] = {
                "Bullish": 0,
                "Bearish": 0,
                "Neutral": 0
            }

        sector_data[sector][sentiment] = count

    result = {}

    for sector, values in sector_data.items():

        bullish = values["Bullish"]
        bearish = values["Bearish"]
        neutral = values["Neutral"]

        if bullish > bearish:
            trend = "Bullish"

        elif bearish > bullish:
            trend = "Bearish"

        else:
            trend = "Neutral"

        result[sector] = {
            "trend": trend,
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral
        }

    return result

def get_top_sectors(db):

    trends = generate_market_trend(db)

    ranking = []

    for sector, data in trends.items():

        if sector == "Other":
            continue

        score = (
            data["bullish"]
            - data["bearish"]
        )

        ranking.append({
            "sector": sector,
            "bullish_score": score,
            "bullish": data["bullish"],
            "bearish": data["bearish"]
        })

    ranking.sort(
        key=lambda x: x["bullish_score"],
        reverse=True
    )

    return ranking
#AI市場サマリー生成機能DAY17
def get_market_snapshot(db):

    return {
        "trends": generate_market_trend(db),
        "ranking": get_top_sectors(db)
    }

def generate_ai_market_report(db):

    snapshot = get_market_snapshot(db)

    articles = (
        db.query(Article)
        .order_by(Article.created_at.desc())
        .limit(10)
        .all()
    )

    news_summaries = [
        article.ai_summary
        for article in articles
        if article.ai_summary
    ]

    summary = AIService.generate_market_summary(
        snapshot,
        news_summaries
    )

    result = {
        "summary": summary,
        "snapshot": snapshot
    }

    return result