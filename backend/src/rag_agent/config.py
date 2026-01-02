from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")
    qdrant_api_key: str = Field(..., validation_alias="QDRANT_API_KEY")
    qdrant_url: str = Field(..., validation_alias="QDRANT_URL")
    qdrant_collection_name: str = Field(default="book_embeddings", validation_alias="QDRANT_COLLECTION_NAME")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    max_chunk_size: int = Field(default=1000, validation_alias="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, validation_alias="CHUNK_OVERLAP")

    model_config = {"env_file": ".env", "case_sensitive": True}


# Create a singleton instance of settings
settings = Settings()