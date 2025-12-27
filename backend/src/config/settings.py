import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "https://example.github.io/")

    # Processing settings
    MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embed-multilingual-v3.0")

    # Qdrant settings
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "book_embeddings")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")