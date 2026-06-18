from fastapi import FastAPI
from app.scheduler import start_scheduler
from app.routers.articles import router as article_router
from app.routers import market_report
from app.routers.ppt import router as ppt_router


app = FastAPI()

@app.on_event("startup")
def startup():
    start_scheduler()


app.include_router(article_router, prefix="/articles", tags=["Articles"])
app.include_router(market_report.router, tags=["Market Reports"])
app.include_router(ppt_router)


@app.get("/")
def root():
    return {"message": "India Market Watch"}