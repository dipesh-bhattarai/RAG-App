from pathlib import Path
from fastapi import APIRouter
from fastapi import FastAPI, File, HTTPException, UploadFile
from uuid import uuid4
from ingestion.pipeline import ingest_pdf

router = APIRouter(prefix='/upload', tags=["upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code = 400,
            detail = "Only PDF files are allowed"
        )

    filename = f"{uuid4()}.pdf"
    file_path = UPLOAD_DIR /filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = ingest_pdf(pdf_path= file_path)

    return {
        "message":"PDF uploaded successfully",
        "filename":file.filename,
        **result
    }