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
cd examples/basic_rag
python run_pipeline.py --documents ./sample_docs
```

### Enterprise RAG
```bash
cd examples/enterprise_rag
docker-compose up -d
python run_pipeline.py --config config.yaml
```

### Compliance RAG
```bash
cd examples/compliance_rag
export ENCRYPTION_KEY=your-key
python run_pipeline.py --config compliance_config.yaml
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
