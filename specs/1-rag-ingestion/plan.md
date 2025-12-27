# Implementation Plan: RAG Website URL Ingestion, Embedding Generation, and Vector Storage

**Feature**: 1-rag-ingestion
**Created**: 2025-12-27
**Status**: Draft
**Input**: RAG Spec-1: URL Ingestion & Vector Storage - Create the backend/ folder, initialize UV packages, and add a single main.py file. In main.py, implement ingestion starting with deployed website URL discovery. Extract and chunk normalized text content in a retrieval-optimized format. Generate embeddings using Cohere models and store vectors with metadata in Qdrant. Define a final main() function to orchestrate the full pipeline end-to-end.

## Technical Context

This implementation will create a Python-based ingestion pipeline for RAG (Retrieval-Augmented Generation) systems. The system will discover, extract, chunk, embed, and store Docusaurus book content from GitHub Pages.

**Key Components:**
- **URL Discovery**: Crawler to discover all pages from a GitHub Pages site
- **Content Extraction**: HTML parsing and text extraction with metadata preservation
- **Text Processing**: Normalization and chunking for embedding optimization
- **Embedding Generation**: Cohere API integration for semantic embeddings
- **Vector Storage**: Qdrant Cloud integration for vector storage and retrieval
- **Pipeline Orchestration**: Main function to coordinate the end-to-end process

**Technology Stack:**
- Language: Python
- Dependencies: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
- Package Manager: UV (for fast Python package management)
- Environment: Configuration via .env files

## Constitution Check

### Technical Accuracy & Validation
- All technical claims will reference official documentation for Cohere, Qdrant, and Docusaurus
- Code examples will be validated against actual APIs and tested for functionality

### Clarity & Accessibility
- Code will include clear comments explaining the purpose of each function
- Implementation will follow Python best practices and standard library conventions
- Error handling will provide clear, actionable messages

### Spec-First AI-Assisted Authoring
- Implementation will directly map to the functional requirements in the feature spec
- Each requirement (FR-001 through FR-012) will be addressed in the implementation

### Reproducibility
- Setup steps will be documented in a requirements file and quickstart guide
- Environment variables will be properly configured via .env files
- Code will be structured to run consistently across different environments

### Practical Implementation Focus
- Implementation will focus on minimal, functional code that addresses the core requirements
- Error handling will be included for common failure scenarios
- Logging will be implemented at each pipeline stage as required

### Architecture Decision Justification
- Architecture will follow a modular design with separate functions for each pipeline stage
- Cohere and Qdrant integration will use official Python SDKs
- Text processing will use established libraries for HTML parsing

## Gates

### Gate 1: Architecture Alignment
✅ **PASSED** - Architecture aligns with requirements to create an ingestion-only pipeline with URL discovery, content extraction, embedding generation, and vector storage

### Gate 2: Technology Feasibility
✅ **PASSED** - All required technologies (Cohere, Qdrant, web scraping) are available and well-documented

### Gate 3: Security & Compliance
✅ **PASSED** - Implementation will use proper environment variables for API keys and follow secure coding practices

## Phase 0: Research & Unknowns Resolution

### Research Tasks

1. **Cohere Embedding Models**: Research the most appropriate Cohere embedding model for text content
   - Decision: Use Cohere's latest embedding model optimized for text similarity
   - Rationale: Cohere embeddings are known for high-quality semantic representations
   - Alternatives considered: OpenAI embeddings, Hugging Face models

2. **Qdrant Vector Storage**: Research optimal schema for storing text chunks with metadata
   - Decision: Use Qdrant collections with structured payloads for metadata
   - Rationale: Qdrant provides efficient vector search with metadata filtering
   - Alternatives considered: Pinecone, Weaviate, Chroma

3. **Docusaurus Content Structure**: Research common HTML structure patterns in Docusaurus sites
   - Decision: Target main content areas using common Docusaurus CSS selectors
   - Rationale: Docusaurus sites follow predictable patterns that can be targeted efficiently
   - Alternatives considered: Generic web scraping approaches

4. **Text Chunking Strategy**: Research optimal chunk sizes for embedding generation
   - Decision: Use semantic chunking with overlap to preserve context
   - Rationale: Semantic chunks maintain meaning while fitting within model limits
   - Alternatives considered: Fixed-size character chunks, sentence-based chunks

### Risk Assessment
- **API Rate Limits**: Cohere and Qdrant APIs may have rate limits that need handling
- **Large Content**: Some pages may exceed embedding model input limits
- **Network Reliability**: GitHub Pages sites may be temporarily unavailable during processing

## Phase 1: Data Model & API Design

### Data Model: data-model.md

**Document Entity:**
- url (string): The source URL of the document
- title (string): The title of the document
- content (string): The extracted text content
- metadata (object): Additional metadata like headings, sections

**Text Chunk Entity:**
- id (string): Unique identifier for the chunk
- document_url (string): Reference to source document
- content (string): The chunked text content
- heading (string): The heading associated with this chunk
- section (string): The section of the document
- position (integer): Position in the original document

**Embedding Entity:**
- chunk_id (string): Reference to the text chunk
- vector (array): The embedding vector values
- model (string): The model used to generate the embedding
- timestamp (datetime): When the embedding was created

**Vector Record Entity:**
- point_id (string): Qdrant point ID
- embedding_id (string): Reference to the embedding
- payload (object): Metadata for search and filtering
- created_at (datetime): Timestamp of storage

### API Contracts

Since this is an ingestion-only system with no external API exposure, contracts will be internal function interfaces:

**discover_urls(base_url: str) -> List[str]**
- Discovers all accessible URLs from a GitHub Pages site
- Returns list of discovered URLs

**extract_content(url: str) -> Document**
- Extracts clean text content from a single URL
- Returns Document object with content and metadata

**chunk_content(document: Document, max_chunk_size: int = 1000) -> List[TextChunk]**
- Splits document content into appropriately sized chunks
- Returns list of TextChunk objects

**generate_embeddings(chunks: List[TextChunk], model: str = "embed-multilingual-v2.0") -> List[Embedding]**
- Generates embeddings for text chunks using Cohere
- Returns list of Embedding objects

**store_vectors(embeddings: List[Embedding]) -> bool**
- Stores embeddings in Qdrant with metadata
- Returns success status

## Phase 2: Implementation Plan

### Task Breakdown

1. **Setup & Project Structure**:
   - Create `backend/` directory
   - Initialize Python project with UV
   - Set up .env file structure
   - Install required dependencies

2. **URL Discovery Module**:
   - Implement web crawling logic to discover all pages
   - Handle GitHub Pages specific structure
   - Create function to return list of URLs

3. **Content Extraction Module**:
   - Implement HTML parsing and text extraction
   - Preserve structural metadata (headings, sections)
   - Create Document object representation

4. **Text Processing Module**:
   - Implement text normalization
   - Create chunking logic with appropriate sizing
   - Generate TextChunk objects with metadata

5. **Embedding Generation Module**:
   - Integrate with Cohere API
   - Generate embeddings with proper error handling
   - Create Embedding objects

6. **Vector Storage Module**:
   - Integrate with Qdrant Cloud
   - Store vectors with metadata payload
   - Implement verification mechanisms

7. **Pipeline Orchestration**:
   - Create main() function to coordinate all stages
   - Implement proper logging for each stage
   - Add error handling and retry logic

8. **Configuration & Environment**:
   - Set up environment variable handling
   - Create example .env file
   - Add configuration validation

### Dependencies (pyproject.toml)
- python = "^3.9"
- requests = "^2.31.0"
- beautifulsoup4 = "^4.12.0"
- cohere = "^4.0.0"
- qdrant-client = "^1.7.0"
- python-dotenv = "^1.0.0"
- loguru = "^0.7.0"

## Phase 3: Implementation Steps

### Step 1: Project Setup
1. Create `backend/` directory
2. Initialize project with `uv init`
3. Create `pyproject.toml` with dependencies
4. Set up `.env` file with required variables

### Step 2: Core Modules Development
1. Develop URL discovery module
2. Develop content extraction module
3. Develop text processing module
4. Develop embedding generation module
5. Develop vector storage module

### Step 3: Integration & Orchestration
1. Create main pipeline function
2. Implement error handling and logging
3. Add configuration validation
4. Test end-to-end flow

### Step 4: Testing & Verification
1. Create test cases for each module
2. Verify vector storage counts
3. Test semantic relevance of stored vectors
4. Validate deterministic behavior

## Success Criteria Verification

Each success criterion from the feature spec will be verified:
- SC-001: Verify 100% URL discovery through comparison with sitemap
- SC-002: Test text extraction accuracy with sample pages
- SC-003: Validate embedding consistency and storage success rate
- SC-004: Verify stored vector counts match ingestion totals
- SC-005: Test query relevance with sample searches
- SC-006: Test pipeline re-execution without duplication
- SC-007: Verify comprehensive logging at each stage

## Risks & Mitigation

1. **API Rate Limits**: Implement exponential backoff and request batching
2. **Large Content**: Implement content chunking before embedding
3. **Network Issues**: Add retry logic with configurable attempts
4. **Duplicate Processing**: Use URL-based deduplication with persistent tracking