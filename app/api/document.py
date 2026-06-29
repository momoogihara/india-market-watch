from fastapi import APIRouter

from app.schemas.document import DocumentRequest, DocumentResponse
from app.services.document_service import index_document

router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
def create_document(request: DocumentRequest):

    article = index_document(request)

    return DocumentResponse(
        id=article.id,
        message="Document indexed successfully"
    )