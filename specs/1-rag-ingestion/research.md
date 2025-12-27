# Research Findings: RAG Website URL Ingestion, Embedding Generation, and Vector Storage

**Feature**: 1-rag-ingestion
**Created**: 2025-12-27

## Decision 1: Cohere Embedding Models

**Research Task**: Determine the most appropriate Cohere embedding model for text content

**Decision**: Use Cohere's `embed-multilingual-v3.0` model for text similarity

**Rationale**:
- The v3 model provides the latest improvements in semantic understanding
- Multilingual support ensures compatibility with diverse content
- Optimized for retrieval tasks with high-dimensional vectors
- Good balance between accuracy and cost

**Alternatives Considered**:
- OpenAI embeddings: More expensive, less specialized for multilingual content
- Hugging Face models: Require more infrastructure management
- Older Cohere models: Less accurate than latest versions

## Decision 2: Qdrant Vector Storage Schema

**Research Task**: Determine optimal schema for storing text chunks with metadata

**Decision**: Use Qdrant collections with structured payloads containing URL, heading, section, and content metadata

**Rationale**:
- Qdrant provides efficient vector search with metadata filtering
- Structured payloads allow for semantic search with metadata constraints
- Supports large-scale vector operations with good performance
- Cloud-hosted option available for easy deployment

**Alternatives Considered**:
- Pinecone: More expensive, less flexible metadata options
- Weaviate: More complex setup, different query language
- Chroma: Self-hosted only, less scalable for production

## Decision 3: Docusaurus Content Structure Targeting

**Research Task**: Determine common HTML structure patterns in Docusaurus sites for content extraction

**Decision**: Target main content areas using CSS selectors for `.main-wrapper`, `article.markdown`, and `.theme-doc-markdown` classes

**Rationale**:
- Docusaurus sites follow predictable patterns with standardized class names
- These selectors capture the primary content while avoiding navigation and headers
- Well-tested approach based on common Docusaurus themes
- Allows for fallback selectors if primary ones don't match

**Alternatives Considered**:
- Generic web scraping approaches: Less accurate, more noise in extracted content
- Manual URL-by-URL extraction: Not scalable for large sites

## Decision 4: Text Chunking Strategy

**Research Task**: Determine optimal chunk sizes and strategies for embedding generation

**Decision**: Use semantic chunking with 512-1024 token chunks and 20% overlap to preserve context

**Rationale**:
- Semantic chunks maintain meaning while fitting within model limits
- Overlap ensures context preservation across chunk boundaries
- 512-1024 token range balances context and embedding quality
- Cohere models handle this input size efficiently

**Alternatives Considered**:
- Fixed-size character chunks: May break context mid-sentence
- Sentence-based chunks: May create very uneven chunk sizes
- Paragraph-based chunks: May exceed model input limits

## Decision 5: URL Discovery Method

**Research Task**: Determine the most effective approach for discovering all pages on GitHub Pages sites

**Decision**: Use a combination of sitemap.xml parsing and web crawling with breadth-first search

**Rationale**:
- Sitemap.xml provides a comprehensive list of pages if available
- Web crawling discovers pages not listed in sitemaps
- Breadth-first search ensures proper depth control
- Handles relative URLs and navigation patterns effectively

**Alternatives Considered**:
- Manual URL lists: Not scalable or maintainable
- Single-page crawling: May miss deeply nested content

## Decision 6: Error Handling Strategy

**Research Task**: Determine appropriate error handling for API rate limits and network issues

**Decision**: Implement exponential backoff with jitter and circuit breaker pattern

**Rationale**:
- Exponential backoff prevents overwhelming APIs during rate limits
- Jitter prevents thundering herd problems
- Circuit breaker prevents cascading failures
- Allows for graceful degradation during partial outages

**Alternatives Considered**:
- Simple retry: May exacerbate rate limit issues
- No retry: Results in data loss during temporary outages

## Risk Assessment Findings

### API Rate Limits
- **Risk**: Cohere and Qdrant APIs have rate limits that could slow processing
- **Mitigation**: Implement request batching and exponential backoff
- **Monitoring**: Track API usage and adjust processing rate accordingly

### Large Content Handling
- **Risk**: Some pages may exceed embedding model input limits (typically 512-1024 tokens)
- **Mitigation**: Pre-process content to chunk before sending to embedding API
- **Validation**: Check content length before API calls

### Network Reliability
- **Risk**: GitHub Pages sites may be temporarily unavailable during processing
- **Mitigation**: Implement retry logic with circuit breaker pattern
- **Resilience**: Track processed URLs to avoid re-processing after failures