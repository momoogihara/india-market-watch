from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.schemas import ArticleResponse
from app.dependencies import get_db

from app.services import article_service
from app.services import report_service

router = APIRouter()


# =========================
# GET
# =========================

@router.get("", response_model=List[ArticleResponse])
def get_articles(db: Session = Depends(get_db)):
    return article_service.get_articles(db)


# =========================
# CREATE
# =========================

@router.post("", response_model=ArticleResponse)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return article_service.create_article(db, article)


# =========================
# RSS IMPORT
# =========================

@router.post("/import-rss")
def import_rss(db: Session = Depends(get_db)):
    return article_service.import_rss_articles(db)

# =========================
# daily-report
# =========================

@router.post("/daily-report")
def daily_report(db: Session = Depends(get_db)):
    return report_service.generate_daily_report(db)

@router.post("/sector-report")
def sector_report(db: Session = Depends(get_db)):
    return report_service.generate_sector_report(db)

# =========================
#集計用関数DAY16
# =========================

@router.get("/market-trends")
def market_trends(db: Session = Depends(get_db)):
    return report_service.generate_market_trend(db)

# =========================
#ランキングDAY16
# =========================
@router.get("/top-sectors")
def top_sectors(
    db: Session = Depends(get_db)
):
    return report_service.get_top_sectors(db)
# =========================
#全期間集計を期日管理DAY17
# =========================
@router.get("/market-snapshot")
def market_snapshot(
    db: Session = Depends(get_db)
):
    return report_service.get_market_snapshot(db)

# =========================
#AI市場サマリー生成機能DAY17
# =========================
# @router.get("/ai-market-report")
# def ai_market_report(
#     db: Session = Depends(get_db)
# ):
#     return report_service.generate_ai_market_report(db)

# # =========================
# # SUMMARY
# # =========================

# @router.post("/generate-summaries")
# def generate_summaries(db: Session = Depends(get_db)):
#     return article_service.generate_missing_summaries(db)


# # =========================
# # CATEGORY
# # =========================

# @router.post("/generate-categories")
# def generate_categories(db: Session = Depends(get_db)):
#     return article_service.generate_missing_categories(db)


# # =========================
# # SENTIMENT
# # =========================

# @router.post("/generate-sentiment")
# def generate_sentiment(db: Session = Depends(get_db)):
#     return article_service.generate_missing_sentiment(db)
