# Examples

This directory contains example implementations demonstrating different RAG patterns.

## Structure

### `basic_rag/`
Simple RAG pipeline for getting started:
- Basic document ingestion
- Simple vector search
- Basic prompt template
- Single-model generation
- Minimal configuration

**Use Case**: Learning the fundamentals, prototyping

### `enterprise_rag/`
Full enterprise-grade implementation:
- Multi-format document processing
- Hybrid search (BM25 + vector)
- Metadata filtering
- Reranking pipeline
- Response caching
- Monitoring and logging
- API with authentication

**Use Case**: Production deployment for mid-size companies

### `compliance_rag/`
Compliance-focused patterns for regulated industries:
- PII detection and redaction
- Audit logging
- Access control
- Data residency compliance
- Citation and source tracking
- Output validation
- Encryption at rest and in transit

**Use Case**: Finance, healthcare, legal, pharmaceutical industries

## Running Examples

### Basic RAG
```bash
# Run with built-in sample documents
python examples/basic_rag/run_pipeline.py

# Or with your own documents
python examples/basic_rag/run_pipeline.py ./my_documents "How many vacation days?"
```

### Enterprise RAG
```bash
# Run with sample enterprise data
python examples/enterprise_rag/run_pipeline.py

# Or with custom query
python examples/enterprise_rag/run_pipeline.py "What are the financial approval thresholds?"
```

### Compliance RAG
```bash
# Run with default user
python examples/compliance_rag/run_pipeline.py

# Or as specific user with custom query
python examples/compliance_rag/run_pipeline.py analyst_001 "What are HIPAA requirements?"
```

## Example Features

Each example includes:
- **README**: Setup and usage instructions
- **Configuration**: YAML configuration files
- **Sample Data**: Synthetic example documents
- **Tests**: Basic test coverage
- **Documentation**: Implementation notes and tradeoffs

## Customization

These examples serve as starting points. Customize based on your:
- Document types and formats
- Industry requirements
- Scale and performance needs
- Budget constraints
- Compliance requirements
