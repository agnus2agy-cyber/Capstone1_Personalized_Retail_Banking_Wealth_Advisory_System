import os
import tempfile

from fastapi import UploadFile
from ingestion.ingestion import ingest_pdf


async def upload_pdf(file: UploadFile):

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(await file.read())
            temp_path = temp_file.name

        chunks = ingest_pdf(temp_path)

        return {
            "status": "success",
            "message": "PDF uploaded and indexed successfully.",
            "chunks_ingested": chunks
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)