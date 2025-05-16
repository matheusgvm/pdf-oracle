from typing import List
from fastapi import UploadFile
import uuid

from app.services.upload_file_service import UploadFileService
from app.services.pdf_text_extractor_service import PdfTextExtractorService
from app.services.rag_service import RAGService
from app.utils.text_preprocessor import preprocess_text

class DocumentPipeline:
    async def process_upload(self, files: List[UploadFile]) -> dict:
        documents_indexed = 0
        total_chunks = 0

        for file in files:
            file_id = str(uuid.uuid4())

            file_content = await file.read()

            # Save file in s3
            upload_file_service = UploadFileService()
            upload_file_service.upload_file_to_s3(file_id, file_content)

            # Extract text from PDF
            pdf_text_extractor_service = PdfTextExtractorService()
            text = pdf_text_extractor_service.text_extract(file.filename, file_content, file.content_type)

            # Preprocess text
            text = preprocess_text(text)

            # Indexing
            rag_service = RAGService()
            response = rag_service.upload_document(text)

            documents_indexed += 1
            total_chunks += response["total_chunks"]

        return {
            "documents_indexed": documents_indexed,
            "total_chunks": total_chunks
        }