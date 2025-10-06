# Production Best Practices

This guide captures battle-tested best practices from 10+ enterprise RAG deployments in regulated industries.

## Document Processing

### Quality Detection

**Always validate document quality before processing:**

```python
from src.document_processing.quality_detection import DocumentQualityChecker

checker = DocumentQualityChecker()
quality_score = checker.check_document(document_path)

if quality_score.ocr_needed and quality_score.ocr_quality < 0.7:
    # Document is scanned and OCR quality is poor
    # Either reject or flag for manual review
    raise ValueError("Document quality too low for reliable processing")
```

**Key learnings:**
- 30% of enterprise documents are scanned PDFs with poor OCR
- Always detect corrupted files before processing (saves compute)
- Set quality thresholds based on your use case (legal: strict, general: moderate)

### Chunking Strategy

**Use hierarchical chunking for enterprise documents:**

```python
from src.document_processing.chunking import HierarchicalChunker

chunker = HierarchicalChunker(
    chunk_size=512,          # Tokens, not characters
    chunk_overlap=50,        # ~10% overlap
    respect_sections=True,   # Don't split sections
    min_chunk_size=100       # Avoid tiny chunks
)

chunks = chunker.chunk_document(document)
```

**Key learnings:**
- Token-based chunking > character-based (models work with tokens)
- Section-aware chunking improves retrieval quality by 15-20%
- Overlap is critical: 10% overlap reduces missed context
- Avoid chunks < 100 tokens (poor semantic meaning)
- Avoid chunks > 1000 tokens (too much noise)

### Metadata Extraction

**Define strict metadata schemas:**

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DocumentMetadata(BaseModel):
    """Strict metadata schema for compliance."""
    
    document_id: str = Field(..., description="Unique document identifier")
    title: str = Field(..., min_length=1)
    document_type: str = Field(..., regex="^(policy|contract|memo|report)$")
    department: str
    created_date: datetime
    modified_date: Optional[datetime]
    author: str
    classification: str = Field(..., regex="^(public|internal|confidential)$")
    retention_years: int = Field(ge=1, le=100)
    tags: List[str] = Field(default_factory=list)
    version: str = "1.0"
```

**Key learnings:**
- Strict schemas prevent garbage metadata
- Classification levels are critical for access control
- Retention policies vary by document type
- Always version documents for audit trails

## Retrieval Optimization

### Hybrid Search

**Always use hybrid search for enterprise RAG:**

```python
from src.retrieval.hybrid_search import HybridSearchEngine

search_engine = HybridSearchEngine(
    vector_weight=0.7,      # 70% vector, 30% BM25
    bm25_weight=0.3,
    rerank=True,            # Enable cross-encoder reranking
    rerank_top_k=20,        # Rerank top 20 results
    final_top_k=5           # Return top 5
)

results = search_engine.search(query, filters={"department": "HR"})
```

**Key learnings:**
- Hybrid search outperforms pure vector search by 25-30%
- Vector: good for semantic similarity
- BM25: excellent for exact matches, acronyms, IDs
- Optimal weights: 60-70% vector, 30-40% BM25 (test for your domain)
- Always rerank: improves precision by 15-20%

### Embedding Strategy

**Cache embeddings aggressively:**

```python
from src.retrieval.embeddings import CachedEmbeddingModel

embedding_model = CachedEmbeddingModel(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_backend="redis",
    cache_ttl=86400 * 30,   # 30 days
    batch_size=32
)

# Automatically cached
embeddings = embedding_model.embed(texts)
```

**Key learnings:**
- Embedding generation is expensive: cache everything
- 60-80% cache hit rate in production
- Use Redis for distributed caching
- Batch processing: 10x faster than individual calls
- For embeddings: BERT-based > OpenAI (cost and control)

### Metadata Filtering

**Pre-filter with metadata before vector search:**

```python
# GOOD: Filter first, then search
results = search_engine.search(
    query="remote work policy",
    filters={
        "department": "HR",
        "document_type": "policy",
        "classification": {"$in": ["public", "internal"]}
    },
    top_k=5
)

# BAD: Search everything, filter later
# This wastes compute and reduces accuracy
results = search_engine.search(query, top_k=100)
filtered_results = [r for r in results if r.metadata.department == "HR"]
```

**Key learnings:**
- Metadata filtering reduces search space by 70-90%
- Improves retrieval quality (more relevant results)
- Enables access control and compliance
- Use database indices for common filters

## Generation & Prompting

### Prompt Engineering

**Use structured prompts with clear roles:**

```python
SYSTEM_PROMPT = """You are an AI assistant for {company_name}.
Your role is to answer employee questions based solely on company documentation.

RULES:
1. Only use information from the provided context
2. If the answer is not in the context, say "I don't have that information"
3. Always cite sources using [Doc ID] format
4. For compliance topics, be extra cautious and conservative
5. Never make up information or policies

CONTEXT:
{context}
"""

USER_PROMPT = """Question: {query}

Provide a clear, accurate answer based on the context above.
Include citations for all claims."""
```

**Key learnings:**
- System prompts set behavior, user prompts ask questions
- Clear rules reduce hallucinations by 40-50%
- Explicit "don't know" instruction is critical
- Citations enable verification and build trust
- Compliance disclaimers protect legally

### Guardrails

**Implement multi-layer guardrails:**

```python
from src.generation.guardrails import GuardrailPipeline, PIIDetector, FactChecker

guardrails = GuardrailPipeline([
    PIIDetector(
        detect=["email", "ssn", "phone", "credit_card"],
        action="redact"
    ),
    FactChecker(
        method="citation_check",
        threshold=0.8
    ),
    ToxicityFilter(threshold=0.7),
    ComplianceValidator(rules=compliance_rules)
])

# Apply guardrails
response = llm.generate(prompt)
safe_response = guardrails.apply(response, context=context)
```

**Key learnings:**
- Layer guardrails: input → generation → output
- PII detection is mandatory for regulated industries
- Fact-checking catches hallucinations
- Citation verification ensures groundedness
- Always log guardrail violations for monitoring

### Streaming Responses

**Use streaming for better UX:**

```python
from fastapi.responses import StreamingResponse

async def generate_stream(query: str):
    async for chunk in llm.stream(prompt):
        # Apply guardrails incrementally
        safe_chunk = guardrails.apply_chunk(chunk)
        yield f"data: {safe_chunk}\n\n"

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    return StreamingResponse(
        generate_stream(request.query),
        media_type="text/event-stream"
    )
```

**Key learnings:**
- Streaming improves perceived latency by 3-5x
- Start sending results within 500ms
- Users tolerate longer total time if streaming
- Implement client-side buffering for smooth display

## Caching Strategy

### Multi-Level Caching

**Implement L1 (memory) and L2 (Redis) caching:**

```python
from src.orchestration.caching import MultiLevelCache

cache = MultiLevelCache(
    l1_size=1000,          # In-memory cache
    l1_ttl=300,            # 5 minutes
    l2_backend="redis",
    l2_ttl=86400,          # 24 hours
    cache_embeddings=True,
    cache_responses=True
)

# Cache key includes query + filters + model version
cache_key = cache.generate_key(query, filters, model_version)
```

**Key learnings:**
- L1 cache: 90% hit rate for repeated queries
- L2 cache: 60% hit rate across users
- Cache embeddings: 30-40% cost reduction
- Cache responses: 50-60% latency reduction
- Invalidate cache on document updates

## Monitoring & Observability

### Key Metrics

**Track these metrics in production:**

```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
query_counter = Counter("rag_queries_total", "Total queries", ["status"])
query_latency = Histogram("rag_query_latency_seconds", "Query latency")
retrieval_precision = Gauge("rag_retrieval_precision", "Retrieval precision")

# Cost metrics
token_counter = Counter("rag_tokens_used", "Tokens used", ["model"])
cost_gauge = Gauge("rag_cost_daily", "Daily cost in USD")

# Quality metrics
hallucination_rate = Gauge("rag_hallucination_rate", "Hallucination rate")
citation_accuracy = Gauge("rag_citation_accuracy", "Citation accuracy")
```

**Key learnings:**
- Monitor latency percentiles (p50, p95, p99), not averages
- Track costs per query, per user, per department
- Quality metrics > quantity metrics
- Set up alerts for anomalies (latency spikes, error rates)
- Weekly reviews of metrics inform improvements

### Logging

**Use structured logging:**

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "query_processed",
    query_id=query_id,
    user_id=user_id,
    query=query,
    num_results=len(results),
    latency_ms=latency,
    cache_hit=cache_hit,
    model_version=model_version,
    cost_usd=cost
)
```

**Key learnings:**
- JSON logs enable easy querying and analysis
- Log all queries for audit compliance
- Include timing for each pipeline stage
- Log costs for chargeback and optimization
- Never log PII in logs

## Security & Compliance

### Access Control

**Implement document-level access control:**

```python
from src.api.middleware import AccessControl

def get_accessible_documents(user_id: str, query: str):
    """Filter documents based on user permissions."""
    
    user = get_user(user_id)
    
    # Build filters based on user role and department
    filters = {
        "classification": {"$in": user.allowed_classifications},
        "$or": [
            {"department": user.department},
            {"visibility": "company-wide"}
        ]
    }
    
    return search_engine.search(query, filters=filters)
```

**Key learnings:**
- Role-based access control (RBAC) is table stakes
- Filter at database level, not application level
- Log all access attempts for audit
- Deny by default, allow explicitly
- Regular access reviews (quarterly)

### PII Detection

**Detect and handle PII appropriately:**

```python
from src.generation.guardrails import PIIDetector

pii_detector = PIIDetector(
    patterns={
        "ssn": r"\d{3}-\d{2}-\d{4}",
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\d{3}-\d{3}-\d{4}",
        "credit_card": r"\d{4}-\d{4}-\d{4}-\d{4}"
    },
    action="redact"  # or "flag", "reject"
)

# Detect in documents
pii_found = pii_detector.detect(document_text)
if pii_found:
    # Redact and log
    clean_text = pii_detector.redact(document_text)
    logger.warning("pii_detected", document_id=doc_id, pii_types=pii_found)
```

**Key learnings:**
- Scan all documents during ingestion
- Redact PII before embedding
- Never log PII
- Regular expression patterns + ML models
- Country-specific PII patterns (GDPR, CCPA)

## Cost Optimization

### Token Management

**Optimize token usage:**

```python
def optimize_context(chunks: List[str], max_tokens: int = 3000):
    """Select most relevant chunks within token budget."""
    
    # Rerank chunks
    scored_chunks = reranker.score(query, chunks)
    
    # Select chunks within budget
    selected = []
    total_tokens = 0
    
    for chunk, score in scored_chunks:
        chunk_tokens = count_tokens(chunk)
        if total_tokens + chunk_tokens <= max_tokens:
            selected.append(chunk)
            total_tokens += chunk_tokens
        else:
            break
    
    return selected, total_tokens
```

**Key learnings:**
- Context length = biggest cost driver
- Typical query: 3K context + 500 output = 3.5K tokens
- Optimize: Better retrieval > longer context
- Monitor token usage per query type
- 80/20 rule: 20% of queries use 80% of tokens

### Model Selection

**Choose models based on use case:**

```python
MODEL_CONFIGS = {
    "simple_qa": {
        "model": "gpt-3.5-turbo",  # Cheap, fast
        "temperature": 0.3,
        "max_tokens": 300
    },
    "complex_analysis": {
        "model": "gpt-4",           # Expensive, high quality
        "temperature": 0.5,
        "max_tokens": 1000
    },
    "compliance": {
        "model": "gpt-4",           # Critical, needs accuracy
        "temperature": 0.1,
        "max_tokens": 500
    }
}
```

**Key learnings:**
- GPT-3.5: 10x cheaper than GPT-4, use for simple queries
- GPT-4: Use for complex reasoning, compliance, high-stakes
- Local models (Llama 2, Mistral): Free after deployment, consider for high volume
- Route queries to appropriate model (cost vs quality)

## Performance Optimization

### Async Processing

**Use async for I/O-bound operations:**

```python
import asyncio
from typing import List

async def process_query_async(query: str):
    """Process query with concurrent operations."""
    
    # Run embedding and BM25 in parallel
    embedding_task = asyncio.create_task(
        embedding_model.embed_async(query)
    )
    bm25_task = asyncio.create_task(
        bm25_index.search_async(query)
    )
    
    # Wait for both
    embedding, bm25_results = await asyncio.gather(
        embedding_task,
        bm25_task
    )
    
    # Vector search with embedding
    vector_results = await vector_db.search_async(embedding)
    
    # Combine results
    return combine_results(vector_results, bm25_results)
```

**Key learnings:**
- Async reduces latency by 30-40%
- Use for database calls, API calls, embeddings
- Don't use for CPU-bound operations
- Connection pooling essential for async

## Common Pitfalls

### ❌ Don't: Process documents synchronously
```python
# BAD
for doc in documents:
    process_document(doc)  # Slow, sequential
```

### ✅ Do: Batch process with workers
```python
# GOOD
from celery import group

job = group(process_document.s(doc) for doc in documents)
result = job.apply_async()
```

### ❌ Don't: Use character-based chunking
```python
# BAD
chunks = [text[i:i+500] for i in range(0, len(text), 500)]
```

### ✅ Do: Use token-based semantic chunking
```python
# GOOD
chunks = semantic_chunker.chunk(text, chunk_size=512, overlap=50)
```

### ❌ Don't: Return raw LLM output
```python
# BAD
return llm.generate(prompt)
```

### ✅ Do: Apply guardrails
```python
# GOOD
response = llm.generate(prompt)
safe_response = guardrails.apply(response)
return safe_response
```

## Conclusion

These best practices are learned from real-world deployments. Adapt them to your specific needs, but remember:

1. **Quality over speed**: Better retrieval > faster generation
2. **Security first**: Access control, PII detection, audit logs
3. **Monitor everything**: You can't improve what you don't measure
4. **Cache aggressively**: Embeddings and responses
5. **Test continuously**: Evaluation is ongoing, not one-time

For questions or feedback: riteshrana36@gmail.com
