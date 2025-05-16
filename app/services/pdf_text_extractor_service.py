import fitz  # pymupdf is imported as fitz
import requests
from app.core.config import settings


class PdfTextExtractorService:
    """
    Service to extract text from PDF files.
    Tries local extraction first; if empty, falls back to OCR service.
    """

    def text_extract(self, file_name: str, file_content: bytes, file_content_type: str) -> str | None:
        """
        Extract text from a PDF either locally or via an OCR API.

        Args:
            file_name (str): The name of the file.
            file_content (bytes): The PDF file content.
            file_content_type (str): The content type of the file.

        Returns:
            Optional[str]: Extracted text or None if extraction fails.
        """
        local_text = self._extract_text_locally(file_content)

        if local_text:
            return local_text
        return self._extract_text_by_ocr_service(file_name, file_content, file_content_type)

    def _extract_text_locally(self, file_content: bytes) -> str | None:
        """
        Extract text locally using pymupdf.

        Args:
            file_content (bytes): PDF file content.

        Returns:
            Optional[str]: Extracted text or None if empty.
        """
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text = "".join(page.get_text().strip() for page in doc)
            return text if text else None
        except Exception as e:
            return None

    def _extract_text_by_ocr_service(self, file_name: str, file_content: bytes, file_content_type: str) -> str | None:
        """
        Extract text via external OCR service.

        Args:
            file_name (str): The name of the file.
            file_content (bytes): The PDF file content.
            file_content_type (str): The content type of the file.

        Returns:
            Optional[str]: Extracted text or None if extraction fails.
        """
        try:
            files = {'file': (file_name, file_content, file_content_type)}
            response = requests.post(f"{settings.OCR_API_URL}/ocr", files=files)
            response.raise_for_status()

            data = response.json()
            pages = data.get('pages', [])
            unified_text = '\n\n'.join(page.get('text', '') for page in pages)
            return unified_text if unified_text else None
        except (requests.RequestException, ValueError, KeyError):
            return None
