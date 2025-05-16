from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    S3_BUCKET_NAME: str = "pdf-oracle"
    S3_PREFIX: str = "documents/"
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    OCR_API_URL: str = "http://localhost:8000/ocr"
    RAG_API_URL: str = "http://localhost:8002/"

    GEMINI_API_KEY: str
    GEMINI_MODEL_ID: str = "gemini/gemini-2.0-flash"

    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 30

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

settings = Settings()
