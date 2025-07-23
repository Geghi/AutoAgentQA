from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.rag import rag_pipeline
import logging
router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    """
    Receives a query, performs a RAG search, and returns the answer.
    """
    try:
        answer = rag_pipeline(request.query)
        return {"answer": answer}
    except Exception as e:
        logging.error(f"An Error has occured: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
