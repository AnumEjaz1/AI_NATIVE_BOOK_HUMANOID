# Data Model: RAG Retrieval Pipeline Validation

**Feature**: 1-rag-retrieval-validation
**Date**: 2025-12-30
**Status**: Complete

## Overview

This document defines the key data structures and entities used in the RAG retrieval pipeline validation system. These models represent the core data objects that will be processed, validated, and logged during the retrieval validation process.

## Core Entities

### RetrievedChunk
**Description**: Represents a content chunk retrieved from Qdrant during the validation process

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

### QueryVector
**Description**: Represents the vector embedding of a test query used for similarity search

**Fields**:
- `vector` (list[float]): The numerical vector representation of the query
- `text` (string): The original text of the query
- `embedding_model` (string): Name/version of the model used to generate the embedding

**Validation Rules**:
- vector must have consistent dimensionality matching the stored embeddings
- embedding_model must match the Cohere model used in Spec-1

### ValidationResult
**Description**: Represents the results of validating a single retrieval operation

**Fields**:
- `query` (string): The original test query
- `retrieved_chunks` (list[RetrievedChunk]): List of chunks returned by the search
- `expected_relevance` (string): Expected type of content to be retrieved
- `validation_passed` (bool): Whether the validation criteria were met
- `metadata_complete` (bool): Whether all required metadata fields are present
- `relevance_score` (float): Assessment of how relevant the results are to the query
- `issues` (list[string]): List of any issues detected during validation

**Validation Rules**:
- retrieved_chunks must contain at least one element for successful validation
- relevance_score must be between 0.0 and 1.0
- issues should be empty if validation_passed is true

### PipelineStatus
**Description**: Represents the overall status of the retrieval pipeline validation

**Fields**:
- `connection_successful` (bool): Whether connection to Qdrant was established
- `total_queries` (int): Number of test queries executed
- `successful_retrievals` (int): Number of queries that returned valid results
- `failed_retrievals` (int): Number of queries that failed validation
- `start_time` (datetime): When the validation process started
- `end_time` (datetime): When the validation process completed
- `execution_time` (float): Total time taken for validation in seconds
- `error_logs` (list[string]): Any errors encountered during the process

**Validation Rules**:
- successful_retrievals + failed_retrievals must equal total_queries
- execution_time must be positive
- error_logs should be empty if all validations passed

## Data Relationships

```
QueryVector --[generates]--> RetrievedChunk
RetrievedChunk --[part of]--> ValidationResult
ValidationResult --[composes]--> PipelineStatus
```

## Data Validation Requirements

### From Functional Requirements
- **FR-003**: All RetrievedChunk objects must contain complete metadata (url, section, heading, chunk_id)
- **FR-004**: RetrievedChunk objects must include similarity_score values
- **FR-007**: RetrievedChunk objects must be consistent across multiple runs for the same query

### Validation Logic
1. When creating a RetrievedChunk, validate that all required metadata fields are present
2. When processing a ValidationResult, verify that similarity scores are within expected ranges
3. When aggregating PipelineStatus, ensure all metrics are consistent and properly calculated

## Serialization Format

The data models will be serialized using Python's built-in dataclasses with JSON serialization for logging and reporting purposes:

```python
# Example structure (to be implemented in retrieve.py):
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class RetrievedChunk:
    id: str
    content: str
    url: str
    section: str
    heading: str
    chunk_id: str
    similarity_score: float
    metadata: Dict

@dataclass
class ValidationResult:
    query: str
    retrieved_chunks: List[RetrievedChunk]
    expected_relevance: str
    validation_passed: bool
    metadata_complete: bool
    relevance_score: float
    issues: List[str]
```

## State Transitions

### ValidationResult States
1. **Initialized**: ValidationResult created with query and expected_relevance
2. **Processed**: RetrievedChunks populated from Qdrant search
3. **Validated**: All validation checks completed, validation_passed set
4. **Logged**: Results written to log file

### PipelineStatus States
1. **Starting**: Pipeline execution begins
2. **Running**: Individual queries being processed
3. **Completed**: All queries processed, final metrics calculated
4. **Reported**: Status written to output