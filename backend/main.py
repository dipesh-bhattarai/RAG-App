from fastapi import FastAPI

from ingestion.chunker import chunk_pdf

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