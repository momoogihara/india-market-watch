from pydantic import BaseModel
from datetime import datetime
#day9追加
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from typing import Any

# 作成用
class ArticleCreate(BaseModel):
    title: str
    content: str | None = None
    source: str | None = None
    source_url: str | None = None
    published_at: datetime | None = None
    
# レスポンス用
class ArticleResponse(ArticleCreate):
    id: int

    ai_summary: str | None = None
    sentiment: Optional[str] = None
    sector: Optional[str]

    class Config:
        from_attributes = True


#market-report/history用
class MarketReportResponse(BaseModel):

    id: int
    created_at: datetime
    report_text: Any

    class Config:
        from_attributes = True