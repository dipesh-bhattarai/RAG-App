from fastapi import APIRouter
from pydantic import BaseModel

from rag.pipeline import rag_pipeline
from memory.history import get_history, add_message


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    session_id: str
    question: str


@router.post("/")
async def chat(request: ChatRequest):

    history = get_history(request.session_id)

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in history
    )

    result = rag_pipeline(
        question=request.question,
        history=history_text
    )

    add_message(
        request.session_id,
        "user",
        request.question
    )

    add_message(
        request.session_id,
        "assistant",
        result["answer"]
    )

    return result