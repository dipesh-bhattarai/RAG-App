from fastapi import FastAPI

from ingestion.pipeline import ingest_pdf

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