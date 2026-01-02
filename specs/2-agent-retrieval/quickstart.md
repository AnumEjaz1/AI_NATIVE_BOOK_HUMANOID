# Quickstart: RAG Agent Construction with Retrieval Capabilities

**Feature**: 2-agent-retrieval
**Date**: 2025-12-30
**Status**: Complete

## Overview

This guide provides step-by-step instructions to set up and run the RAG agent system. The agent integrates with OpenAI Agents SDK, retrieves content from Qdrant Cloud, and generates grounded responses based on retrieved book content.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- OpenAI API key
- Qdrant Cloud account and credentials
- Cohere API key (same model used in previous specs)
- Git (for cloning the repository)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Create Python Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install openai qdrant-client cohere python-dotenv pytest
```

Alternatively, if a requirements.txt file exists in the project:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_COLLECTION_NAME=your_collection_name  # The collection where embeddings from previous specs were stored
COHERE_MODEL_NAME=embed-multilingual-v3.0  # Or the specific model used in previous specs
AGENT_NAME=book_retrieval_agent
AGENT_INSTRUCTIONS="You are a helpful assistant that answers questions based on the provided book content. Use the retrieved context to ground your responses in the book material."
```

**Note**: Ensure you're using the same Cohere model that was used in previous specs to maintain embedding consistency.

## Running the Agent

### 1. Navigate to the Backend Directory

```bash
cd backend/src/embedding/
```

### 2. Run the Agent System

```bash
python retrieve.py
```

### 3. Test Queries (Optional)

To run with custom test queries, you can pass them as command-line arguments:

```bash
python retrieve.py --queries "What is vector retrieval?" "Explain semantic search" "How does RAG work?"
```

## Expected Output

The agent system will produce:

1. **Agent Initialization**: Confirmation that the OpenAI agent is properly initialized
2. **Connection Status**: Confirmation of successful connection to Qdrant Cloud
3. **Query Processing**: For each query:
   - Retrieved content chunks with similarity scores
   - Context injection into agent prompt
   - Generated response grounded in retrieved content
   - Citations to source material
4. **Response Quality**: Verification that responses are grounded in book content
5. **Agent Status**: Overall system status including:
   - Number of successful vs failed queries
   - Processing time metrics
   - Any errors encountered
6. **Log File**: Detailed logs in `agent_retrieval.log` with:
   - Query inputs
   - Retrieved chunks and similarity scores
   - Agent responses
   - Any detected processing failures

## Verification Steps

### 1. Check Agent Initialization
- Verify that the OpenAI agent is created successfully
- Confirm that agent instructions are properly set

### 2. Check Qdrant Connection
- Verify that the system connects to Qdrant Cloud successfully
- Confirm that the collection from previous specs is accessible

### 3. Validate Retrieval Quality
- Check that semantic search returns contextually relevant chunks
- Verify similarity scores are within expected ranges (typically 0.5-1.0 for relevant results)

### 4. Confirm Response Grounding
- Ensure responses are based on retrieved content
- Verify citations to source material are included
- Check that responses are deterministic for identical queries

### 5. Test Failure Handling
- Introduce queries that should return no results
- Verify that retrieval failures are handled gracefully

## Troubleshooting

### Agent Initialization Issues
- Verify OPENAI_API_KEY in your .env file
- Check that you have access to the OpenAI Agents API

### Connection Issues
- Verify QDRANT_URL and QDRANT_API_KEY in your .env file
- Check that your Qdrant Cloud account is active and accessible
- Ensure the collection name matches what was created in previous specs

### Embedding Model Mismatch
- Confirm you're using the same Cohere model as in previous specs
- Check that embedding dimensions match between queries and stored vectors

### Empty Results
- Verify that the Qdrant collection contains data from previous specs
- Check that test queries are semantically related to the embedded content

### Context Injection Issues
- Ensure the retrieved context isn't too large for the model's context window
- Verify that context is properly formatted for the agent

## Sample Output

```
RAG Agent System Started
========================

✓ OpenAI agent initialized successfully
✓ Connected to Qdrant Cloud successfully
✓ Collection 'book_embeddings' found with 1250 vectors
✓ Cohere model 'embed-multilingual-v3.0' loaded

Processing Test Queries...
Query 1: "What is vector retrieval?"
  - Retrieved 5 chunks with scores: [0.89, 0.85, 0.78, 0.72, 0.68]
  - Context injected into agent prompt
  - Response generated: "Vector retrieval is the process of finding..."
  - Grounding verified: ✓ Response based on retrieved content
  - Citations: [chunk-001, chunk-002, chunk-005]

Query 2: "Explain semantic search"
  - Retrieved 5 chunks with scores: [0.92, 0.87, 0.81, 0.75, 0.69]
  - Context injected into agent prompt
  - Response generated: "Semantic search uses meaning rather than keywords..."
  - Grounding verified: ✓ Response based on retrieved content
  - Citations: [chunk-012, chunk-015, chunk-022]

Agent Status:
- Total Queries: 2
- Successful Responses: 2 (100%)
- Grounding Verified: 100%
- Processing Time: 8.4 seconds
- Agent Status: ✓ All queries processed successfully

Log file created: agent_retrieval.log
```

## Next Steps

After successful setup:
1. Review the log file for any anomalies
2. Test with a broader range of queries to validate agent behavior
3. Experiment with different agent instructions to optimize response quality
4. Prepare for integration with the next phase of the RAG system