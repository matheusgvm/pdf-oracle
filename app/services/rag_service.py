import requests
from app.core.config import settings


class RAGService:
    def __init__(self):
        self.api_url = settings.RAG_API_URL

    def upload_document(self, text: str) -> dict:
        response = requests.post(f"{self.api_url}/upload/", json={"text": text, "chunk_size": settings.CHUNK_SIZE,
                                                                  "chunk_overlap": settings.CHUNK_OVERLAP})
        if response.status_code != 200:
            raise Exception(f"Error uploading document: {response.text}")
        return response.json()

    def retrieve_chunks(self, query: str) -> list[str]:
        response = requests.get(f"{self.api_url}/query/", params={"q": query})
        if response.status_code != 200:
            raise Exception(f"Error retrieving chunks: {response.text}")
        return response.json()
