# Quickstart: RAG Backend-Frontend Integration

## Prerequisites

- Python 3.11+
- pip package manager
- OpenAI API key
- Qdrant Cloud API key and endpoint

## Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn python-dotenv openai qdrant-client
   ```

3. **Create environment file**:
   Create a `.env` file in the backend root with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_COLLECTION_NAME=book_content
   ```

4. **Project structure**:
   ```
   backend/
   ├── src/
   │   ├── rag_agent/
   │   │   ├── __init__.py
   │   │   ├── api.py
   │   │   ├── models.py
   │   │   ├── services.py
   │   │   └── config.py
   │   └── embedding/  # From previous specs
   ├── pyproject.toml
   ├── requirements.txt
   └── main.py
   ```

## Running the Service

1. **Start the FastAPI server**:
   ```bash
   cd backend
   uvicorn src.rag_agent.api:app --reload --port 8000
   ```

2. **Access the API**:
   - API documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health
   - Query endpoint: http://localhost:8000/query

## Testing the API

1. **Health check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Query the RAG agent**:
   ```bash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is embodied AI?"
     }'
   ```

## Integration with Frontend

The API is configured with CORS enabled for local development. The frontend can make requests to the backend endpoints directly from localhost.

## Environment Configuration

All configuration is managed through environment variables loaded from the `.env` file:
- `OPENAI_API_KEY`: API key for OpenAI services
- `QDRANT_API_KEY`: API key for Qdrant vector database
- `QDRANT_URL`: URL for the Qdrant cloud instance
- `QDRANT_COLLECTION_NAME`: Name of the collection containing book content