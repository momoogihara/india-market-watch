from sqlalchemy.orm import Session
from app.repositories import market_report_repository
import json

def save_report(db, report_data: dict):
    clean_data = json.loads(json.dumps(report_data))
    return market_report_repository.create_report(db, clean_data)


def fetch_reports(db: Session, limit: int = 20):
    return market_report_repository.get_reports(db, limit)