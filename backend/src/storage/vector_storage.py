"""
Vector Storage Module for RAG Ingestion Pipeline

Stores embeddings in Qdrant with associated metadata.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List
from src.embedding.embedding_generator import Embedding
from src.config.settings import Settings
import logging
import uuid


def store_vectors(embeddings: List[Embedding]) -> bool:
    """
    Store embeddings in Qdrant with metadata.

    Args:
        embeddings (List[Embedding]): List of Embedding objects to store

    Returns:
        bool: Success status
    """
    try:
        # Initialize Qdrant client
        client = QdrantClient(
            url=Settings.QDRANT_URL,
            api_key=Settings.QDRANT_API_KEY,
        )

        # Create collection if it doesn't exist
        try:
            client.get_collection(Settings.COLLECTION_NAME)
        except:
            # Collection doesn't exist, create it
            client.create_collection(
                collection_name=Settings.COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=len(embeddings[0].vector) if embeddings else 1024,  # Default size if no embeddings
                    distance=models.Distance.COSINE
                )
            )

        # Prepare points for insertion
        points = []
        for embedding in embeddings:
            # Get the associated chunk to extract metadata
            # For simplicity, we'll extract document URL from chunk_id which has format "doc_url_chunk_pos"
            doc_url_parts = embedding.chunk_id.split("_chunk_")
            doc_url = doc_url_parts[0] if doc_url_parts else "unknown"

            point = models.PointStruct(
                id=str(uuid.uuid4()),  # Generate unique ID
                vector=embedding.vector,
                payload={
                    "chunk_id": embedding.chunk_id,
                    "document_url": doc_url,
                    "model": embedding.model,
                    "model_version": embedding.model_version,
                    "content_preview": embedding.chunk_id[:200]  # First 200 chars as preview
                }
            )
            points.append(point)

        # Upload points to collection
        client.upsert(
            collection_name=Settings.COLLECTION_NAME,
            points=points
        )

        logging.info(f"Successfully stored {len(points)} vectors in Qdrant")
        return True

    except Exception as e:
        logging.error(f"Error storing vectors in Qdrant: {e}")
        return False