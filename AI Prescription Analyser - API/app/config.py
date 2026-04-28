from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "AI Prescription Analyzer"
    APP_VERSION: str = "1.0.0"

    GROQ_API_KEY: str
    LLM_MODEL_NAME: str = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    TESSERACT_PATH: Optional[str] = None

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()