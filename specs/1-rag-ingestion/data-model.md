# Data Model: RAG Website URL Ingestion, Embedding Generation, and Vector Storage

**Feature**: 1-rag-ingestion
**Created**: 2025-12-27

## Document Entity

Represents a web page from the Docusaurus book with URL, title, content, and structural metadata.

**Fields**:
- `id` (string): Unique identifier for the document
- `url` (string): The source URL of the document (required, unique)
- `title` (string): The title of the document (required)
- `content` (string): The extracted text content (required)
- `html_content` (string): The original HTML content (optional)
- `headings` (array): List of headings found in the document (optional)
- `sections` (array): List of sections in the document (optional)
- `created_at` (datetime): Timestamp when document was processed
- `updated_at` (datetime): Timestamp when document was last updated

**Validation Rules**:
- URL must be a valid URL format
- Content must not be empty
- URL must be unique across all documents

## Text Chunk Entity

Represents a segment of processed text with associated metadata (source URL, section, heading, content).

**Fields**:
- `id` (string): Unique identifier for the chunk (required, unique)
- `document_id` (string): Reference to the source document (required)
- `document_url` (string): Reference to source document URL (required)
- `content` (string): The chunked text content (required)
- `heading` (string): The heading associated with this chunk (optional)
- `section` (string): The section of the document (optional)
- `position` (integer): Position in the original document (required)
- `word_count` (integer): Number of words in the chunk (computed)
- `char_count` (integer): Number of characters in the chunk (computed)
- `hash` (string): Content hash for duplicate detection (computed)
- `created_at` (datetime): Timestamp when chunk was created

**Validation Rules**:
- Content must not exceed maximum embedding input size
- Position must be non-negative
- Document reference must exist
- Content must not be empty

## Embedding Entity

Represents a vector representation of text content with consistent dimensionality.

**Fields**:
- `id` (string): Unique identifier for the embedding (required, unique)
- `chunk_id` (string): Reference to the text chunk (required)
- `vector` (array): The embedding vector values (required)
- `model` (string): The model used to generate the embedding (required)
- `model_version` (string): Version of the model used (required)
- `dimensions` (integer): Number of dimensions in the vector (required)
- `created_at` (datetime): Timestamp when embedding was created
- `processing_time_ms` (integer): Time taken to generate the embedding

**Validation Rules**:
- Vector must have consistent dimensions per model
- Model and model_version must be valid Cohere models
- Chunk reference must exist
- Vector values must be valid floats

## Vector Record Entity

Represents a stored embedding in Qdrant with associated metadata for retrieval.

**Fields**:
- `point_id` (string): Qdrant point ID (required, unique)
- `embedding_id` (string): Reference to the embedding (required)
- `chunk_id` (string): Reference to the text chunk (required)
- `payload` (object): Metadata for search and filtering:
  - `document_url` (string): Source document URL
  - `heading` (string): Associated heading
  - `section` (string): Document section
  - `content_preview` (string): First 200 chars of content
  - `metadata` (object): Additional metadata as key-value pairs
- `collection_name` (string): Qdrant collection name (required)
- `created_at` (datetime): Timestamp when stored in Qdrant

**Validation Rules**:
- Point ID must be unique in the collection
- Embedding and chunk references must exist
- Payload must contain required metadata fields
- Collection must exist in Qdrant

## Processing State Entity

Tracks the state of documents during the ingestion pipeline to ensure deterministic behavior.

**Fields**:
- `id` (string): Unique identifier for the processing record (required)
- `url` (string): The URL being processed (required, unique)
- `status` (enum): Processing status (pending, processing, completed, failed)
- `stage` (enum): Current pipeline stage (discovery, extraction, chunking, embedding, storage)
- `attempts` (integer): Number of processing attempts
- `last_attempt_at` (datetime): Timestamp of last processing attempt
- `error_message` (string): Error message if processing failed
- `created_at` (datetime): Timestamp when record was created
- `updated_at` (datetime): Timestamp when record was last updated

**Validation Rules**:
- URL must be unique across all processing records
- Status must be one of the allowed enum values
- Stage must be one of the allowed enum values
- Attempts must be non-negative

## State Transitions

**Processing State Flow**:
1. `pending` → `processing` (when pipeline starts processing)
2. `processing` → `completed` (when all stages complete successfully)
3. `processing` → `failed` (when processing fails with max attempts reached)
4. `failed` → `pending` (when retry is initiated)

**Stage Progression**:
- discovery → extraction → chunking → embedding → storage
- Each stage must complete successfully before moving to the next
- Failed stages can be retried independently