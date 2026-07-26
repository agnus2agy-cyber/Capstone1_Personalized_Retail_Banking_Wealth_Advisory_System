from fastapi import APIRouter, UploadFile, File, HTTPException
from services.upload_service import upload_pdf

upload_router = APIRouter()


@upload_router.post("/query/v1/retail/upload")
async def upload_pdf_route(file: UploadFile = File(...)):
    """
    Upload a PDF and ingest it into the knowledge base.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    return await upload_pdf(file)