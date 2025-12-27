"""
Text Processing Module for RAG Ingestion Pipeline

Normalizes and chunks text content for embedding optimization.
"""
import hashlib
from typing import List
from src.extraction.content_extraction import Document


class TextChunk:
    def __init__(self, document_id: str, document_url: str, content: str,
                 heading: str = "", section: str = "", position: int = 0):
        self.id = f"{document_id}_chunk_{position}"
        self.document_id = document_id
        self.document_url = document_url
        self.content = content
        self.heading = heading
        self.section = section
        self.position = position
        self.hash = hashlib.md5(content.encode()).hexdigest()


def chunk_content(document: Document, max_chunk_size: int = 1000) -> List[TextChunk]:
    """
    Split document content into appropriately sized chunks.

    Args:
        document (Document): Document object to chunk
        max_chunk_size (int): Maximum size of each chunk in characters

    Returns:
        List[TextChunk]: List of TextChunk objects
    """
    content = document.content
    chunks = []
    position = 0

    # Simple approach: split by sentences while respecting max_chunk_size
    sentences = content.split('. ')
    current_chunk = ""
    current_heading = ""

    # Use first heading as default if available
    if document.headings:
        current_heading = document.headings[0]

    for i, sentence in enumerate(sentences):
        # Add sentence to current chunk
        potential_chunk = current_chunk + ". " + sentence if current_chunk else sentence

        # If adding this sentence would exceed the limit
        if len(potential_chunk) > max_chunk_size and current_chunk:
            # Save the current chunk
            chunks.append(TextChunk(
                document_id=document.id,
                document_url=document.url,
                content=current_chunk,
                heading=current_heading,
                position=position
            ))
            position += 1

            # Start new chunk with this sentence
            current_chunk = sentence
        else:
            # Add sentence to current chunk
            current_chunk = potential_chunk

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(TextChunk(
            document_id=document.id,
            document_url=document.url,
            content=current_chunk,
            heading=current_heading,
            position=position
        ))

    return chunks