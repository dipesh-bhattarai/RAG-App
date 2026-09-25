from fastapi import FastAPI

from db.qdrant import list_document

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "RAG API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}