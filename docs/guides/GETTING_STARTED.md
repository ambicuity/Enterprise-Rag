# Getting Started Guide

This guide will help you set up and run the Enterprise RAG system locally.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **Docker and Docker Compose**
- **Git**
- (Optional) **CUDA-compatible GPU** for local model serving

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ambicuity/Enterprise-Rag.git
cd Enterprise-Rag
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# (Optional) Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# LLM Configuration
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379

# MongoDB
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USER=admin
MONGODB_PASSWORD=password

# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASSWORD=password

# Monitoring
ENABLE_METRICS=true
PROMETHEUS_PORT=9090

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
```

### 5. Start Infrastructure Services

Start all required services using Docker Compose:

```bash
docker-compose up -d
```

Verify services are running:

```bash
docker-compose ps
```

You should see:
- Qdrant (vector database) - http://localhost:6333
- Redis (cache) - localhost:6379
- MongoDB (metadata) - localhost:27017
- RabbitMQ (queue) - http://localhost:15672
- Prometheus (metrics) - http://localhost:9090
- Grafana (visualization) - http://localhost:3000

## Running the Application

### Option 1: Development Server

Run the FastAPI application in development mode:

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Option 2: Production Server

Run with Gunicorn for production:

```bash
gunicorn src.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

## Running Examples

### Basic RAG Pipeline

```bash
cd examples/basic_rag
python run_pipeline.py
```

This will:
1. Load sample documents
2. Process and chunk them
3. Generate embeddings
4. Store in vector database
5. Run example queries

### Enterprise RAG Pipeline

```bash
cd examples/enterprise_rag
python run_pipeline.py --config config.yaml
```

This demonstrates:
- Multi-format document processing
- Hybrid search (BM25 + vector)
- Reranking
- Metadata filtering
- Caching

## Verification

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Upload a document (placeholder endpoint)
curl -X POST "http://localhost:8000/api/v1/documents" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample.pdf"

# Query the RAG system (placeholder endpoint)
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the company policy on remote work?",
    "top_k": 5
  }'
```

### Check Service Health

```bash
# Qdrant
curl http://localhost:6333/collections

# RabbitMQ Management
# Open http://localhost:15672 (admin/password)

# Grafana
# Open http://localhost:3000 (admin/admin)
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_chunking.py

# Run integration tests
pytest tests/integration/
```

## Code Quality

### Format Code

```bash
# Format with Black
black src/ tests/

# Lint with Ruff
ruff check src/ tests/

# Type check with MyPy
mypy src/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit code, add tests, update documentation.

### 3. Run Tests and Linting

```bash
pytest
black src/ tests/
ruff check src/ tests/
mypy src/
```

### 4. Commit Changes

```bash
git add .
git commit -m "Add your feature description"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

## Troubleshooting

### Common Issues

**Issue: Docker services won't start**
```bash
# Check Docker is running
docker ps

# Remove old volumes
docker-compose down -v

# Restart services
docker-compose up -d
```

**Issue: Port already in use**
```bash
# Find process using port
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process or change port in .env
```

**Issue: Python dependencies won't install**
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -r requirements.txt -v
```

**Issue: GPU not detected**
```bash
# Check CUDA installation
nvidia-smi

# Verify PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA-compatible PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Getting Help

- **Documentation**: Check `/docs` directory
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions

## Next Steps

1. **Read the Architecture Guide**: `/docs/architecture/OVERVIEW.md`
2. **Explore Examples**: `/examples` directory
3. **Review Best Practices**: `/docs/best_practices`
4. **Set Up Monitoring**: Configure Prometheus and Grafana
5. **Deploy to Production**: Follow deployment guide

## Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Vector Database Comparison](https://github.com/erikbern/ann-benchmarks)

## Development Tips

1. **Use Type Hints**: Enables better IDE support and catches errors early
2. **Write Tests First**: Test-driven development improves code quality
3. **Monitor Metrics**: Use Prometheus/Grafana for performance insights
4. **Cache Aggressively**: Embedding generation is expensive
5. **Batch Processing**: Process documents in batches for efficiency
6. **Version Control**: Commit frequently with meaningful messages

## Performance Tuning

### For Development
- Use smaller embedding models
- Reduce batch sizes
- Use local caching
- Limit document size

### For Production
- Enable GPU acceleration
- Optimize batch sizes
- Configure connection pooling
- Set up CDN for static assets
- Use async workers

## Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Generate strong JWT secret key
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Implement PII detection
- [ ] Regular security updates

## Monitoring Checklist

- [ ] Configure Prometheus scraping
- [ ] Set up Grafana dashboards
- [ ] Enable structured logging
- [ ] Configure log aggregation
- [ ] Set up alerting rules
- [ ] Monitor GPU usage
- [ ] Track token consumption
- [ ] Monitor API latency
