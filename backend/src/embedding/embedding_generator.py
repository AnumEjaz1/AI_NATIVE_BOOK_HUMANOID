"""
Embedding Generation Module for RAG Ingestion Pipeline

Generates semantic embeddings using Cohere models.
"""
import cohere
from typing import List
from src.processing.text_processing import TextChunk
from src.config.settings import Settings
import logging


class Embedding:
    def __init__(self, chunk_id: str, vector: List[float], model: str, model_version: str, dimensions: int):
        self.id = f"emb_{chunk_id}"
        self.chunk_id = chunk_id
        self.vector = vector
        self.model = model
        self.model_version = model_version
        self.dimensions = dimensions


def generate_embeddings(chunks: List[TextChunk], model: str = Settings.EMBEDDING_MODEL) -> List[Embedding]:
    """
    Generate embeddings for text chunks using Cohere.

    Args:
        chunks (List[TextChunk]): List of TextChunk objects to embed
        model (str): Cohere embedding model to use

    Returns:
        List[Embedding]: List of Embedding objects
    """
    if not chunks:
        return []

    # Initialize Cohere client
    co = cohere.Client(Settings.COHERE_API_KEY)

    # Extract text content from chunks
    texts = [chunk.content for chunk in chunks]

    try:
        # Generate embeddings
        response = co.embed(
            texts=texts,
            model=model
        )

        embeddings = []
        for i, embedding_vector in enumerate(response.embeddings):
            chunk = chunks[i]
            embedding = Embedding(
                chunk_id=chunk.id,
                vector=embedding_vector,
                model=model,
                model_version=response.meta["api_version"]["version"],  # This might need adjustment
                dimensions=len(embedding_vector)
            )
            embeddings.append(embedding)

        logging.info(f"Generated {len(embeddings)} embeddings successfully")
        return embeddings

    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        raise