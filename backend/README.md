# RAG FastAPI Backend

This is a FastAPI backend service that exposes the RAG agent as HTTP endpoints, allowing frontend applications to query the RAG system and receive responses grounded in book content.

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
   pip install -r requirements.txt
   ```

3. **Create environment file**:
   Create a `.env` file in the backend root with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_URL=your_qdrant_cluster_url_here
   QDRANT_COLLECTION_NAME=book_content
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

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /query`: Submit queries to the RAG agent
- `GET /debug/logs`: Debug logs (when debug mode enabled)
- `GET /metrics`: Performance metrics

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
       "query": "What is embodied AI?",
       "metadata": {"session_id": "test-session"}
     }'
   ```

## Configuration

All configuration is managed through environment variables loaded from the `.env` file:
- `OPENAI_API_KEY`: API key for OpenAI services
- `QDRANT_API_KEY`: API key for Qdrant vector database
- `QDRANT_URL`: URL for the Qdrant cloud instance
- `QDRANT_COLLECTION_NAME`: Name of the collection containing book content
- `LOG_LEVEL`: Logging level (default: INFO)
- `DEBUG`: Enable debug mode (default: False)