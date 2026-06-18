from sqlalchemy.orm import Session
from app.models import MarketReport
import json

def create_report(db, data: dict):

    report = MarketReport(
         report_text=data 
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def get_reports(db: Session, limit: int = 20):
    return (
        db.query(MarketReport)
        .order_by(MarketReport.created_at.desc())
        .limit(limit)
        .all()
    )