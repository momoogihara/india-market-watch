from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services import market_report_service
from app.services.report_service import generate_ai_market_report

from typing import List
from app.schemas import MarketReportResponse

router = APIRouter()

# =========================
# ① レポート生成 + 保存
# =========================
@router.get("/market-report/generate")
def generate_report(db: Session = Depends(get_db)):

    report = generate_ai_market_report(db)

    market_report_service.save_report(db, report)

    return report

# =========================
# ② 履歴取得
# =========================
@router.get("/market-report/history", response_model=List[MarketReportResponse])
def get_history(limit: int = 20, db: Session = Depends(get_db)):

    return market_report_service.fetch_reports(db, limit)