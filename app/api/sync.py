from fastapi import APIRouter
from app.services.sync_service import sync_rss_to_vector

router = APIRouter()

@router.post("/sync")
def sync():
    return sync_rss_to_vector()