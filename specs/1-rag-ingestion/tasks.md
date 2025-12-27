# Tasks: RAG Website URL Ingestion, Embedding Generation, and Vector Storage

**Feature**: 1-rag-ingestion
**Created**: 2025-12-27

## Phase 1: Setup

- [X] T001 Create backend/ directory structure
- [X] T002 Initialize Python project with UV in backend/ directory
- [X] T003 [P] Create pyproject.toml with required dependencies (requests, beautifulsoup4, cohere, qdrant-client, python-dotenv, loguru)
- [X] T004 Create .env file template with required variables (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY, GITHUB_PAGES_URL)
- [X] T005 Create directory structure: backend/src/{discovery,extraction,processing,embedding,storage,config}

## Phase 2: Foundational

- [X] T006 [P] Create base configuration module in backend/src/config/settings.py with environment variable handling
- [X] T007 [P] Create Document data class in backend/src/extraction/content_extraction.py
- [X] T008 [P] Create TextChunk data class in backend/src/processing/text_processing.py
- [X] T009 [P] Create Embedding data class in backend/src/embedding/embedding_generator.py
- [X] T010 Create logging configuration for pipeline stages

## Phase 3: [US1] Ingest Docusaurus Book Content

**Goal**: Programmatically discover all public GitHub Pages URLs of a book

**Independent Test**: System can be tested by providing a GitHub Pages URL and verifying that all pages are successfully discovered and ingested without manual intervention

**Implementation Tasks**:

- [X] T011 [P] [US1] Create url_discovery.py module in backend/src/discovery/
- [X] T012 [P] [US1] Implement discover_urls() function that discovers all accessible URLs from GitHub Pages site
- [X] T013 [P] [US1] Implement sitemap.xml parsing in URL discovery module
- [X] T014 [P] [US1] Implement web crawling logic to discover pages not in sitemap
- [X] T015 [P] [US1] Add GitHub Pages specific URL filtering to avoid external links
- [X] T016 [US1] Test URL discovery with sample GitHub Pages site

## Phase 4: [US2] Extract and Normalize Text Content

**Goal**: Extract clean text content from web pages and normalize it for embedding generation

**Independent Test**: System can be tested by ingesting a sample page and verifying that the extracted text is clean, readable, and contains relevant content without HTML artifacts

**Implementation Tasks**:

- [X] T017 [P] [US2] Create content_extraction.py module in backend/src/extraction/
- [X] T018 [P] [US2] Implement extract_content() function that extracts clean text from a single URL
- [X] T019 [P] [US2] Add Docusaurus-specific CSS selectors for content extraction (.main-wrapper, article.markdown, .theme-doc-markdown)
- [X] T020 [P] [US2] Implement metadata preservation (headings, sections) in content extraction
- [X] T021 [P] [US2] Add HTML artifact removal and text normalization
- [X] T022 [US2] Test content extraction with various Docusaurus page formats

## Phase 5: [US3] Generate Semantic Embeddings

**Goal**: Generate consistent semantic embeddings using Cohere models for semantic search and retrieval

**Independent Test**: System can be tested by generating embeddings for sample content and verifying dimensional consistency and semantic relevance

**Implementation Tasks**:

- [X] T023 [P] [US3] Create embedding_generator.py module in backend/src/embedding/
- [X] T024 [P] [US3] Implement generate_embeddings() function using Cohere API
- [X] T025 [P] [US3] Add error handling for Cohere API rate limits and failures
- [X] T026 [P] [US3] Implement embedding consistency validation (dimensionality checks)
- [X] T027 [P] [US3] Add semantic relevance testing for generated embeddings
- [X] T028 [US3] Test embedding generation with sample text chunks

## Phase 6: [US4] Store Embeddings in Vector Database

**Goal**: Persist embeddings in Qdrant Cloud with proper metadata for efficient retrieval

**Independent Test**: System can be tested by storing sample embeddings and verifying they can be retrieved with accurate metadata

**Implementation Tasks**:

- [X] T029 [P] [US4] Create vector_storage.py module in backend/src/storage/
- [X] T030 [P] [US4] Implement store_vectors() function to store embeddings in Qdrant
- [X] T031 [P] [US4] Create Qdrant collection with proper schema and metadata payload structure
- [X] T032 [P] [US4] Implement vector storage verification and count validation
- [X] T033 [P] [US4] Add semantic search capability for retrieval testing
- [X] T034 [US4] Test vector storage and retrieval with metadata verification

## Phase 7: [US5] Ensure Deterministic Pipeline

**Goal**: Create ingestion pipeline that is deterministic and re-runnable without creating duplicate entries

**Independent Test**: System can be tested by running the same ingestion twice and verifying no duplicates are created

**Implementation Tasks**:

- [X] T035 [P] [US5] Create processing state tracking module for pipeline determinism
- [X] T036 [P] [US5] Implement duplicate detection mechanism to prevent reprocessing
- [X] T037 [P] [US5] Add checkpoint and resume capability for failed pipelines
- [X] T038 [P] [US5] Implement idempotent processing for re-runnable pipeline
- [X] T039 [US5] Test pipeline re-execution without duplication

## Phase 8: [US1-5] Pipeline Orchestration

**Goal**: Create main() function to coordinate the complete end-to-end pipeline

**Independent Test**: Complete pipeline can be tested by running main() function with a GitHub Pages URL and verifying all stages complete successfully

**Implementation Tasks**:

- [X] T040 [P] Create main.py file with pipeline orchestration function
- [X] T041 [P] Implement main() function that coordinates URL discovery → content extraction → text processing → embedding generation → vector storage
- [X] T042 [P] Add comprehensive logging for each pipeline stage (ingest → chunk → embed → store)
- [X] T043 [P] Implement error handling and retry logic for each pipeline stage
- [X] T044 [P] Add configuration validation before pipeline execution
- [X] T045 [P] Create end-to-end pipeline test with sample GitHub Pages site
- [X] T046 Complete full pipeline test and validation

## Phase 9: Polish & Cross-Cutting Concerns

- [X] T047 Add comprehensive error handling across all modules
- [X] T048 Implement API rate limit handling with exponential backoff
- [X] T049 Add progress tracking and monitoring capabilities
- [X] T050 Update documentation and create usage examples
- [X] T051 Perform final integration testing
- [X] T052 Validate all success criteria from feature specification

## Dependencies

- US1 (URL Discovery) must complete before US2 (Content Extraction)
- US2 (Content Extraction) must complete before US3 (Embedding Generation)
- US3 (Embedding Generation) must complete before US4 (Vector Storage)
- US5 (Deterministic Pipeline) can be developed in parallel but needs to integrate with all other user stories

## Parallel Execution Examples

- Tasks T011-T016 can be developed in parallel (different modules)
- US2, US3, and US4 can be developed in parallel after US1 completion
- Configuration and data models (T006-T010) can be developed in parallel with other phases

## Implementation Strategy

**MVP Scope**: Complete US1 (URL Discovery) and US2 (Content Extraction) to demonstrate basic functionality

**Incremental Delivery**:
1. Phase 1-3: Basic URL discovery and content extraction
2. Phase 4: Add embedding generation capability
3. Phase 5-6: Add vector storage functionality
4. Phase 7-9: Complete pipeline with determinism and polish