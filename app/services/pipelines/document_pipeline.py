from typing import List
from fastapi import UploadFile
import uuid

from app.services.upload_file_service import UploadFileService

class DocumentPipeline:
    async def process_upload(self, files: List[UploadFile]) -> dict:
        documents_indexed = 0
        total_chunks = 0

        for file in files:
            file_id = str(uuid.uuid4())

            # Save file in s3
            content = await file.read()
            upload_file_service = UploadFileService()
            upload_file_service.upload_file_to_s3(file_id, content)

            # Executa OCR se necessário
            # text = ocr_service.extract_text(file.content_type, content)

            # Chunk + Embeddings
            # chunks = chunking_utils.split(text)
            # embedding_service.index_chunks(file_id, chunks)

            documents_indexed += 1
            total_chunks += 64  # Placeholder

        return {
            "documents_indexed": documents_indexed,
            "total_chunks": total_chunks
        }