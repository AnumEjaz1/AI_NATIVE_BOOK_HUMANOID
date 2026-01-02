# Data Model: RAG Agent Construction with Retrieval Capabilities

**Feature**: 2-agent-retrieval
**Date**: 2025-12-30
**Status**: Complete

## Overview

This document defines the key data structures and entities used in the RAG agent construction system. These models represent the core data objects that will be processed, validated, and logged during the agent-based retrieval and response generation process.

## Core Entities

### AgentRequest
**Description**: Represents a user query or instruction sent to the AI agent for processing

**Fields**:
- `query` (string): The original user query or request
- `user_id` (string): Identifier for the user making the request
- `timestamp` (datetime): When the request was received
- `context` (dict): Additional context or metadata about the request
- `session_id` (string): Session identifier for conversation history

**Validation Rules**:
- query must not be empty
- timestamp must be current or past
- user_id should follow standard identifier format

### RetrievedContext
**Description**: Content chunks retrieved from Qdrant that provide grounding for the agent's response

**Fields**:
- `chunks` (list[RetrievedChunk]): List of content chunks retrieved from Qdrant
- `retrieval_query` (string): The query used to retrieve the content
- `retrieval_time` (float): Time taken to retrieve the content
- `relevance_threshold` (float): Minimum similarity score for inclusion
- `total_chunks_found` (int): Total number of chunks found before filtering

**Validation Rules**:
- chunks list must not be empty
- retrieval_time must be positive
- relevance_threshold must be between 0.0 and 1.0

### RetrievedChunk
**Description**: A single content chunk retrieved from Qdrant during the validation process

**Fields**:
- `id` (string): Unique identifier for the chunk (matches the Qdrant point ID)
- `content` (string): The actual text content of the chunk
- `url` (string): Source URL where this content originated
- `section` (string): Document section or chapter where the content appears
- `heading` (string): Heading or title associated with this content
- `chunk_id` (string): Internal identifier for the chunk within the document
- `similarity_score` (float): Cosine similarity score between query and this chunk
- `metadata` (dict): Additional metadata stored with the chunk in Qdrant

**Validation Rules**:
- All string fields must not be empty
- similarity_score must be between 0.0 and 1.0
- metadata must contain required fields (url, section, heading, chunk_id)

### AgentResponse
**Description**: The generated response that incorporates information from retrieved context

**Fields**:
- `content` (string): The agent's response to the user query
- `source_chunks` (list[string]): IDs of the retrieved chunks used in the response
- `confidence_score` (float): Confidence level in the response accuracy
- `grounding_verification` (bool): Whether the response was verified to be grounded in retrieved content
- `citations` (list[dict]): Citations to specific parts of the retrieved content
- `processing_time` (float): Time taken to generate the response

**Validation Rules**:
- content must not be empty
- confidence_score must be between 0.0 and 1.0
- grounding_verification must be a boolean
- source_chunks must match IDs in the corresponding RetrievedContext

### QueryVector
**Description**: Vector representation of the user query used for similarity search in Qdrant

**Fields**:
- `vector` (list[float]): The numerical vector representation of the query
- `text` (string): The original text of the query
- `embedding_model` (string): Name/version of the model used to generate the embedding
- `dimension` (int): Number of dimensions in the vector

**Validation Rules**:
- vector must have consistent dimensionality matching the stored embeddings
- embedding_model must match the Cohere model used in previous specs
- dimension must be positive

### AgentStatus
**Description**: Represents the overall status of the agent system

**Fields**:
- `agent_initialized` (bool): Whether the OpenAI agent is properly initialized
- `qdrant_connected` (bool): Whether connection to Qdrant is established
- `total_queries_processed` (int): Number of queries processed since initialization
- `successful_responses` (int): Number of successful responses generated
- `failed_queries` (int): Number of queries that resulted in errors
- `start_time` (datetime): When the agent was initialized
- `error_logs` (list[string]): Any errors encountered during operation

**Validation Rules**:
- successful_responses + failed_queries must equal total_queries_processed
- error_logs should be empty if all queries succeeded
- start_time must be before current time

## Data Relationships

```
AgentRequest --[generates]--> QueryVector
QueryVector --[searches]--> RetrievedContext
RetrievedContext --[contains]--> RetrievedChunk
RetrievedContext + AgentRequest --[generates]--> AgentResponse
AgentResponse --[updates]--> AgentStatus
```

## Data Validation Requirements

### From Functional Requirements
- **FR-003**: AgentResponse objects must have retrieved context properly injected
- **FR-004**: AgentResponse objects must be grounded in retrieved book content
- **FR-005**: AgentResponse objects must be deterministic for identical AgentRequest objects
- **FR-006**: AgentStatus objects must track retrieval failures and log them appropriately

### Validation Logic
1. When creating an AgentResponse, validate that source_chunks match IDs in the corresponding RetrievedContext
2. When processing an AgentResponse, verify that grounding_verification is properly set
3. When aggregating AgentStatus, ensure all metrics are consistent and properly calculated

## Serialization Format

The data models will be serialized using Python's built-in dataclasses with JSON serialization for logging and reporting purposes:

```python
# Example structure (to be implemented in retrieve.py):
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class AgentRequest:
    query: str
    user_id: str
    timestamp: datetime
    context: Dict
    session_id: str

@dataclass
class AgentResponse:
    content: str
    source_chunks: List[str]
    confidence_score: float
    grounding_verification: bool
    citations: List[Dict]
    processing_time: float
```

## State Transitions

### AgentResponse States
1. **Initialized**: AgentResponse created with query and context
2. **Processing**: RetrievedContext integrated into agent prompt
3. **Generated**: Response content created by the agent
4. **Verified**: Grounding verification completed
5. **Completed**: Response returned to user with proper citations

### AgentStatus States
1. **Initializing**: Agent being set up with OpenAI and Qdrant
2. **Ready**: Agent initialized and ready to process queries
3. **Processing**: Agent actively handling requests
4. **Monitoring**: Status being tracked and updated