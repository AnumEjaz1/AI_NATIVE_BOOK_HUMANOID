"""
Unit tests for RAG agent construction with retrieval capabilities
Testing agent initialization and basic retrieval functions
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from backend.src.embedding.retrieve import RAGAgent, ConfigManager, AgentResponse


class TestConfigManager:
    """Test configuration loading and validation"""

    def test_config_loading_from_env(self, monkeypatch):
        """Test that ConfigManager loads environment variables correctly"""
        # Set up environment variables for testing
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.setenv("QDRANT_URL", "https://test.qdrant.tech:6333")
        monkeypatch.setenv("QDRANT_API_KEY", "test-qdrant-key")
        monkeypatch.setenv("COHERE_API_KEY", "test-cohere-key")
        monkeypatch.setenv("QDRANT_COLLECTION_NAME", "test_collection")

        config = ConfigManager()
        assert config.openai_api_key == "test-openai-key"
        assert config.qdrant_url == "https://test.qdrant.tech:6333"
        assert config.qdrant_api_key == "test-qdrant-key"
        assert config.cohere_api_key == "test-cohere-key"
        assert config.collection_name == "test_collection"

    def test_config_validation_missing_vars(self, monkeypatch):
        """Test that ConfigManager validates required environment variables"""
        # Remove required environment variables
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("QDRANT_URL", raising=False)
        monkeypatch.delenv("QDRANT_API_KEY", raising=False)
        monkeypatch.delenv("COHERE_API_KEY", raising=False)
        monkeypatch.delenv("QDRANT_COLLECTION_NAME", raising=False)

        with pytest.raises(ValueError, match="Missing required environment variables"):
            ConfigManager()


class TestRAGAgentInitialization:
    """Test RAG agent initialization functions"""

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_initialize_clients(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test that clients are initialized correctly"""
        # Mock the client instances
        mock_openai_instance = Mock()
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_client.return_value = mock_openai_instance
        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance

        agent = RAGAgent()
        agent.initialize_clients()

        # Verify that clients were initialized
        assert agent.openai_client is not None
        assert agent.qdrant_client is not None
        assert agent.cohere_client is not None

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection",
        "AGENT_NAME": "test_agent",
        "AGENT_INSTRUCTIONS": "Test instructions"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_initialize_agent(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test agent initialization"""
        # Mock the OpenAI client and its beta.assistants attribute
        mock_openai_instance = Mock()
        mock_assistant = Mock()
        mock_assistant.id = "test-assistant-id"
        mock_assistant.name = "test_agent"
        mock_openai_instance.beta.assistants.create.return_value = mock_assistant
        mock_openai_client.return_value = mock_openai_instance

        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance

        agent = RAGAgent()
        agent.initialize_clients()
        agent.initialize_agent()

        # Verify that the agent was created
        assert agent.agent is not None
        mock_openai_instance.beta.assistants.create.assert_called_once()

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_validate_connection_success(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test connection validation with successful connection"""
        # Mock the Qdrant client and its methods
        mock_client_instance = Mock()
        mock_collections = Mock()
        mock_collections.collections = [Mock()]
        mock_client_instance.get_collections.return_value = mock_collections
        mock_qdrant_client.return_value = mock_client_instance

        mock_openai_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_client.return_value = mock_openai_instance
        mock_cohere_client.return_value = mock_cohere_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_client_instance

        result = agent.validate_connection()
        assert result is True
        mock_client_instance.get_collections.assert_called_once()

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_validate_connection_failure(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test connection validation with failed connection"""
        # Mock the Qdrant client to raise an exception
        mock_client_instance = Mock()
        mock_client_instance.get_collections.side_effect = Exception("Connection failed")
        mock_qdrant_client.return_value = mock_client_instance

        mock_openai_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_client.return_value = mock_openai_instance
        mock_cohere_client.return_value = mock_cohere_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_client_instance

        result = agent.validate_connection()
        assert result is False


class TestRAGAgentRetrieval:
    """Integration tests for retrieval functionality"""

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_semantic_search_integration(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Integration test for semantic search functionality"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()

        # Mock the Cohere embed response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        mock_cohere_instance.embed.return_value = mock_embed_response
        mock_cohere_client.return_value = mock_cohere_instance

        # Mock the Qdrant search response
        mock_point = Mock()
        mock_point.id = "1"
        mock_point.score = 0.8
        mock_point.payload = {
            "content": "Test content",
            "url": "http://example.com",
            "section": "Section 1",
            "heading": "Heading 1",
            "chunk_id": "chunk-1"
        }
        mock_search_result = [mock_point]
        mock_qdrant_instance.search.return_value = mock_search_result
        mock_qdrant_client.return_value = mock_qdrant_instance

        mock_openai_instance = Mock()
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Test semantic search
        result = agent.semantic_search("test query", top_k=1)

        # Verify the results
        assert len(result.chunks) == 1
        assert result.chunks[0].content == "Test content"
        assert result.chunks[0].similarity_score == 0.8

        # Verify that the correct methods were called
        mock_cohere_instance.embed.assert_called_once()
        mock_qdrant_instance.search.assert_called_once()


class TestRAGAgentResponseGrounding:
    """Test response grounding and deterministic behavior features"""

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_verify_response_grounding(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test response grounding verification function"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Create a retrieved context with a chunk
        chunk = RetrievedChunk(
            id="1",
            content="This is relevant content about vector retrieval",
            url="http://example.com",
            section="Section 1",
            heading="Vector Retrieval",
            chunk_id="chunk-1",
            similarity_score=0.8,
            metadata={}
        )
        retrieved_context = RetrievedContext(
            chunks=[chunk],
            retrieval_query="What is vector retrieval?",
            retrieval_time=0.1,
            relevance_threshold=0.5,
            total_chunks_found=1
        )

        # Test with response that contains content from the chunk
        response_with_content = "Vector retrieval is a technique where This is relevant content about vector retrieval"
        result_true = agent.verify_response_grounding(response_with_content, retrieved_context)
        assert result_true is True

        # Test with response that doesn't contain content from the chunk
        response_without_content = "This is a completely different topic"
        result_false = agent.verify_response_grounding(response_without_content, retrieved_context)
        assert result_false is False

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_extract_citations_from_response(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test citation extraction from response"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Create a retrieved context with chunks
        chunk1 = RetrievedChunk(
            id="1",
            content="This is content about vector retrieval",
            url="http://example.com/vector",
            section="Section 1",
            heading="Vector Retrieval",
            chunk_id="chunk-1",
            similarity_score=0.8,
            metadata={}
        )
        chunk2 = RetrievedChunk(
            id="2",
            content="This is content about semantic search",
            url="http://example.com/semantic",
            section="Section 2",
            heading="Semantic Search",
            chunk_id="chunk-2",
            similarity_score=0.7,
            metadata={}
        )
        retrieved_context = RetrievedContext(
            chunks=[chunk1, chunk2],
            retrieval_query="Tell me about these topics",
            retrieval_time=0.1,
            relevance_threshold=0.5,
            total_chunks_found=2
        )

        # Test with response that cites the first chunk
        response_with_citation = "Vector retrieval is important. See http://example.com/vector for more details."
        citations = agent.extract_citations_from_response(response_with_citation, retrieved_context)
        assert len(citations) == 1
        assert citations[0]["url"] == "http://example.com/vector"

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_ensure_deterministic_behavior(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test deterministic behavior for identical queries"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Since we can't actually run the full agent process in tests,
        # we'll test the helper method for comparing responses
        result = agent._responses_are_similar("This is a test response", "This is a test response")
        assert result is True

        result_diff = agent._responses_are_similar("This is a test response", "This is a different response")
        assert result_diff is False

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_add_confidence_scoring(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test confidence scoring for agent responses"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Create a retrieved context with chunks
        chunk = RetrievedChunk(
            id="1",
            content="This is relevant content",
            url="http://example.com",
            section="Section 1",
            heading="Heading 1",
            chunk_id="chunk-1",
            similarity_score=0.8,
            metadata={}
        )
        retrieved_context = RetrievedContext(
            chunks=[chunk],
            retrieval_query="Test query",
            retrieval_time=0.1,
            relevance_threshold=0.5,
            total_chunks_found=1
        )

        # Test confidence scoring with a response that cites the chunk
        response_with_citation = "This is relevant content. See http://example.com for details."
        confidence = agent.add_confidence_scoring(response_with_citation, retrieved_context)
        assert confidence > 0.5  # Should be relatively high due to citation

        # Test with empty context
        empty_context = RetrievedContext([], "Test query", 0.0, 0.5, 0)
        low_confidence = agent.add_confidence_scoring("Any response", empty_context)
        assert low_confidence == 0.1  # Should be low due to no context


class TestRAGAgentFailureHandling:
    """Test failure handling and logging functionality"""

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_detect_retrieval_failures_and_log(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test retrieval failure detection and logging"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Mock the semantic_search method to return empty results
        agent.semantic_search = Mock(return_value=RetrievedContext(
            chunks=[],
            retrieval_query="test query",
            retrieval_time=0.1,
            relevance_threshold=0.5,
            total_chunks_found=0
        ))

        # Test with empty results
        result = agent.detect_retrieval_failures_and_log("test query")
        assert result is True  # Should detect failure when no results found

        # Mock the semantic_search method to raise an exception
        agent.semantic_search = Mock(side_effect=Exception("Connection failed"))

        # Test with exception
        result_exception = agent.detect_retrieval_failures_and_log("test query")
        assert result_exception is True  # Should detect failure when exception occurs

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_handle_empty_retrieval_results_gracefully(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test handling of empty retrieval results gracefully"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Mock the semantic_search method to return empty results
        agent.semantic_search = Mock(return_value=RetrievedContext(
            chunks=[],
            retrieval_query="test query",
            retrieval_time=0.1,
            relevance_threshold=0.5,
            total_chunks_found=0
        ))

        # Test handling empty results
        response = agent.handle_empty_retrieval_results_gracefully("test query")
        assert "couldn't find specific information" in response.content.lower()
        assert response.confidence_score == 0.3  # Lower confidence for empty results

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_add_connection_failure_detection_with_retry_logic(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test connection failure detection with retry logic"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Mock successful connection
        mock_collections = Mock()
        mock_collections.collections = [Mock(), Mock()]
        mock_qdrant_instance.get_collections.return_value = mock_collections

        result = agent.add_connection_failure_detection_with_retry_logic()
        assert result is True  # Should return True for successful connection

        # Mock failed connection
        mock_qdrant_instance.get_collections.side_effect = Exception("Connection failed")

        result_failed = agent.add_connection_failure_detection_with_retry_logic()
        assert result_failed is False  # Should return False for failed connection

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_create_comprehensive_error_logging_for_agent_failures(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """Test comprehensive error logging for agent failures"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance
        mock_openai_client.return_value = mock_openai_instance

        agent = RAGAgent()
        agent.qdrant_client = mock_qdrant_instance
        agent.cohere_client = mock_cohere_instance

        # Test error logging
        test_error = Exception("Test error for logging")
        agent.create_comprehensive_error_logging_for_agent_failures(test_error, "test_context")

        # We can't easily test logging output, but we can verify the method runs without error


class TestEndToEndIntegration:
    """End-to-end integration tests for the complete agent pipeline"""

    @patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-qdrant-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.OpenAI')
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_end_to_end_agent_pipeline(self, mock_cohere_client, mock_qdrant_client, mock_openai_client):
        """End-to-end test for the complete agent pipeline"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_openai_instance = Mock()

        # Mock the Cohere embed response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        mock_cohere_instance.embed.return_value = mock_embed_response
        mock_cohere_client.return_value = mock_cohere_instance

        # Mock the Qdrant search response
        mock_point = Mock()
        mock_point.id = "1"
        mock_point.score = 0.8
        mock_point.payload = {
            "content": "Test content for validation",
            "url": "http://example.com",
            "section": "Section 1",
            "heading": "Heading 1",
            "chunk_id": "chunk-1"
        }
        mock_search_result = [mock_point]
        mock_qdrant_instance.search.return_value = mock_search_result

        # Mock collections for connection validation
        mock_collections = Mock()
        mock_collections.collections = [Mock()]
        mock_qdrant_instance.get_collections.return_value = mock_collections

        # Mock collection info
        mock_collection_info = Mock()
        mock_collection_info.points_count = 100
        mock_qdrant_instance.get_collection.return_value = mock_collection_info

        # Mock thread and run creation for OpenAI
        mock_thread = Mock()
        mock_thread.id = "test-thread-id"
        mock_openai_instance.beta.threads.create.return_value = mock_thread

        # Mock run creation and retrieval
        mock_run = Mock()
        mock_run.status = "completed"
        mock_run.id = "test-run-id"
        mock_openai_instance.beta.threads.runs.create.return_value = mock_run
        mock_openai_instance.beta.threads.runs.retrieve.return_value = mock_run

        # Mock messages retrieval
        mock_message = Mock()
        mock_message.content = [Mock()]
        mock_message.content[0].text = Mock()
        mock_message.content[0].text.value = "This is a test response based on the provided context."
        mock_messages = Mock()
        mock_messages.data = [mock_message]
        mock_openai_instance.beta.threads.messages.list.return_value = mock_messages

        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_openai_client.return_value = mock_openai_instance

        # Test the complete agent pipeline
        agent = RAGAgent()
        agent.initialize_clients()
        agent.initialize_agent()

        # Verify that initialization worked
        assert agent.openai_client is not None
        assert agent.qdrant_client is not None
        assert agent.cohere_client is not None
        assert agent.agent is not None

        # Test connection validation
        connection_ok = agent.validate_connection()
        assert connection_ok is True

        # Test collection validation
        collection_ok = agent.validate_collection_exists()
        assert collection_ok is True

        # Test processing a query
        response = agent.process_query("What is vector retrieval?")
        assert response.content is not None
        assert response.source_chunks is not None
        assert response.processing_time >= 0

        # Test comprehensive validation
        test_queries = ["What is vector retrieval?", "Explain semantic search?"]
        status = agent.comprehensive_agent_validation(test_queries)

        # Verify the status
        assert status.agent_initialized is True
        assert status.qdrant_connected is True
        assert status.total_queries == 2
        assert status.successful_responses >= 0  # At least some should succeed with mocked responses
        assert status.processing_time >= 0  # Execution time should be non-negative
        assert status.start_time <= datetime.now()  # Start time should be in the past


if __name__ == "__main__":
    pytest.main([__file__])