from datetime import datetime
from typing import Any

from pydantic import BaseModel


class MarketReportResponse(BaseModel):
    id: int
    created_at: datetime
    report_text: Any

    class Config:
        from_attributes = True