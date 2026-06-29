from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat_api(request: ChatRequest):
    answer = chat(request.query)

    return ChatResponse(answer=answer)