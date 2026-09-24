from fastapi import APIRouter
from db.qdrant import (
    remove_document,
    list_documents
)

router = APIRouter(
    prefix = "/document",
    tags=["Documents"]
)


@router.get("/")
async def get_documents():
    return list_documents()


@router.delete("/{document_id}")
async def remove_document(
    document_id:str,
):
    remove_document(document_id)
    return {
        "message":"Document deleted"
    }
    