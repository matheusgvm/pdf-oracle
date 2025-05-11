from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    S3_BUCKET_NAME: str = "pdf-oracle"
    S3_PREFIX: str = "documents/"
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

settings = Settings()
