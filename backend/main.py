from fastapi import FastAPI

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