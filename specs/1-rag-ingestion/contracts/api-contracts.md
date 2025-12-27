# API Contracts: RAG Ingestion Pipeline

**Feature**: 1-rag-ingestion
**Created**: 2025-12-27

## Internal Function Interfaces

### URL Discovery Service

**Function**: `discover_urls(base_url: str) -> List[str]`
- **Purpose**: Discover all accessible URLs from a GitHub Pages site
- **Input**: Base URL of the GitHub Pages site
- **Output**: List of discovered URLs
- **Error Cases**: Network errors, invalid URL format, rate limiting
- **Performance**: Should complete within 60 seconds for sites with <1000 pages

### Content Extraction Service

**Function**: `extract_content(url: str) -> Document`
- **Purpose**: Extract clean text content from a single URL
- **Input**: URL to extract content from
- **Output**: Document object with content and metadata
- **Error Cases**: Network errors, parsing failures, content not found
- **Performance**: Should complete within 10 seconds per page

### Text Processing Service

**Function**: `chunk_content(document: Document, max_chunk_size: int = 1000) -> List[TextChunk]`
- **Purpose**: Split document content into appropriately sized chunks
- **Input**: Document object and maximum chunk size
- **Output**: List of TextChunk objects
- **Error Cases**: Invalid document format, empty content
- **Performance**: Should process 100KB content within 5 seconds

### Embedding Generation Service

**Function**: `generate_embeddings(chunks: List[TextChunk], model: str = "embed-multilingual-v3.0") -> List[Embedding]`
- **Purpose**: Generate embeddings for text chunks using Cohere
- **Input**: List of TextChunk objects and embedding model
- **Output**: List of Embedding objects
- **Error Cases**: API rate limits, authentication failures, invalid content
- **Performance**: Should handle 100 chunks within 60 seconds (considering API rate limits)

### Vector Storage Service

**Function**: `store_vectors(embeddings: List[Embedding]) -> bool`
- **Purpose**: Store embeddings in Qdrant with metadata
- **Input**: List of Embedding objects
- **Output**: Success status (true/false)
- **Error Cases**: Qdrant connection failures, authentication issues, invalid payloads
- **Performance**: Should store 100 vectors within 30 seconds

### Pipeline Orchestration Service

**Function**: `process_document(url: str) -> ProcessingResult`
- **Purpose**: Process a single document through the entire pipeline
- **Input**: URL to process
- **Output**: ProcessingResult with status and any errors
- **Error Cases**: Any stage failure, network issues, API failures
- **Performance**: Should complete within 120 seconds per document (including API calls)

## Data Transfer Objects

### Document
```python
class Document:
    id: str
    url: str
    title: str
    content: str
    html_content: Optional[str]
    headings: List[str]
    sections: List[str]
    created_at: datetime
```

### TextChunk
```python
class TextChunk:
    id: str
    document_id: str
    document_url: str
    content: str
    heading: Optional[str]
    section: Optional[str]
    position: int
    hash: str
```

### Embedding
```python
class Embedding:
    id: str
    chunk_id: str
    vector: List[float]
    model: str
    model_version: str
    dimensions: int
```

### ProcessingResult
```python
class ProcessingResult:
    success: bool
    document_url: str
    stages_completed: List[str]
    error_message: Optional[str]
    processing_time: float
```

## Error Handling Contracts

### Standard Error Format
```python
class PipelineError:
    error_code: str
    message: str
    stage: str
    timestamp: datetime
    details: Optional[Dict]
```

### Retry Strategy
- All services should implement exponential backoff for API-dependent operations
- Maximum 3 retries with 1s, 2s, 4s delay pattern
- Circuit breaker pattern for external API failures
- Idempotent operations where possible to support retries

## Logging Contracts

### Log Format
All services must log to standard output with the following structured format:
```
{"timestamp": "ISO8601", "level": "INFO|ERROR|WARN", "stage": "discovery|extraction|chunking|embedding|storage", "url": "document_url", "message": "log_message", "correlation_id": "unique_id"}
```

### Required Log Events
- Start of each processing stage
- Completion of each processing stage
- Errors at any stage with full context
- Batch processing events (start/end of batch)