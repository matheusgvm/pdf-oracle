import requests
from app.core.config import settings


class RAGService:
    def __init__(self):
        self.api_url = settings.RAG_API_URL

    def upload_document(self, text: str) -> dict:
        """
        Uploads a document's text to the RAG API for chunking and indexing.

        Args:
            text (str): The document text to upload.

        Returns:
            dict: The response JSON from the API.

        Raises:
            requests.HTTPError: If the upload fails.
        """
        payload = {
            "text": text,
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
        }
        response = requests.post(f"{self.api_url}/upload/", json=payload)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(f"Error uploading document: {response.text}") from e
        return response.json()

    def retrieve_chunks(self, query: str) -> dict:
        """
        Retrieves relevant chunks for a query from the RAG API.

        Args:
            query (str): The query string.

        Returns:
            dict: The response JSON containing retrieved chunks.

        Raises:
            requests.HTTPError: If retrieval fails.
        """
        response = requests.get(f"{self.api_url}/query/", params={"q": query})
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(f"Error retrieving chunks: {response.text}") from e
        return response.json()
