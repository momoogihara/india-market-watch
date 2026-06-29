from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentRequest(BaseModel):
    title: str
    content: str
    source: Optional[str] = None
    source_url: Optional[str] = None


class DocumentResponse(BaseModel):
    id: int
    message: str