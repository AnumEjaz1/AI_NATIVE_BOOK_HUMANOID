from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class SourceDocument(BaseModel):
    """
    A document source referenced in the response
    """
    title: str = Field(..., description="Title of the source document", min_length=1)
    content: str = Field(..., description="Content snippet from the document", min_length=1)
    url: Optional[str] = Field(None, description="URL or path to the full document")
    score: Optional[float] = Field(None, description="Relevance score of the document", ge=0.0, le=1.0)

    @validator('score')
    def validate_score(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0 and 1')
        return v


class QueryRequest(BaseModel):
    """
    Represents a user's query to the RAG system
    """
    query: str = Field(..., description="The user's input text to be processed", min_length=1, max_length=10000)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional context or parameters for the query")
    user_id: Optional[str] = Field(None, description="Identifier for the user making the request")


class QueryResponse(BaseModel):
    """
    The RAG agent's response to a user query
    """
    response: str = Field(..., description="The agent's answer to the query", min_length=1)
    sources: Optional[List[SourceDocument]] = Field(None, description="List of source documents referenced")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional information about the response")
    query_id: Optional[str] = Field(None, description="Identifier for tracking the query")


class HealthStatus(BaseModel):
    """
    Health check response
    """
    status: str = Field("healthy", description="Health status of the service", pattern="^healthy$")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the check")

    @validator('status')
    def validate_status(cls, v):
        if v != "healthy":
            raise ValueError('Status must be "healthy"')
        return v

    @validator('timestamp')
    def validate_timestamp_format(cls, v):
        try:
            # Validate that it's a valid ISO format datetime
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('Timestamp must be in ISO 8601 format')
        return v