from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from app.services.pipelines.document_pipeline import DocumentPipeline

router = APIRouter()

@router.post("/", summary="Upload PDF documents")
async def upload_documents(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    pipeline = DocumentPipeline()
    try:
        result = await pipeline.process_upload(files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    return {
        "message": "Documents processed successfully",
        "documents_indexed": result.get("documents_indexed", 0),
        "total_chunks": result.get("total_chunks", 0),
    }
