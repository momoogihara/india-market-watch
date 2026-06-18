from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.dependencies import get_db
from app.services import market_report_service
from app.services.ppt_service import generate_sample_ppt
from app.services import report_service
from app.models import Article

from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(
    prefix="/ppt",
    tags=["PPT"]
)


@router.get("/download")
def download_ppt(
    db: Session = Depends(get_db)
):
    reports = market_report_service.fetch_reports(
        db,
        limit=1
    )
    
    ranking = report_service.get_top_sectors(db)
    sectors = [
        item["sector"]
        for item in ranking[:5]
    ]
    scores = [
        item["bullish_score"]
        for item in ranking[:5]
    ]

    ranking_text = ""
    for i, item in enumerate(ranking[:5], start=1):
        ranking_text += (
        f"{i}. {item['sector']} "
        f"({item['bullish_score']:+})\n"
    )
    if ranking:
        strongest_sector = ranking[0]["sector"]
        weakest_sector = ranking[-1]["sector"]
    else:
        strongest_sector = "N/A"
        weakest_sector = "N/A"

    if not reports:
        summary = "No report found."
    else:
        summary = reports[0].report_text["summary"]

    daily_report = report_service.generate_daily_report(
    db
    )

    bullish_count = daily_report["sentiment"]["Bullish"]
    bearish_count = daily_report["sentiment"]["Bearish"]
    neutral_count = daily_report["sentiment"]["Neutral"]

    if bullish_count > bearish_count:
        market_tone = "Bullish"
    elif bearish_count > bullish_count:
        market_tone = "Bearish"
    else:
        market_tone = "Neutral"
    
    total = max(daily_report["total_articles"], 1)

    bullish_pct = round(
        daily_report["sentiment"]["Bullish"] * 100 / total
    )

    bearish_pct = round(
        daily_report["sentiment"]["Bearish"] * 100 / total
    )

    neutral_pct = round(
        daily_report["sentiment"]["Neutral"] * 100 / total
    )


    coverage_text = f"""
    Total Articles : {total}
    Bullish : {daily_report['sentiment']['Bullish']} ({bullish_pct}%)
    Bearish : {daily_report['sentiment']['Bearish']} ({bearish_pct}%)
    Neutral : {daily_report['sentiment']['Neutral']} ({neutral_pct}%)
    """

    #Top News Headline用
    articles = (
    db.query(Article)
    .order_by(Article.created_at.desc())
    .limit(5)
    .all()
    )

    headline_text = ""

    for i, article in enumerate(articles, start=1):
        headline_text += (
            f"{i}. {article.title}\n\n"
        )

    file_path = generate_sample_ppt(
        summary,
        strongest_sector,
        weakest_sector,
        market_tone,
        ranking_text,
        coverage_text,
        sectors,
        scores,
        bullish_count,
        bearish_count,
        neutral_count,
        headline_text
    )

    return FileResponse(
        path=file_path,
        filename="india_market_watch.pptx",
        media_type=(
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    )