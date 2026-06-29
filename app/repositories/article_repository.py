from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models import Article
from app.schemas import ArticleCreate


# =========================
# BASIC CRUD
# =========================

def get_all(db: Session):
    return db.query(Article).all()


def create(db: Session, article):
    db_article = Article(
        title=article.get("title"),
        content=article.get("content"),
        source=article.get("source"),
        source_url=article.get("source_url"),
        published_at=article.get("published_at"),
    )

    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article

def get_by_title(db: Session, title: str):
    return (
        db.query(Article)
        .filter(Article.title == title)
        .first()
    )


def get_by_url(db: Session, url: str):
    return (
        db.query(Article)
        .filter(Article.source_url == url)
        .first()
    )


# =========================
# UPDATE FUNCTIONS
# =========================

def update_summary(db: Session, article_id: int, summary: str):
    article = db.query(Article).filter(Article.id == article_id).first()

    if article:
        article.ai_summary = summary
        db.commit()
        db.refresh(article)

    return article


def update_category(db: Session, article_id: int, category: str):
    article = db.query(Article).filter(Article.id == article_id).first()

    if article:
        article.category = category
        db.commit()
        db.refresh(article)

    return article


def update_sentiment(db: Session, article_id: int, sentiment: str):
    article = db.query(Article).filter(Article.id == article_id).first()

    if article:
        article.sentiment = sentiment
        db.commit()
        db.refresh(article)

    return article


def update_all_fields(db: Session, article_id: int, summary, sentiment, sector):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        return None

    article.ai_summary = summary or ""
    article.sentiment = sentiment or "Neutral"
    article.sector = sector or "Other"

    db.commit()
    db.refresh(article)

    return article


# =========================
# QUERY FUNCTIONS
# =========================

def get_articles_without_category(db: Session):
    return (
        db.query(Article)
        .filter(Article.category == None)
        .all()
    )


def get_articles_since(db: Session, days: int):
    cutoff = datetime.utcnow() - timedelta(days=days)

    return (
        db.query(Article)
        .filter(Article.created_at >= cutoff)
        .all()
    )


# =========================
# ANALYTICS
# =========================

def get_sector_sentiment_stats(db: Session):
    results = (
        db.query(
            Article.sector,
            Article.sentiment,
            func.count(Article.id).label("count")
        )
        .group_by(
            Article.sector,
            Article.sentiment
        )
        .all()
    )

    return [
        {
            "sector": row.sector,
            "sentiment": row.sentiment,
            "count": row.count
        }
        for row in results
    ]

def get_by_url(db, url: str):
    return (
        db.query(Article)
        .filter(Article.source_url == url)
        .first()
    )

# from sqlalchemy.orm import Session

# from app.models import Article
# from app.schemas import ArticleCreate

# from sqlalchemy import func

# from datetime import datetime
# from datetime import timedelta


# # from app.models import Article
# # from app.db import SessionLocal

# def get_all(db: Session):
#     return db.query(Article).all()


# def create(db: Session, article: ArticleCreate):
#     db_article = Article(
#         title=article.title,
#         content=article.content,
#         source=article.source, 
#         source_url=article.source_url,
#         published_at=article.published_at
#     )

#     db.add(db_article)
#     db.commit()
#     db.refresh(db_article)

#     return db_article

# def get_by_title(db: Session, title: str):
#     return (
#         db.query(Article)
#         .filter(Article.title == title)
#         .first()
#     )

# def get_by_url(db, url):
#     return (
#         db.query(Article)
#         .filter(Article.source_url == url)
#         .first()
#     )
# def update_summary(db: Session, article_id: int, summary: str):

#     article = (
#         db.query(Article)
#         .filter(Article.id == article_id)
#         .first()
#     )

#     if article:
#         article.ai_summary = summary
#         db.commit()
#         db.refresh(article)

#     return article

# def update_category(
#     db: Session,
#     article_id: int,
#     category: str
# ):
#     article = db.query(Article).filter(
#         Article.id == article_id
#     ).first()

#     if article:
#         article.category = category
#         db.commit()
#         db.refresh(article)

#     return article

# def get_articles_without_category(
#     db: Session
# ):
#     return (
#         db.query(Article)
#         .filter(Article.category == None)
#         .all()
#     )

# def update_sentiment(db, article_id: int, sentiment: str):
#     article = db.query(Article).filter(Article.id == article_id).first()

#     if article:
#         article.sentiment = sentiment
#         db.commit()
#         db.refresh(article)

#     return article

# def update_all_fields(db, article_id, summary, sentiment, sector):

#     article = (
#         db.query(Article)
#         .filter(Article.id == article_id)
#         .first()
#     )

#     if not article:
#         return None

#     article.ai_summary = summary or ""
#     article.sentiment = sentiment or "Neutral"
#     article.sector = sector or "Other"

#     db.commit()
#     db.refresh(article)

#     return article

# #集計用関数DAY16
# def get_sector_sentiment_stats(db):
#     """
#     Sector × Sentiment の件数集計
#     """

#     results = (
#         db.query(
#             Article.sector,
#             Article.sentiment,
#             func.count(Article.id).label("count")
#         )
#         .group_by(
#             Article.sector,
#             Article.sentiment
#         )
#         .all()
#     )

#     return [
#         {
#             "sector": row.sector,
#             "sentiment": row.sentiment,
#             "count": row.count
#         }
#         for row in results
#     ]

# #全期間集計を期日管理する
# def get_articles_since(db, days):

#     cutoff = datetime.utcnow() - timedelta(days=days)

#     return (
#         db.query(Article)
#         .filter(
#             Article.created_at >= cutoff
#         )
#         .all()
#     )


# #phase2_RAG同期
# class ArticleRepository:
#     def __init__(self, db):
#             self.db = db

#     def get_all_articles(self):
#             return self.db.query(Article).all()
    
# # #関数ベースに統一
# # def create_article(title, content, source=None, source_url=None):
# #     db = SessionLocal()

# #     article = Article(
# #         title=title,
# #         content=content,
# #         source=source,
# #         source_url=source_url,
# #     )

# #     db.add(article)
# #     db.commit()
# #     db.refresh(article)
# #     db.close()

# #     return article


# # def update_article(article_id: int, update_data: dict):
# #     db = SessionLocal()

# #     article = db.query(Article).filter(Article.id == article_id).first()

# #     if not article:
# #         db.close()
# #         return None

# #     for k, v in update_data.items():
# #         setattr(article, k, v)

# #     db.commit()
# #     db.refresh(article)
# #     db.close()

# #     return article