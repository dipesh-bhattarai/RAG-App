from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter(
    prefix="/document",
    tags=["Documents"]
)

@router.get("/")
async def get_documents():
    return {
        "message": "document router works"
    }

@router.delete("/{document_id}")
async def remove_document(document_id: str):
    return {
        "message": "delete works",
        "document_id": document_id
    }

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "RAG API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}