"""
Integration tests for the RAG FastAPI backend.
These tests validate the complete functionality of the API.
"""
import asyncio
from fastapi.testclient import TestClient
from src.rag_agent.api import app
from src.rag_agent.models import QueryRequest


def test_health_endpoint():
    """Test the health check endpoint."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


def test_query_endpoint_basic():
    """Test the query endpoint with a basic request."""
    with TestClient(app) as client:
        query_request = {
            "query": "What is artificial intelligence?",
            "metadata": {"test": "value"}
        }

        response = client.post("/query", json=query_request)
        assert response.status_code == 200

        data = response.json()
        assert "response" in data
        assert "sources" in data
        assert isinstance(data["sources"], list) or data["sources"] is None
        assert "metadata" in data


def test_query_endpoint_empty_query():
    """Test the query endpoint with an empty query (should fail validation)."""
    with TestClient(app) as client:
        query_request = {
            "query": "",  # Empty query should fail validation
            "metadata": {"test": "value"}
        }

        response = client.post("/query", json=query_request)
        assert response.status_code == 422  # Validation error


def test_metrics_endpoint():
    """Test the metrics endpoint."""
    with TestClient(app) as client:
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "metrics_endpoint_available"


def test_debug_logs_endpoint_disabled():
    """Test the debug logs endpoint when debug is disabled."""
    with TestClient(app) as client:
        response = client.get("/debug/logs")
        # Should return 403 since debug is disabled by default
        assert response.status_code == 403


if __name__ == "__main__":
    # Run the tests
    print("Running integration tests...")

    test_health_endpoint()
    print("PASS: Health endpoint test passed")

    test_query_endpoint_basic()
    print("PASS: Query endpoint basic test passed")

    test_query_endpoint_empty_query()
    print("PASS: Query endpoint validation test passed")

    test_metrics_endpoint()
    print("PASS: Metrics endpoint test passed")

    test_debug_logs_endpoint_disabled()
    print("PASS: Debug logs endpoint test passed")

    print("\nAll integration tests passed! OK")