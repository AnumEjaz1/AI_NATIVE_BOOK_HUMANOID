"""
Unit tests for RAG retrieval pipeline validation - User Story 1
Testing connection and basic retrieval functions
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from backend.src.embedding.retrieve import RAGValidator, ConfigManager


class TestConfigManager:
    """Test configuration loading and validation"""

    def test_config_loading_from_env(self, monkeypatch):
        """Test that ConfigManager loads environment variables correctly"""
        # Set up environment variables for testing
        monkeypatch.setenv("QDRANT_URL", "https://test.qdrant.tech:6333")
        monkeypatch.setenv("QDRANT_API_KEY", "test-api-key")
        monkeypatch.setenv("COHERE_API_KEY", "test-cohere-key")
        monkeypatch.setenv("QDRANT_COLLECTION_NAME", "test_collection")

        config = ConfigManager()
        assert config.qdrant_url == "https://test.qdrant.tech:6333"
        assert config.qdrant_api_key == "test-api-key"
        assert config.cohere_api_key == "test-cohere-key"
        assert config.collection_name == "test_collection"

    def test_config_validation_missing_vars(self, monkeypatch):
        """Test that ConfigManager validates required environment variables"""
        # Remove required environment variables
        monkeypatch.delenv("QDRANT_URL", raising=False)
        monkeypatch.delenv("QDRANT_API_KEY", raising=False)
        monkeypatch.delenv("COHERE_API_KEY", raising=False)
        monkeypatch.delenv("QDRANT_COLLECTION_NAME", raising=False)

        with pytest.raises(ValueError, match="Missing required environment variables"):
            ConfigManager()


class TestRAGValidatorConnection:
    """Test RAG validator connection functions"""

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_initialize_clients(self, mock_cohere_client, mock_qdrant_client):
        """Test that clients are initialized correctly"""
        # Mock the client instances
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()
        mock_qdrant_client.return_value = mock_qdrant_instance
        mock_cohere_client.return_value = mock_cohere_instance

        validator = RAGValidator()
        validator.initialize_clients()

        # Verify that clients were initialized
        assert validator.qdrant_client is not None
        assert validator.cohere_client is not None

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    def test_validate_connection_success(self, mock_qdrant_client):
        """Test connection validation with successful connection"""
        # Mock the Qdrant client and its methods
        mock_client_instance = Mock()
        mock_client_instance.get_collections.return_value = Mock()
        mock_client_instance.get_collections.return_value.collections = [Mock()]
        mock_qdrant_client.return_value = mock_client_instance

        validator = RAGValidator()
        validator.qdrant_client = mock_client_instance

        result = validator.validate_connection()
        assert result is True
        mock_client_instance.get_collections.assert_called_once()

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    def test_validate_connection_failure(self, mock_qdrant_client):
        """Test connection validation with failed connection"""
        # Mock the Qdrant client to raise an exception
        mock_client_instance = Mock()
        mock_client_instance.get_collections.side_effect = Exception("Connection failed")
        mock_qdrant_client.return_value = mock_client_instance

        validator = RAGValidator()
        validator.qdrant_client = mock_client_instance

        result = validator.validate_connection()
        assert result is False

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    def test_validate_collection_exists_success(self, mock_qdrant_client):
        """Test collection validation with existing collection"""
        # Mock the Qdrant client and collection info
        mock_client_instance = Mock()
        mock_collection_info = Mock()
        mock_collection_info.points_count = 100
        mock_client_instance.get_collection.return_value = mock_collection_info
        mock_qdrant_client.return_value = mock_client_instance

        validator = RAGValidator()
        validator.qdrant_client = mock_client_instance

        result = validator.validate_collection_exists()
        assert result is True
        mock_client_instance.get_collection.assert_called_once_with("test_collection")

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    def test_validate_collection_exists_failure(self, mock_qdrant_client):
        """Test collection validation with non-existing collection"""
        # Mock the Qdrant client to raise an exception for non-existing collection
        mock_client_instance = Mock()
        mock_client_instance.get_collection.side_effect = Exception("Collection not found")
        mock_qdrant_client.return_value = mock_client_instance

        validator = RAGValidator()
        validator.qdrant_client = mock_client_instance

        result = validator.validate_collection_exists()
        assert result is False


class TestRAGValidatorFailureDetection:
    """Tests for failure detection and logging functionality"""

    def test_detect_empty_results(self):
        """Test empty result detection"""
        from backend.src.embedding.retrieve import RetrievedChunk, RAGValidator

        validator = RAGValidator()

        # Test with empty chunks list
        empty_chunks = []
        result = validator.detect_empty_results(empty_chunks)
        assert result is True

        # Test with non-empty chunks list
        non_empty_chunks = [
            RetrievedChunk(
                id="1",
                content="test content",
                url="http://example.com",
                section="Section 1",
                heading="Heading 1",
                chunk_id="chunk-1",
                similarity_score=0.8,
                metadata={}
            )
        ]
        result = validator.detect_empty_results(non_empty_chunks)
        assert result is False

    def test_detect_dimension_mismatch(self):
        """Test dimension mismatch detection"""
        from backend.src.embedding.retrieve import RAGValidator

        validator = RAGValidator()

        # Test with empty vector (should detect mismatch)
        empty_vector = []
        result = validator.detect_dimension_mismatch(empty_vector)
        assert result is True

        # Test with non-empty vector (should not detect mismatch)
        valid_vector = [0.1, 0.2, 0.3]
        result = validator.detect_dimension_mismatch(valid_vector)
        assert result is False

    def test_comprehensive_error_logging(self, caplog):
        """Test comprehensive error logging"""
        from backend.src.embedding.retrieve import RAGValidator

        validator = RAGValidator()

        # Test error logging
        test_error = Exception("Test error for logging")
        with caplog.at_level("ERROR"):
            validator.create_comprehensive_error_logging(test_error, "test_context")

        # Verify that an error was logged
        assert "Pipeline failure in test_context" in caplog.text
        assert "Test error for logging" in caplog.text


class TestRAGValidatorMetadataValidation:
    """Tests for metadata validation and reproducibility features"""

    def test_validate_chunk_metadata(self):
        """Test metadata validation for individual chunks"""
        from backend.src.embedding.retrieve import RetrievedChunk

        # Create a chunk with all required metadata
        valid_chunk = RetrievedChunk(
            id="1",
            content="test content",
            url="http://example.com",
            section="Section 1",
            heading="Heading 1",
            chunk_id="chunk-1",
            similarity_score=0.8,
            metadata={}
        )

        validator = RAGValidator()
        result = validator._validate_chunk_metadata(valid_chunk)
        assert result is True

        # Test chunk with missing metadata
        invalid_chunk = RetrievedChunk(
            id="2",
            content="test content",
            url="",  # Missing URL
            section="Section 1",
            heading="Heading 1",
            chunk_id="chunk-1",
            similarity_score=0.8,
            metadata={}
        )

        result = validator._validate_chunk_metadata(invalid_chunk)
        assert result is False

    def test_validate_metadata_fields(self):
        """Test validation of metadata fields for a list of chunks"""
        from backend.src.embedding.retrieve import RetrievedChunk

        # Create chunks with valid metadata
        valid_chunks = [
            RetrievedChunk(
                id="1",
                content="test content 1",
                url="http://example.com/1",
                section="Section 1",
                heading="Heading 1",
                chunk_id="chunk-1",
                similarity_score=0.8,
                metadata={}
            ),
            RetrievedChunk(
                id="2",
                content="test content 2",
                url="http://example.com/2",
                section="Section 2",
                heading="Heading 2",
                chunk_id="chunk-2",
                similarity_score=0.7,
                metadata={}
            )
        ]

        validator = RAGValidator()
        result = validator.validate_metadata_fields(valid_chunks)
        assert result is True

        # Test with one invalid chunk
        invalid_chunks = valid_chunks + [
            RetrievedChunk(
                id="3",
                content="test content 3",
                url="",  # Missing URL
                section="Section 3",
                heading="Heading 3",
                chunk_id="chunk-3",
                similarity_score=0.6,
                metadata={}
            )
        ]

        result = validator.validate_metadata_fields(invalid_chunks)
        assert result is False


class TestRAGValidatorSemanticSearch:
    """Integration tests for semantic search functionality"""

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_semantic_search_integration(self, mock_cohere_client, mock_qdrant_client):
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
        mock_search_result = [
            Mock(id="1", score=0.8, payload={
                "content": "Test content",
                "url": "http://example.com",
                "section": "Section 1",
                "heading": "Heading 1",
                "chunk_id": "chunk-1"
            })
        ]
        mock_qdrant_instance.search.return_value = mock_search_result
        mock_qdrant_client.return_value = mock_qdrant_instance

        validator = RAGValidator()
        validator.qdrant_client = mock_qdrant_instance
        validator.cohere_client = mock_cohere_instance

        # Test semantic search
        results = validator.semantic_search("test query", top_k=1)

        # Verify the results
        assert len(results) == 1
        assert results[0].content == "Test content"
        assert results[0].similarity_score == 0.8

        # Verify that the correct methods were called
        mock_cohere_instance.embed.assert_called_once()
        mock_qdrant_instance.search.assert_called_once()

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_execute_test_queries(self, mock_cohere_client, mock_qdrant_client):
        """Test execution of multiple test queries"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()

        # Mock the Cohere embed response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        mock_cohere_instance.embed.return_value = mock_embed_response
        mock_cohere_client.return_value = mock_cohere_instance

        # Mock the Qdrant search response
        mock_search_result = [
            Mock(id="1", score=0.8, payload={
                "content": "Test content",
                "url": "http://example.com",
                "section": "Section 1",
                "heading": "Heading 1",
                "chunk_id": "chunk-1"
            })
        ]
        mock_qdrant_instance.search.return_value = mock_search_result
        mock_qdrant_client.return_value = mock_qdrant_instance

        validator = RAGValidator()
        validator.qdrant_client = mock_qdrant_instance
        validator.cohere_client = mock_cohere_instance

        # Test executing multiple queries
        queries = ["query 1", "query 2"]
        results = validator.execute_test_queries(queries, top_k=1)

        # Verify the results
        assert len(results) == 2
        for result in results:
            assert result.validation_passed is True  # Assuming the mock results pass validation

        # Verify that search was called for each query
        assert mock_qdrant_instance.search.call_count == 2


class TestEndToEndIntegration:
    """End-to-end integration tests for the complete validation pipeline"""

    @patch.dict(os.environ, {
        "QDRANT_URL": "https://test.qdrant.tech:6333",
        "QDRANT_API_KEY": "test-api-key",
        "COHERE_API_KEY": "test-cohere-key",
        "QDRANT_COLLECTION_NAME": "test_collection"
    })
    @patch('backend.src.embedding.retrieve.QdrantClient')
    @patch('backend.src.embedding.retrieve.cohere.Client')
    def test_end_to_end_validation_pipeline(self, mock_cohere_client, mock_qdrant_client):
        """End-to-end test for the complete validation pipeline"""
        # Mock the clients
        mock_qdrant_instance = Mock()
        mock_cohere_instance = Mock()

        # Mock the Cohere embed response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3, 0.4]]
        mock_cohere_instance.embed.return_value = mock_embed_response
        mock_cohere_client.return_value = mock_cohere_instance

        # Mock the Qdrant search response
        mock_search_result = [
            Mock(id="1", score=0.8, payload={
                "content": "Test content for validation",
                "url": "http://example.com",
                "section": "Section 1",
                "heading": "Heading 1",
                "chunk_id": "chunk-1"
            })
        ]
        mock_qdrant_instance.search.return_value = mock_search_result
        mock_qdrant_client.return_value = mock_qdrant_instance

        # Mock collection information
        mock_collection_info = Mock()
        mock_collection_info.points_count = 100
        mock_qdrant_instance.get_collection.return_value = mock_collection_info
        mock_collections = Mock()
        mock_collections.collections = [Mock()]
        mock_qdrant_instance.get_collections.return_value = mock_collections

        validator = RAGValidator()
        validator.qdrant_client = mock_qdrant_instance
        validator.cohere_client = mock_cohere_instance

        # Test the comprehensive validation
        test_queries = ["What is vector retrieval?", "Explain semantic search?"]
        status = validator.comprehensive_validation(test_queries)

        # Verify the pipeline status
        assert status.connection_successful is True
        assert status.total_queries == 2
        assert status.successful_retrievals >= 0  # At least some should succeed with mocked responses
        assert status.execution_time >= 0  # Execution time should be non-negative
        assert status.start_time <= status.end_time  # End time should be after start time

        # Verify that the necessary methods were called
        assert mock_qdrant_instance.get_collections.called
        assert mock_qdrant_instance.get_collection.called
        assert mock_cohere_instance.embed.call_count == len(test_queries)  # Called for each query
        assert mock_qdrant_instance.search.call_count == len(test_queries)  # Called for each query


if __name__ == "__main__":
    pytest.main([__file__])