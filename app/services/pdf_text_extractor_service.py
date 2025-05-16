import pymupdf
from app.core.config import settings
import requests


class PdfTextExtractorService:
    def text_extract(self, ffile_name: str, file_content: bytes, file_content_type: str):
        local_text = self._extract_text_locally(file_content)

        if local_text:
            return local_text
        else:
            return self._extract_text_by_ocr_service(ffile_name, file_content, file_content_type)

    def _extract_text_locally(self, file_content: bytes):
        doc = pymupdf.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text().strip()

        return text if text else None

    def _extract_text_by_ocr_service(self, file_name: str, file_content: bytes, file_content_type: str):
            file = {'file': (file_name, file_content, file_content_type)}
            response = requests.post(settings.OCR_API_URL, files=file)

            pages = response.json()
            pages = pages['pages']
            unified_text = '\n\n'.join(page['text'] for page in pages)

            return unified_text if unified_text else None