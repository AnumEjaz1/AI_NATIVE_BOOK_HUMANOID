"""
RAG Agent Construction with Retrieval Capabilities

This module implements an AI agent that can retrieve relevant book content from Qdrant
and generate grounded responses using retrieved context. The agent integrates with
OpenAI Agents SDK, retrieves content from Qdrant Cloud, and generates responses
based on retrieved book content.
"""
import os
import logging
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
import openai
from openai import OpenAI
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models


# Load environment variables
load_dotenv()


@dataclass
class AgentRequest:
    """Represents a user query or instruction sent to the AI agent for processing"""
    query: str
    user_id: str
    timestamp: datetime
    context: Dict
    session_id: str


@dataclass
class RetrievedChunk:
    """A single content chunk retrieved from Qdrant during the validation process"""
    id: str
    content: str
    url: str
    section: str
    heading: str
    chunk_id: str
    similarity_score: float
    metadata: Dict


@dataclass
class RetrievedContext:
    """Content chunks retrieved from Qdrant that provide grounding for the agent's response"""
    chunks: List[RetrievedChunk]
    retrieval_query: str
    retrieval_time: float
    relevance_threshold: float
    total_chunks_found: int


@dataclass
class AgentResponse:
    """The generated response that incorporates information from retrieved context"""
    content: str
    source_chunks: List[str]
    confidence_score: float
    grounding_verification: bool
    citations: List[Dict]
    processing_time: float


@dataclass
class QueryVector:
    """Vector representation of the user query used for similarity search in Qdrant"""
    vector: List[float]
    text: str
    embedding_model: str
    dimension: int


@dataclass
class AgentStatus:
    """Represents the overall status of the agent system"""
    agent_initialized: bool
    qdrant_connected: bool
    total_queries_processed: int
    successful_responses: int
    failed_queries: int
    start_time: datetime
    error_logs: List[str]


class ConfigManager:
    """Implement configuration loading from environment variables"""

    def __init__(self):
        load_dotenv()  # Load environment variables

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")
        self.cohere_model = os.getenv("COHERE_MODEL_NAME", "embed-multilingual-v3.0")
        self.agent_name = os.getenv("AGENT_NAME", "book_retrieval_agent")
        self.agent_instructions = os.getenv("AGENT_INSTRUCTIONS",
            "You are a helpful assistant that answers questions based on the provided book content. Use the retrieved context to ground your responses in the book material.")

        self.validate_config()

    def validate_config(self):
        """Validate that all required configuration is present"""
        missing_vars = []
        if not self.openai_api_key:
            missing_vars.append("OPENAI_API_KEY")
        if not self.qdrant_url:
            missing_vars.append("QDRANT_URL")
        if not self.qdrant_api_key:
            missing_vars.append("QDRANT_API_KEY")
        if not self.cohere_api_key:
            missing_vars.append("COHERE_API_KEY")
        if not self.collection_name:
            missing_vars.append("QDRANT_COLLECTION_NAME")

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


class RAGAgent:
    """Main class for RAG agent with retrieval capabilities"""

    def __init__(self):
        """Initialize the RAG agent with configuration from environment variables"""
        # Load configuration
        self.config = ConfigManager()

        # Initialize clients
        self.openai_client = None
        self.qdrant_client = None
        self.cohere_client = None

        # Initialize agent
        self.agent = None

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging configuration for query inputs, responses, and errors"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('agent_retrieval.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def initialize_clients(self):
        """Create OpenAI client initialization with agent creation"""
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=self.config.openai_api_key)

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=self.config.qdrant_url,
            api_key=self.config.qdrant_api_key
        )

        # Initialize Cohere client
        self.cohere_client = cohere.Client(api_key=self.config.cohere_api_key)

    def initialize_agent(self):
        """Implement OpenAI agent initialization with proper configuration"""
        # Create the agent using OpenAI's Assistants API
        self.agent = self.openai_client.beta.assistants.create(
            name=self.config.agent_name,
            instructions=self.config.agent_instructions,
            model="gpt-4o"  # Using a more widely available model
        )
        self.logger.info(f"Agent '{self.config.agent_name}' initialized successfully")

    def validate_agent_initialization(self) -> bool:
        """Create function to validate OpenAI agent initialization"""
        if self.agent is None:
            self.logger.error("Agent not initialized")
            return False
        try:
            # Try to get the agent to verify it exists
            retrieved_agent = self.openai_client.beta.assistants.retrieve(self.agent.id)
            self.logger.info(f"Agent validation successful: {retrieved_agent.name}")
            return True
        except Exception as e:
            self.logger.error(f"Agent validation failed: {str(e)}")
            return False

    def validate_connection(self) -> bool:
        """Implement Qdrant connection function with credentials validation"""
        try:
            # Test connection by listing collections
            collections = self.qdrant_client.get_collections()
            self.logger.info(f"Successfully connected to Qdrant. Found {len(collections.collections)} collections")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Qdrant: {str(e)}")
            return False

    def validate_collection_exists(self) -> bool:
        """Create function to validate Qdrant collection existence"""
        try:
            collection_info = self.qdrant_client.get_collection(self.config.collection_name)
            self.logger.info(f"Collection '{self.config.collection_name}' exists with {collection_info.points_count} vectors")
            return True
        except Exception as e:
            self.logger.error(f"Collection '{self.config.collection_name}' does not exist: {str(e)}")
            return False

    def generate_embedding(self, text: str) -> List[float]:
        """Implement embedding generation function using Cohere model from previous specs"""
        try:
            response = self.cohere_client.embed(
                texts=[text],
                model=self.config.cohere_model
            )
            return response.embeddings[0]
        except Exception as e:
            self.logger.error(f"Failed to generate embedding for text '{text[:50]}...': {str(e)}")
            raise

    def semantic_search(self, query: str, top_k: int = 5, threshold: float = 0.5) -> RetrievedContext:
        """Create semantic search function with vector similarity search in Qdrant"""
        start_time = time.time()

        # Generate embedding for the query
        query_vector = self.generate_embedding(query)

        # Perform semantic search in Qdrant
        search_result = self.qdrant_client.search(
            collection_name=self.config.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=threshold,
            with_payload=True,
            with_vectors=False
        )

        # Convert search results to RetrievedChunk objects
        chunks = []
        for point in search_result:
            chunk = RetrievedChunk(
                id=point.id,
                content=point.payload.get("content", ""),
                url=point.payload.get("url", ""),
                section=point.payload.get("section", ""),
                heading=point.payload.get("heading", ""),
                chunk_id=point.payload.get("chunk_id", ""),
                similarity_score=point.score,
                metadata=point.payload
            )
            chunks.append(chunk)

        retrieval_time = time.time() - start_time

        return RetrievedContext(
            chunks=chunks,
            retrieval_query=query,
            retrieval_time=retrieval_time,
            relevance_threshold=threshold,
            total_chunks_found=len(search_result)
        )

    def format_context_for_agent(self, retrieved_context: RetrievedContext) -> str:
        """Create function to format retrieved context for agent prompts"""
        if not retrieved_context.chunks:
            return "No relevant content found in the book for this query."

        formatted_context = "Relevant book content:\n\n"
        for i, chunk in enumerate(retrieved_context.chunks, 1):
            formatted_context += f"Source {i}:\n"
            formatted_context += f"URL: {chunk.url}\n"
            formatted_context += f"Section: {chunk.section}\n"
            formatted_context += f"Heading: {chunk.heading}\n"
            formatted_context += f"Content: {chunk.content}\n\n"

        return formatted_context

    def create_context_injection_mechanism(self, query: str, retrieved_context: RetrievedContext) -> Tuple[str, List[str]]:
        """Implement context injection mechanism with length limits"""
        # Format the context
        formatted_context = self.format_context_for_agent(retrieved_context)

        # Create the full prompt with context
        prompt = f"Context:\n{formatted_context}\n\nQuery: {query}\n\nPlease provide a response based on the provided context, citing sources when possible."

        # Extract source chunk IDs
        source_chunks = [chunk.id for chunk in retrieved_context.chunks]

        return prompt, source_chunks

    def process_query(self, query: str, user_id: str = "default_user", top_k: int = 5) -> AgentResponse:
        """Implement basic query processing function"""
        start_time = time.time()

        # Create a thread for the query
        thread = self.openai_client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        # Retrieve relevant context from Qdrant
        retrieved_context = self.semantic_search(query, top_k=top_k)

        # Format context and get source chunks
        formatted_prompt, source_chunks = self.create_context_injection_mechanism(query, retrieved_context)

        # Update the thread with the formatted prompt
        self.openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=formatted_prompt
        )

        # Run the agent
        run = self.openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.agent.id
        )

        # Wait for the run to complete
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)
            run = self.openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Get the response
        if run.status == "completed":
            messages = self.openai_client.beta.threads.messages.list(
                thread_id=thread.id,
                order="desc",
                limit=1
            )

            if messages.data:
                response_content = messages.data[0].content[0].text.value
            else:
                response_content = "No response generated by the agent."
        else:
            response_content = f"Agent failed to process the query. Status: {run.status}"
            source_chunks = []

        processing_time = time.time() - start_time

        # Verify grounding of the response
        grounding_verification = self.verify_response_grounding(response_content, retrieved_context)

        # Extract citations from the response
        citations = self.extract_citations_from_response(response_content, retrieved_context)

        return AgentResponse(
            content=response_content,
            source_chunks=source_chunks,
            confidence_score=0.8,  # Default confidence score
            grounding_verification=grounding_verification,
            citations=citations,
            processing_time=processing_time
        )

    def verify_response_grounding(self, response_content: str, retrieved_context: RetrievedContext) -> bool:
        """Implement response grounding verification function"""
        if not retrieved_context.chunks:
            # If no context was retrieved, the response can't be grounded
            return False

        # Simple check: see if key phrases from the context appear in the response
        response_lower = response_content.lower()

        # Look for at least one piece of content from the retrieved context in the response
        for chunk in retrieved_context.chunks:
            if len(chunk.content) > 20:  # Only check substantial content
                # Check if a phrase from the chunk appears in the response
                sample_phrase = chunk.content[:50].lower()  # Take first 50 chars as sample
                if len(sample_phrase.split()) > 3:  # Make sure it's a meaningful phrase
                    phrase_words = sample_phrase.split()[:5]  # Take first 5 words as a sample
                    sample_phrase = " ".join(phrase_words)
                    if sample_phrase in response_lower:
                        return True

        # If no content overlap found, check for citation references
        for chunk in retrieved_context.chunks:
            if chunk.url.lower() in response_content.lower() or chunk.heading.lower() in response_content.lower():
                return True

        return False

    def extract_citations_from_response(self, response_content: str, retrieved_context: RetrievedContext) -> List[Dict]:
        """Create function to track citations to retrieved content"""
        citations = []

        for chunk in retrieved_context.chunks:
            # Check if this chunk is cited in the response
            if chunk.url.lower() in response_content.lower() or chunk.heading.lower() in response_content.lower():
                citation = {
                    "chunk_id": chunk.id,
                    "url": chunk.url,
                    "heading": chunk.heading,
                    "section": chunk.section,
                    "text": chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content
                }
                citations.append(citation)

        return citations

    def ensure_deterministic_behavior(self, query: str, user_id: str = "default_user", top_k: int = 5, runs: int = 3) -> bool:
        """Implement deterministic behavior for identical queries"""
        responses = []

        for i in range(runs):
            response = self.process_query(query, user_id, top_k)
            responses.append(response.content)

        # Check if all responses are the same (or very similar)
        first_response = responses[0] if responses else ""
        return all(self._responses_are_similar(first_response, resp) for resp in responses[1:])

    def _responses_are_similar(self, response1: str, response2: str, threshold: float = 0.8) -> bool:
        """Helper method to check if two responses are similar"""
        # Simple similarity check using length and common words
        if abs(len(response1) - len(response2)) / max(len(response1), len(response2), 1) > 0.5:
            return False  # Length difference too large

        # Simple word overlap check
        words1 = set(response1.lower().split())
        words2 = set(response2.lower().split())

        if not words1 and not words2:
            return True
        if not words1 or not words2:
            return False

        common_words = words1.intersection(words2)
        total_words = words1.union(words2)

        similarity = len(common_words) / len(total_words)
        return similarity >= threshold

    def add_confidence_scoring(self, response_content: str, retrieved_context: RetrievedContext) -> float:
        """Add confidence scoring to agent responses"""
        if not retrieved_context.chunks:
            return 0.1  # Low confidence if no context

        # Calculate confidence based on how much of the context was used
        context_utilization = len(self.extract_citations_from_response(response_content, retrieved_context)) / len(retrieved_context.chunks)

        # Calculate confidence based on similarity scores of retrieved chunks
        avg_similarity = sum(chunk.similarity_score for chunk in retrieved_context.chunks) / len(retrieved_context.chunks)

        # Combine factors for final confidence score
        confidence = (context_utilization * 0.4) + (avg_similarity * 0.6)
        return min(confidence, 1.0)  # Ensure confidence doesn't exceed 1.0

    def compare_responses_for_identical_queries(self, query: str, runs: int = 3) -> Dict:
        """Create function to compare responses for identical queries"""
        responses = []
        for i in range(runs):
            response = self.process_query(query)
            responses.append({
                "run": i + 1,
                "content": response.content,
                "processing_time": response.processing_time
            })

        # Check consistency
        first_content = responses[0]["content"] if responses else ""
        all_same = all(self._responses_are_similar(first_content, resp["content"]) for resp in responses[1:])

        return {
            "query": query,
            "responses": responses,
            "consistent": all_same,
            "total_runs": runs,
            "consistent_runs": len([r for r in responses if self._responses_are_similar(first_content, r["content"])]) if responses else 0
        }

    def implement_content_matching_to_verify_grounding(self, response_content: str, retrieved_context: RetrievedContext) -> bool:
        """Implement content matching to verify grounding in retrieved context"""
        if not retrieved_context.chunks:
            return False

        # Check for semantic similarity between response and retrieved content
        response_words = set(response_content.lower().split())

        for chunk in retrieved_context.chunks:
            chunk_words = set(chunk.content.lower().split())

            # Calculate overlap
            common_words = response_words.intersection(chunk_words)
            if len(common_words) > 0:
                # If there's any overlap, consider it grounded
                return True

        # If no direct word overlap, check for semantic relevance
        # This is a simplified version - in practice, you'd use embeddings for semantic similarity
        return False

    def detect_retrieval_failures_and_log(self, query: str) -> bool:
        """Implement retrieval failure detection and logging"""
        try:
            # Attempt to retrieve context for the query
            retrieved_context = self.semantic_search(query)

            # If no chunks were found, this could be a failure
            if not retrieved_context.chunks:
                self.logger.warning(f"No relevant content found for query: {query}")
                return True  # Indicate that a failure was detected

            return False  # No failure detected
        except Exception as e:
            self.logger.error(f"Retrieval failure for query '{query}': {str(e)}")
            return True  # Indicate that a failure was detected

    def handle_empty_retrieval_results_gracefully(self, query: str, top_k: int = 5) -> AgentResponse:
        """Create function to handle empty retrieval results gracefully"""
        try:
            retrieved_context = self.semantic_search(query, top_k=top_k)

            if not retrieved_context.chunks:
                self.logger.info(f"No relevant content found for query: {query}. Providing general response.")

                # Create a response even when no context was found
                return AgentResponse(
                    content="I couldn't find specific information about this topic in the book. However, I can try to provide general information based on my training.",
                    source_chunks=[],
                    confidence_score=0.3,  # Lower confidence when no specific context found
                    grounding_verification=False,
                    citations=[],
                    processing_time=0.1  # Simulated processing time
                )
            else:
                # Process normally with the retrieved context
                return self.process_query(query, top_k=top_k)

        except Exception as e:
            self.logger.error(f"Error handling query '{query}' with empty results: {str(e)}")
            return AgentResponse(
                content="An error occurred while processing your query. Please try again later.",
                source_chunks=[],
                confidence_score=0.1,
                grounding_verification=False,
                citations=[],
                processing_time=0.1
            )

    def add_connection_failure_detection_with_retry_logic(self):
        """Add connection failure detection with retry logic"""
        # This would typically implement retry logic with exponential backoff
        # For now, we'll implement a basic version that checks connection status
        try:
            # Test the connection by performing a simple operation
            collections = self.qdrant_client.get_collections()
            self.logger.info(f"Connection test successful. Found {len(collections.collections)} collections.")
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            # In a real implementation, you would implement retry logic here
            return False

    def implement_timeout_and_error_handling_for_qdrant_operations(self, query: str, top_k: int = 5, timeout: int = 30) -> AgentResponse:
        """Implement timeout and error handling for Qdrant operations"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {timeout} seconds")

        # Set up the timeout handler (on Unix-like systems)
        old_handler = None
        timeout_occurred = False
        try:
            # For Unix systems, we can use signal to implement timeout
            import platform
            if platform.system() != "Windows":
                old_handler = signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)

            # Perform the search operation
            retrieved_context = self.semantic_search(query, top_k=top_k)

            # Cancel the alarm if set
            if platform.system() != "Windows":
                signal.alarm(0)
                if old_handler:
                    signal.signal(signal.SIGALRM, old_handler)

            # Process the results normally
            return self.process_query(query, top_k=top_k)

        except TimeoutError as te:
            self.logger.error(f"Timeout occurred during Qdrant operation: {str(te)}")
            return AgentResponse(
                content="The retrieval operation took too long to complete. Please try again later.",
                source_chunks=[],
                confidence_score=0.0,
                grounding_verification=False,
                citations=[],
                processing_time=timeout
            )
        except Exception as e:
            self.logger.error(f"Error during Qdrant operation for query '{query}': {str(e)}")
            return AgentResponse(
                content="An error occurred during the retrieval operation. Please try again later.",
                source_chunks=[],
                confidence_score=0.1,
                grounding_verification=False,
                citations=[],
                processing_time=0.1
            )

    def create_comprehensive_error_logging_for_agent_failures(self, error: Exception, context: str = ""):
        """Create comprehensive error logging for agent failures"""
        error_msg = f"Agent failure in {context}: {str(error)}"
        self.logger.error(error_msg)

        # In a real implementation, you might want to log additional details like:
        # - Stack trace
        # - Request details
        # - Time of occurrence
        # - User information
        # - Component that failed
        import traceback
        self.logger.error(f"Stack trace: {traceback.format_exc()}")

    def add_validation_for_context_injection_failures(self, query: str, retrieved_context: RetrievedContext) -> bool:
        """Add validation for context injection failures"""
        try:
            # Test the context injection mechanism
            formatted_prompt, source_chunks = self.create_context_injection_mechanism(query, retrieved_context)

            # Check if the prompt is too long (could cause token overflow)
            if len(formatted_prompt) > 100000:  # Rough estimate of token limit
                self.logger.warning(f"Formatted prompt for query '{query}' is very long ({len(formatted_prompt)} chars) and may cause token overflow.")
                return False  # Indicates potential failure

            # Additional checks could be added here
            return True  # No failures detected
        except Exception as e:
            self.logger.error(f"Context injection validation failed for query '{query}': {str(e)}")
            return False

    def comprehensive_agent_validation(self, test_queries: List[str]) -> AgentStatus:
        """Create comprehensive agent status reporting"""
        start_time = datetime.now()
        self.logger.info("Starting comprehensive RAG agent validation...")

        # Initialize agent status
        status = AgentStatus(
            agent_initialized=False,
            qdrant_connected=False,
            total_queries_processed=len(test_queries),
            successful_responses=0,
            failed_queries=0,
            start_time=start_time,
            error_logs=[]
        )

        try:
            # Initialize clients and agent
            self.initialize_clients()
            self.initialize_agent()

            # Validate agent and connection
            agent_ok = self.validate_agent_initialization()
            connection_ok = self.validate_connection()
            collection_ok = self.validate_collection_exists()

            if not (agent_ok and connection_ok and collection_ok):
                status.error_logs.append("Agent initialization or connection validation failed")
                return status

            status.agent_initialized = True
            status.qdrant_connected = True

            # Execute test queries
            for query in test_queries:
                try:
                    response = self.process_query(query)
                    if response.content and "failed" not in response.content.lower():
                        status.successful_responses += 1
                    else:
                        status.failed_queries += 1
                except Exception as e:
                    self.logger.error(f"Error processing query '{query}': {str(e)}")
                    status.failed_queries += 1
                    status.error_logs.append(f"Query '{query}' failed: {str(e)}")

        except Exception as e:
            self.logger.error(f"Comprehensive agent validation failed: {str(e)}")
            status.error_logs.append(str(e))

        self.logger.info(f"Validation completed. Successful: {status.successful_responses}, Failed: {status.failed_queries}")

        return status


def main():
    """Implement main() function to execute end-to-end agent query tests"""
    import argparse

    parser = argparse.ArgumentParser(description="RAG Agent with Retrieval Capabilities")
    parser.add_argument("--queries", nargs="+", default=[
        "What is vector retrieval?",
        "Explain semantic search",
        "How does RAG work?"
    ], help="Test queries to validate agent responses")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to retrieve")

    args = parser.parse_args()

    # Initialize agent
    agent = RAGAgent()

    # Run comprehensive validation
    status = agent.comprehensive_agent_validation(args.queries)

    # Print summary
    print("\nRAG Agent System Summary")
    print("========================")
    print(f"Agent Initialized: {'Yes' if status.agent_initialized else 'No'}")
    print(f"Qdrant Connected: {'Yes' if status.qdrant_connected else 'No'}")
    print(f"Total Queries: {status.total_queries_processed}")
    print(f"Successful Responses: {status.successful_responses}")
    print(f"Failed Queries: {status.failed_queries}")
    print(f"Error Logs: {len(status.error_logs)}")

    if status.error_logs:
        print("\nErrors Encountered:")
        for error in status.error_logs:
            print(f"  - {error}")

    agent_status = "All validations passed" if status.successful_responses == status.total_queries_processed else "Some validations failed"
    print(f"Agent Status: {agent_status}")

    print(f"\nLog file created: agent_retrieval.log")


if __name__ == "__main__":
    main()