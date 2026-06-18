from app.db import SessionLocal
from app.services.export_service import export_articles_csv

db = SessionLocal()

file_path = export_articles_csv(db)

print(f"CSV Exported : {file_path}")

db.close()