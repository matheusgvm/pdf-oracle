from typing import List
from fastapi import UploadFile
import uuid

from app.services.upload_file_service import UploadFileService
from app.services.pdf_text_extractor_service import PdfTextExtractorService
from app.services.rag_service import RAGService
from app.utils.text_preprocessor import preprocess_text


class DocumentPipeline:
    """
    Pipeline to process uploaded PDF documents by saving them,
    extracting and preprocessing text, and indexing via RAG service.
    """

    def __init__(
        self,
        upload_service: UploadFileService = None,
        pdf_extractor_service: PdfTextExtractorService = None,
        rag_service: RAGService = None,
    ):
        """
        Initialize the DocumentPipeline with optional service dependencies.
        If services are not provided, default instances are created.

        Args:
            upload_service (UploadFileService, optional): Service to upload files to storage.
            pdf_extractor_service (PdfTextExtractorService, optional): Service to extract text from PDFs.
            rag_service (RAGService, optional): Service to index documents.
        """
        self.upload_service = upload_service or UploadFileService()
        self.pdf_extractor_service = pdf_extractor_service or PdfTextExtractorService()
        self.rag_service = rag_service or RAGService()

    async def process_upload(self, files: List[UploadFile]) -> dict:
        """
        Process a list of uploaded PDF files:
          - Save each file to S3.
          - Extract and preprocess text from each PDF.
          - Index the processed text using RAGService.

        Args:
            files (List[UploadFile]): List of PDF files to process.

        Returns:
            dict: Summary with total documents indexed and total chunks processed.
        """
        documents_indexed = 0
        total_chunks = 0

        for file in files:
            file_id = str(uuid.uuid4())
            file_content = await file.read()

            self.upload_service.upload_file_to_s3(file_id, file_content)

            text = self.pdf_extractor_service.text_extract(file.filename, file_content, file.content_type)
            text = preprocess_text(text)

            response = self.rag_service.upload_document(text)

            documents_indexed += 1
            total_chunks += response.get("total_chunks", 0)

        return {
            "documents_indexed": documents_indexed,
            "total_chunks": total_chunks,
        }
