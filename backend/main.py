from fastapi import FastAPI

from api.upload import router as upload_router
from api.document import router as document_router
from api.chat import router as chat_router
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout
)

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "RAG API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


app.include_router(upload_router)
app.include_router(document_router)
app.include_router(chat_router)