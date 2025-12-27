# Quickstart Guide: RAG Website URL Ingestion, Embedding Generation, and Vector Storage

**Feature**: 1-rag-ingestion
**Created**: 2025-12-27

## Prerequisites

- Python 3.9 or higher
- UV package manager
- Cohere API key
- Qdrant Cloud account and API key
- Access to target GitHub Pages site

## Setup

### 1. Clone and Navigate to Backend Directory
```bash
mkdir backend
cd backend
```

### 2. Initialize Python Project
```bash
uv init
```

### 3. Create Virtual Environment and Install Dependencies
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv loguru
```

### 4. Create Environment File
Create `.env` file in the backend directory:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
GITHUB_PAGES_URL=https://your-book.github.io/
LOG_LEVEL=INFO
```

## Project Structure
```
backend/
├── .env
├── .gitignore
├── main.py
├── requirements.txt  # if not using UV directly
├── config/
│   └── settings.py
├── src/
│   ├── __init__.py
│   ├── discovery/
│   │   ├── __init__.py
│   │   └── url_discovery.py
│   ├── extraction/
│   │   ├── __init__.py
│   │   └── content_extraction.py
│   ├── processing/
│   │   ├── __init__.py
│   │   └── text_processing.py
│   ├── embedding/
│   │   ├── __init__.py
│   │   └── embedding_generator.py
│   └── storage/
│       ├── __init__.py
│       └── vector_storage.py
```

## Configuration

### Settings Configuration (`config/settings.py`)
```python
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
```

## Running the Pipeline

### 1. Create Main Pipeline File (`main.py`)
```python
import asyncio
import logging
from loguru import logger

from config.settings import Settings
from src.discovery.url_discovery import discover_urls
from src.extraction.content_extraction import extract_content
from src.processing.text_processing import chunk_content
from src.embedding.embedding_generator import generate_embeddings
from src.storage.vector_storage import store_vectors

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

    # Step 1: Discover URLs
    logger.info(f"Discovering URLs from {Settings.GITHUB_PAGES_URL}")
    urls = discover_urls(Settings.GITHUB_PAGES_URL)
    logger.info(f"Discovered {len(urls)} URLs")

    # Step 2-5: Process each URL through the pipeline
    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        try:
            # Extract content
            document = extract_content(url)

            # Process and chunk content
            text_chunks = chunk_content(document)

            # Generate embeddings
            embeddings = generate_embeddings(text_chunks)

            # Store vectors
            success = store_vectors(embeddings)

            if success:
                logger.info(f"Successfully processed and stored {url}")
            else:
                logger.error(f"Failed to store vectors for {url}")

        except Exception as e:
            logger.error(f"Error processing {url}: {str(e)}")
            continue

    logger.info("RAG ingestion pipeline completed")

if __name__ == "__main__":
    asyncio.run(main())
```

## Running the Application

### 1. Execute the Pipeline
```bash
cd backend
python main.py
```

### 2. Monitor the Process
- Check console output for progress logs
- Verify embeddings are stored in Qdrant
- Review any error messages in the logs

## Verification Steps

### 1. Check URL Discovery
- Verify all expected pages were discovered
- Check that no broken links were processed

### 2. Verify Content Extraction
- Confirm text content is clean (no HTML tags)
- Verify metadata (headings, sections) is preserved

### 3. Validate Embeddings
- Check that embeddings have consistent dimensions
- Verify successful storage in Qdrant

### 4. Test Retrieval
- Perform test queries to verify semantic relevance
- Confirm vector counts match expected values

## Troubleshooting

### Common Issues

**API Rate Limits**:
- Implement exponential backoff in your embedding function
- Add delays between API calls if needed

**Large Pages**:
- Content chunking will automatically handle large pages
- Monitor memory usage during processing

**Network Issues**:
- The pipeline includes retry logic for network requests
- Check internet connectivity and URL accessibility

### Environment Variables
Ensure all required environment variables are set in your `.env` file before running.

## Next Steps

1. After successful setup, consider adding:
   - Progress tracking and checkpointing
   - Parallel processing for faster ingestion
   - More sophisticated error handling and recovery
   - Integration with FastAPI for API access