"""
Main RAG Ingestion Pipeline

Orchestrates the full pipeline: URL discovery → Content extraction → Text processing →
Embedding generation → Vector storage
"""
import asyncio
import logging

from src.config.settings import Settings
from src.discovery.url_discovery import discover_urls
from src.extraction.content_extraction import extract_content
from src.processing.text_processing import chunk_content
from src.embedding.embedding_generator import generate_embeddings
from src.storage.vector_storage import store_vectors

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    """
    Main function to orchestrate the full RAG ingestion pipeline:
    1. Discover URLs from GitHub Pages site
    2. Extract content from each URL
    3. Process and chunk the content
    4. Generate embeddings using Cohere
    5. Store vectors in Qdrant
    """
    logger.info("Starting RAG ingestion pipeline")

    # Validate required settings
    if not Settings.COHERE_API_KEY:
        logger.error("COHERE_API_KEY environment variable is required")
        return
    if not Settings.QDRANT_URL:
        logger.error("QDRANT_URL environment variable is required")
        return
    if not Settings.GITHUB_PAGES_URL:
        logger.error("GITHUB_PAGES_URL environment variable is required")
        return

    # Step 1: Discover URLs
    logger.info(f"Discovering URLs from {Settings.GITHUB_PAGES_URL}")
    urls = discover_urls(Settings.GITHUB_PAGES_URL)
    logger.info(f"Discovered {len(urls)} URLs")

    # Process each URL through the pipeline
    processed_count = 0
    failed_count = 0

    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        try:
            # Step 2: Extract content
            logger.info(f"Extracting content from {url}")
            document = extract_content(url)

            # Step 3: Process and chunk content
            logger.info(f"Chunking content from {url}")
            text_chunks = chunk_content(document)

            # Step 4: Generate embeddings
            logger.info(f"Generating embeddings for {len(text_chunks)} chunks from {url}")
            embeddings = generate_embeddings(text_chunks)

            # Step 5: Store vectors
            logger.info(f"Storing {len(embeddings)} vectors for {url}")
            success = store_vectors(embeddings)

            if success:
                logger.info(f"Successfully processed and stored {url}")
                processed_count += 1
            else:
                logger.error(f"Failed to store vectors for {url}")
                failed_count += 1

        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            failed_count += 1
            continue

    logger.info(f"RAG ingestion pipeline completed. Processed: {processed_count}, Failed: {failed_count}")


if __name__ == "__main__":
    asyncio.run(main())