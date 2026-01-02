from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, AsyncIterator
import logging
import asyncio
import time
from datetime import datetime
from contextlib import asynccontextmanager

from src.rag_agent.models import QueryRequest, QueryResponse, HealthStatus
from src.rag_agent.services import RAGAgentService
from src.rag_agent.config import settings


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Lifespan event manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    global rag_service
    logger.info("Starting up RAG Agent API...")

    try:
        # Perform health checks for external dependencies
        await _check_external_dependencies()

        # Initialize the RAG agent service
        rag_service = RAGAgentService()
        await rag_service.initialize()
        logger.info("RAG Agent API started successfully")

        yield  # Application runs during this period

    except Exception as e:
        logger.error(f"Failed to start RAG Agent API: {str(e)}")
        raise
    finally:
        # Shutdown cleanup
        logger.info("Shutting down RAG Agent API...")
        if rag_service:
            # Perform any necessary cleanup
            logger.info("RAG Agent service cleaned up")
        else:
            logger.warning("RAG Agent service was not initialized")


# Create FastAPI app instance with lifespan
app = FastAPI(
    title="RAG Agent API",
    description="API for interacting with the RAG agent system",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow local frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins - allowing all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG agent service
rag_service: Optional[RAGAgentService] = None


async def _check_external_dependencies():
    """
    Check health of external dependencies (OpenAI, Qdrant).
    """
    logger.info("Checking external dependencies...")

    # Check if required environment variables are set
    if not settings.openai_api_key:
        logger.warning("OpenAI API key not set - some functionality may be limited")
    else:
        logger.info("OpenAI API key is configured")

    if not settings.qdrant_url or not settings.qdrant_api_key:
        logger.warning("Qdrant configuration incomplete - vector store may be unavailable")
    else:
        logger.info("Qdrant configuration is complete")

    logger.info("External dependency checks completed")


@app.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return HealthStatus(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/debug/logs")
async def get_debug_logs():
    """
    Debug endpoint to retrieve recent request logs for debugging.
    This endpoint is only available when debug mode is enabled.
    """
    if not settings.debug:
        raise HTTPException(status_code=403, detail="Debug mode not enabled")

    # This is a placeholder implementation
    # In a real implementation, you would return actual logs
    return {
        "message": "Debug logs endpoint - logs would be returned here",
        "debug_enabled": settings.debug,
        "recent_requests": []
    }


@app.get("/metrics")
async def get_metrics():
    """
    Metrics endpoint for performance monitoring.
    """
    # This is a placeholder implementation
    # In a real implementation, you would return actual metrics
    return {
        "status": "metrics_endpoint_available",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoints_called": 0,  # Would track actual metrics in production
        "average_response_time": 0.0,  # Would calculate actual metrics in production
        "active_connections": 0  # Would track actual metrics in production
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(query_request: QueryRequest):
    """
    Endpoint to process user queries with the RAG agent.

    Args:
        query_request: The user's query request containing the query text and optional metadata

    Returns:
        QueryResponse containing the agent's response and source references
    """
    if rag_service is None:
        logger.error("RAG Agent Service not initialized")
        raise HTTPException(status_code=500, detail="RAG Agent Service not initialized")

    request_id = f"req_{int(time.time())}_{hash(query_request.query) % 10000}"
    logger.info(f"Request {request_id}: Received query request from user_id={query_request.user_id}")

    try:
        # Process the query using the RAG agent service
        response = await rag_service.process_query(query_request)

        logger.info(f"Request {request_id}: Query processed successfully")
        logger.debug(f"Request {request_id}: Response metadata: {response.metadata}")

        return response
    except Exception as e:
        logger.error(f"Request {request_id}: Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")