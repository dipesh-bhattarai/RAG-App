from fastapi import FastAPI

from ingestion.embedder import embed_text

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