from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str | None = None
    source: str | None = None
    source_url: str | None = None
    published_at: datetime | None = None


class ArticleResponse(ArticleCreate):
    id: int

    ai_summary: str | None = None
    sentiment: Optional[str] = None
    sector: Optional[str] = None

    class Config:
        from_attributes = True