# Quickstart: RAG Retrieval Pipeline Validation

**Feature**: 1-rag-retrieval-validation
**Date**: 2025-12-30
**Status**: Complete

## Overview

This guide provides step-by-step instructions to set up and run the RAG retrieval pipeline validation system. The validation system connects to Qdrant Cloud, retrieves embedded book content, and validates semantic relevance, metadata integrity, and end-to-end pipeline correctness.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Qdrant Cloud account and credentials
- Cohere API key (same model used in Spec-1)
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
pip install qdrant-client cohere python-dotenv pytest
```

Alternatively, if a requirements.txt file exists in the project:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_COLLECTION_NAME=your_collection_name  # The collection where embeddings from Spec-1 were stored
COHERE_MODEL_NAME=embed-multilingual-v3.0  # Or the specific model used in Spec-1
```

**Note**: Ensure you're using the same Cohere model that was used in Spec-1 to maintain embedding consistency.

## Running the Validation

### 1. Navigate to the Backend Directory

```bash
cd backend/src/embedding/
```

### 2. Run the Retrieval Validation

```bash
python retrieve.py
```

### 3. Custom Test Queries (Optional)

To run with custom test queries, you can modify the test queries in the retrieve.py file or pass them as command-line arguments if implemented:

```bash
python retrieve.py --queries "What is the main concept?" "Explain the architecture" "How does validation work?"
```

## Expected Output

The validation will produce:

1. **Connection Status**: Confirmation of successful connection to Qdrant Cloud
2. **Query Results**: For each test query:
   - Retrieved content chunks with similarity scores
   - Metadata validation status (URL, section, heading, chunk ID)
   - Relevance assessment
3. **Validation Summary**: Overall pipeline status including:
   - Number of successful vs failed retrievals
   - Metadata completeness percentage
   - Execution time
4. **Log File**: Detailed logs in `retrieval_validation.log` with:
   - Query inputs
   - Similarity scores
   - Retrieved chunks
   - Any detected pipeline failures

## Verification Steps

### 1. Check Connection
- Verify that the system connects to Qdrant Cloud successfully
- Confirm that the collection from Spec-1 is accessible

### 2. Validate Retrieval Quality
- Check that semantic search returns contextually relevant chunks
- Verify similarity scores are within expected ranges (typically 0.5-1.0 for relevant results)

### 3. Confirm Metadata Integrity
- Ensure all retrieved results include URL, section, heading, and chunk ID
- Verify metadata format matches expectations

### 4. Assess Reproducibility
- Run the validation multiple times with the same queries
- Confirm that results are consistent across runs

### 5. Test Failure Detection
- Introduce queries that should return no results
- Verify that empty results are detected and logged appropriately

## Troubleshooting

### Connection Issues
- Verify QDRANT_URL and QDRANT_API_KEY in your .env file
- Check that your Qdrant Cloud account is active and accessible
- Ensure the collection name matches what was created in Spec-1

### Embedding Model Mismatch
- Confirm you're using the same Cohere model as in Spec-1
- Check that embedding dimensions match between queries and stored vectors

### Empty Results
- Verify that the Qdrant collection contains data from Spec-1
- Check that test queries are semantically related to the embedded content

### Dimension Mismatch
- Ensure the Cohere model used for query embeddings matches the one used for document embeddings
- Verify that both Spec-1 and Spec-2 use the same embedding dimensions

## Sample Output

```
RAG Retrieval Pipeline Validation Started
=========================================

✓ Connected to Qdrant Cloud successfully
✓ Collection 'book_embeddings' found with 1250 vectors
✓ Cohere model 'embed-multilingual-v3.0' loaded

Running Test Queries...
Query 1: "What is vector retrieval?"
  - Retrieved 5 chunks with scores: [0.89, 0.85, 0.78, 0.72, 0.68]
  - Metadata: ✓ All chunks have complete metadata
  - Relevance: ✓ High semantic relevance detected

Query 2: "Explain semantic search"
  - Retrieved 5 chunks with scores: [0.92, 0.87, 0.81, 0.75, 0.69]
  - Metadata: ✓ All chunks have complete metadata
  - Relevance: ✓ High semantic relevance detected

Validation Summary:
- Total Queries: 2
- Successful Retrievals: 2 (100%)
- Metadata Complete: 100%
- Execution Time: 4.2 seconds
- Pipeline Status: ✓ All validations passed

Log file created: retrieval_validation.log
```

## Next Steps

After successful validation:
1. Review the log file for any anomalies
2. Adjust test queries to cover different content areas
3. Validate with a broader range of queries to ensure robustness
4. Prepare for the next phase of the RAG system integration