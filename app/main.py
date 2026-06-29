from fastapi import FastAPI
from app.scheduler import start_scheduler
from app.routers.articles import router as article_router
from app.routers import market_report
from app.routers.ppt import router as ppt_router
#phese2
import sys
import os
from pydantic import BaseModel
from app.rag.chat import chat
from app.rag.vectorstore import add_document
from app.api.chat import router as chat_router
from app.api.document import router as document_router

from app.api.sync import router as sync_router
from app.api.search import router as search_router


app = FastAPI()

@app.on_event("startup")
def startup():
    start_scheduler()


app.include_router(article_router, prefix="/articles", tags=["Articles"])
app.include_router(market_report.router, tags=["Market Reports"])
app.include_router(ppt_router)
app.include_router(chat_router)
app.include_router(document_router)
app.include_router(sync_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {"message": "India Market Watch"}


# class ChatRequest(BaseModel):
#     query: str

# @app.post("/chat")
# def chat_endpoint(req: ChatRequest):
#     return chat(req.query)


# テスト用：ニュース投入
@app.post("/add")
def add_news(text: str, doc_id: str):
    add_document(doc_id, text, {"source": "manual"})
    return {"status": "added"}


# print("🔥 ACTIVE DB URL:", engine.url)