# Enterprise RAG: A Practical Guide from the Trenches

**Author:** Ritesh Rana  
**Email:** riteshrana36@gmail.com  
**Website:** https://riteshrana.engineer

---

## 📋 Purpose

This repository contains a **production-grade guide and implementation patterns** for building Retrieval-Augmented Generation (RAG) systems for mid-size enterprise companies (100–1000 employees) in **regulated industries** (pharma, finance, law, consulting, HR).

It captures **real-world, battle-tested learnings** from 10+ client deployments, including:
- Document processing and quality detection
- Metadata architecture and schema design
- Hybrid retrieval strategies
- Model deployment and serving
- Infrastructure reliability and cost optimization

---

## 🎯 Repository Goals

This repository aims to:

1. **Provide reference implementations** for enterprise RAG pipelines
2. **Demonstrate document quality detection**, hierarchical chunking, metadata schemas, and hybrid search patterns
3. **Offer deployment templates** (Ollama, vLLM, GPU setup, queue management)
4. **Include realistic evaluation scripts** and cost-performance analysis tools
5. **Maintain clarity, pragmatism, and reproducibility**

---

## 🏗️ Repository Structure

```
enterprise-rag/
├── src/
│   ├── document_processing/      # Document ingestion and quality detection
│   │   ├── parsers/              # PDF, DOCX, Excel parsers
│   │   ├── quality_detection/    # OCR quality, corruption detection
│   │   ├── chunking/             # Hierarchical and semantic chunking
│   │   └── metadata/             # Metadata extraction and schemas
│   │
│   ├── retrieval/                # Retrieval and search components
│   │   ├── embeddings/           # Embedding model wrappers
│   │   ├── vector_stores/        # Vector DB integrations (Qdrant, Weaviate)
│   │   ├── hybrid_search/        # BM25 + vector search fusion
│   │   └── reranking/            # Cross-encoder reranking
│   │
│   ├── generation/               # LLM generation components
│   │   ├── prompts/              # Production-tested prompt templates
│   │   ├── guardrails/           # Output validation and safety
│   │   └── streaming/            # Streaming response handlers
│   │
│   ├── orchestration/            # Pipeline orchestration
│   │   ├── pipelines/            # End-to-end RAG pipelines
│   │   ├── caching/              # Response and embedding caching
│   │   └── monitoring/           # Logging, metrics, tracing
│   │
│   └── api/                      # FastAPI application
│       ├── routes/               # API endpoints
│       ├── models/               # Pydantic models
│       └── middleware/           # Auth, rate limiting, CORS
│
├── infrastructure/               # Deployment and infrastructure
│   ├── docker/                   # Dockerfiles for services
│   ├── kubernetes/               # K8s manifests and Helm charts
│   ├── gpu_setup/                # GPU configuration and optimization
│   └── queue_management/         # Celery/RabbitMQ setup
│
├── deployment/                   # Model serving configurations
│   ├── ollama/                   # Ollama setup and configs
│   ├── vllm/                     # vLLM deployment patterns
│   └── model_configs/            # Model-specific configurations
│
├── evaluation/                   # Evaluation and testing
│   ├── metrics/                  # RAG-specific metrics (faithfulness, relevance)
│   ├── test_sets/                # Synthetic test datasets
│   └── cost_analysis/            # Cost-performance benchmarks
│
├── docs/                         # Documentation
│   ├── architecture/             # System architecture diagrams
│   ├── guides/                   # Implementation guides
│   └── best_practices/           # Production best practices
│
├── examples/                     # Example implementations
│   ├── basic_rag/                # Simple RAG pipeline
│   ├── enterprise_rag/           # Full enterprise setup
│   └── compliance_rag/           # Compliance-focused patterns
│
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── e2e/                      # End-to-end tests
│
├── scripts/                      # Utility scripts
│   ├── data_generation/          # Synthetic data generation
│   └── benchmarking/             # Performance benchmarking
│
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- (Optional) CUDA-compatible GPU for local model serving

### Installation

```bash
# Clone the repository
git clone https://github.com/ambicuity/Enterprise-Rag.git
cd Enterprise-Rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Install development dependencies
pip install -r requirements-dev.txt
```

### Running a Basic RAG Pipeline

```bash
# Start vector database and other services
docker-compose up -d

# Run the example pipeline
python examples/basic_rag/run_pipeline.py

# Start the API server
uvicorn src.api.main:app --reload
```

---

## 💼 For GitHub Copilot

When assisting with this repository, Copilot should:

### Code Generation Guidelines
- Generate **clean, modular, production-oriented code** for RAG components
- Use **type hints** and **Pydantic models** for data validation
- Prioritize **FastAPI** for API development and **LangChain/LlamaIndex** for RAG orchestration
- Write **strongly typed Python code** with proper error handling

### Engineering Approach
- Suggest **realistic and debuggable** engineering approaches over theoretical ones
- Prioritize **reliability, cost-efficiency, and compliance** for enterprise environments
- Focus on **incremental improvements** and **maintainability**
- Consider **scalability** and **monitoring** from the start

### Code Style
- **Language:** Python 3.10+
- **Framework:** FastAPI for APIs, LangChain/LlamaIndex for RAG
- **Type Safety:** Use type hints, Pydantic models
- **Infrastructure:** Docker + Kubernetes-ready configs
- **Documentation:** Clear docstrings and inline comments for complex logic
- **Tone:** Pragmatic, engineering-first, production-tested

### Data Handling
- Use **mock or synthetic enterprise documents** (do not use public datasets)
- Implement **proper data sanitization** and **PII detection**
- Follow **compliance requirements** for regulated industries

---

## 📚 Key Features

### 1. Document Processing
- **Multi-format support:** PDF, DOCX, Excel, PowerPoint, HTML
- **Quality detection:** OCR quality assessment, corruption detection
- **Hierarchical chunking:** Section-aware, semantic chunking
- **Metadata extraction:** Automatic metadata tagging and schema validation

### 2. Retrieval Strategies
- **Hybrid search:** BM25 + vector search with score fusion
- **Reranking:** Cross-encoder models for relevance optimization
- **Multi-vector retrieval:** Parent-child document strategies
- **Query expansion:** Automatic query rewriting and expansion

### 3. Generation & Guardrails
- **Production prompts:** Battle-tested prompt templates
- **Output validation:** Schema validation, fact-checking
- **Safety filters:** PII detection, content filtering
- **Citation tracking:** Source attribution and transparency

### 4. Infrastructure
- **GPU optimization:** Efficient batching, quantization strategies
- **Caching layers:** Response caching, embedding caching
- **Queue management:** Async task processing with Celery
- **Monitoring:** Prometheus metrics, structured logging

### 5. Evaluation
- **RAG-specific metrics:** Faithfulness, answer relevance, context precision
- **Cost analysis:** Token usage tracking, cost per query
- **Performance benchmarks:** Latency, throughput measurements
- **A/B testing framework:** Compare retrieval and generation strategies

---

## 🔒 Security & Compliance

For regulated industries, this repository includes:

- **PII Detection:** Automated detection and redaction
- **Access Control:** Role-based access patterns
- **Audit Logging:** Comprehensive query and access logs
- **Data Residency:** Configuration for on-premise deployments
- **Encryption:** At-rest and in-transit encryption patterns

---

## 📊 Performance Considerations

### Cost Optimization
- **Embedding caching:** Reduce redundant embedding calls
- **Response caching:** Cache frequent queries
- **Batch processing:** Optimize throughput for bulk operations
- **Model quantization:** Use 4-bit/8-bit quantization where appropriate

### Latency Optimization
- **Async processing:** Non-blocking I/O operations
- **Streaming responses:** Start returning results immediately
- **Parallel retrieval:** Concurrent vector and keyword search
- **Index optimization:** Proper HNSW configuration

---

## 🧪 Testing Strategy

- **Unit tests:** Individual component testing
- **Integration tests:** End-to-end pipeline testing
- **Performance tests:** Load and stress testing
- **Evaluation tests:** Quality metrics validation

---

## 📖 Documentation

Comprehensive guides available in `/docs`:

- **Architecture Overview:** System design and component interaction
- **Deployment Guide:** Step-by-step deployment instructions
- **Best Practices:** Production lessons learned
- **Troubleshooting:** Common issues and solutions

---

## 🤝 Contributing

This repository represents battle-tested patterns from real deployments. Contributions that add:
- **New production patterns** with real-world validation
- **Performance optimizations** with benchmarks
- **Additional deployment configurations** for different environments
- **Evaluation metrics** and tools

are welcome. Please ensure contributions maintain the pragmatic, production-first approach.

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Built from learnings across 10+ enterprise RAG deployments in regulated industries. Special thanks to all the teams who provided feedback and real-world validation.

---

## 📞 Contact

**Ritesh Rana**  
Email: riteshrana36@gmail.com  
Website: https://riteshrana.engineer

For questions, feedback, or consulting inquiries, please reach out via email.