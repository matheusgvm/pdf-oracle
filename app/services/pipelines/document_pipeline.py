from typing import List
from fastapi import UploadFile
import uuid

from app.services.upload_file_service import UploadFileService
from app.services.pdf_text_extractor_service import PdfTextExtractorService

class DocumentPipeline:
    async def process_upload(self, files: List[UploadFile]) -> dict:
        documents_indexed = 0
        total_chunks = 0

        for file in files:
            file_id = str(uuid.uuid4())

            # Save file in s3
            file_content = await file.read()

            upload_file_service = UploadFileService()
            document_path = upload_file_service.upload_file_to_s3(file_id, file_content)

            # Extract text from PDF
            pdf_text_extractor_service = PdfTextExtractorService()
            text = pdf_text_extractor_service.text_extract(file.filename, file_content, file.content_type)
            print(text)

            # Chunk + Embeddings
            # chunks = chunking_utils.split(text)
            # embedding_service.index_chunks(file_id, chunks)

            documents_indexed += 1
            total_chunks += 64  # Placeholder

        return {
            "documents_indexed": documents_indexed,
            "total_chunks": total_chunks
        }