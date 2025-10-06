# Source Code

This directory contains the core implementation of the Enterprise RAG system.

## Structure

### `document_processing/`
Document ingestion, parsing, and quality detection:
- **parsers/**: Multi-format document parsers (PDF, DOCX, Excel, etc.)
- **quality_detection/**: OCR quality assessment, corruption detection
- **chunking/**: Hierarchical and semantic chunking strategies
- **metadata/**: Metadata extraction and schema validation

### `retrieval/`
Retrieval and search components:
- **embeddings/**: Embedding model wrappers and management
- **vector_stores/**: Vector database integrations (Qdrant, Weaviate, etc.)
- **hybrid_search/**: BM25 + vector search fusion strategies
- **reranking/**: Cross-encoder reranking for relevance optimization

### `generation/`
LLM generation and guardrails:
- **prompts/**: Production-tested prompt templates
- **guardrails/**: Output validation, fact-checking, safety filters
- **streaming/**: Streaming response handlers

### `orchestration/`
Pipeline orchestration and monitoring:
- **pipelines/**: End-to-end RAG pipelines
- **caching/**: Response and embedding caching strategies
- **monitoring/**: Logging, metrics, and distributed tracing

### `api/`
FastAPI application:
- **routes/**: API endpoint definitions
- **models/**: Pydantic models for request/response validation
- **middleware/**: Authentication, rate limiting, CORS

## Development Guidelines

1. **Type Safety**: Use type hints and Pydantic models throughout
2. **Modularity**: Keep components loosely coupled and testable
3. **Error Handling**: Implement comprehensive error handling and logging
4. **Documentation**: Add docstrings for all public functions and classes
5. **Testing**: Write unit tests for all core functionality
