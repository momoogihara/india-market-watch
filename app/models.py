from sqlalchemy import Column, Integer, String, Text, DateTime ,func
from datetime import datetime
from app.db import Base
from sqlalchemy.dialects.postgresql import JSONB

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    content = Column(Text)

    source = Column(String)
    source_url = Column(String, unique=True)

    published_at = Column(DateTime)

    ai_summary = Column(Text, nullable=True)

    category = Column(String, nullable=True)

    sentiment = Column(String(20), nullable=True)

    sector = Column(String, index=True, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

# #レポート履歴保存用テーブル(day18追加)
class MarketReport(Base):
    __tablename__ = "market_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_text = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    