from fastapi import FastAPI, APIRouter

from db.qdrant import list_document

app = FastAPI()

router = APIRouter(
    prefix="/document",
    tags=["Documents"]
)


@router.get("/")
async def get_documents():
    return list_document()


app.include_router(router)


@app.get("/")
async def root():
    return {"message": "RAG API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}