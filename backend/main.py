from fastapi import FastAPI, APIRouter

from db.qdrant import delete_document

app = FastAPI()

router = APIRouter(
    prefix="/document",
    tags=["Documents"]
)


@router.delete("/{document_id}")
async def remove_document(document_id: str):

    delete_document(document_id)

    return {
        "message": "Document deleted"
    }


app.include_router(router)


@app.get("/")
async def root():
    return {"message": "RAG API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}