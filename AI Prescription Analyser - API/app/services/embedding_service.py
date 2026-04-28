from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import get_settings


settings = get_settings()


@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )