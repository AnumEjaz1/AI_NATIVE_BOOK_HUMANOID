# Data Model: RAG Backend-Frontend Integration

## Entities

### QueryRequest
**Description**: Represents a user's query to the RAG system
**Fields**:
- query: str (required) - The user's input text to be processed
- metadata: dict (optional) - Additional context or parameters for the query
- user_id: str (optional) - Identifier for the user making the request

**Validation Rules**:
- query must not be empty
- query length must be less than 10000 characters
- metadata keys must be strings

### QueryResponse
**Description**: The RAG agent's response to a user query
**Fields**:
- response: str (required) - The agent's answer to the query
- sources: list[dict] (optional) - List of source documents referenced
- metadata: dict (optional) - Additional information about the response
- query_id: str (optional) - Identifier for tracking the query

**Validation Rules**:
- response must not be empty
- sources must be a list of dictionaries with required keys
- metadata must be a dictionary

### SourceDocument
**Description**: A document source referenced in the response
**Fields**:
- title: str (required) - Title of the source document
- content: str (required) - Content snippet from the document
- url: str (optional) - URL or path to the full document
- score: float (optional) - Relevance score of the document

**Validation Rules**:
- title must not be empty
- content must not be empty
- score must be between 0 and 1 if provided

### HealthStatus
**Description**: Health check response
**Fields**:
- status: str (required) - "healthy" if service is operational
- timestamp: str (required) - ISO 8601 timestamp of the check

**Validation Rules**:
- status must be "healthy"
- timestamp must be in ISO 8601 format

## State Transitions

### Query Processing
1. QueryRequest received → Processing state
2. Processing state → QueryResponse generated
3. QueryResponse generated → Response returned to client

## API Contracts

### POST /query
**Request**: QueryRequest
**Response**: QueryResponse
**Status Codes**:
- 200: Successful response
- 400: Invalid request format
- 500: Server error during processing

### GET /health
**Request**: None
**Response**: HealthStatus
**Status Codes**:
- 200: Service is healthy
- 500: Service is unhealthy