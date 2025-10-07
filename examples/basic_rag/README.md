# 🎓 Basic RAG Pipeline Example

A beginner-friendly introduction to Retrieval-Augmented Generation (RAG).

This example demonstrates the three core concepts of RAG in the simplest way possible, making it perfect for:
- Learning RAG fundamentals
- Understanding the workflow before building complex systems
- Prototyping and experimentation

---

## 🚀 Quick Start

```bash
# Run with built-in sample documents
python examples/basic_rag/run_pipeline.py

# Run with your own documents
python examples/basic_rag/run_pipeline.py ./my_documents

# Ask a custom question
python examples/basic_rag/run_pipeline.py "What is the vacation policy?"
```

---

## 📖 What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique that enhances AI responses by:

1. **Retrieval**: Finding relevant documents from your knowledge base
2. **Augmentation**: Adding those documents as context to the query  
3. **Generation**: Using an AI model to generate an answer based on the context

### Why Use RAG?

- ✅ Provide accurate, source-backed answers
- ✅ Keep AI responses grounded in your specific data
- ✅ Reduce hallucinations by working with retrieved facts
- ✅ Enable domain-specific Q&A without fine-tuning models

---

## 🧾 Sample Output

```
================================================================================
🎓 Basic RAG Pipeline Example
================================================================================

This example demonstrates the three core steps of RAG:
  1. Retrieval: Search for relevant documents
  2. Augmentation: Add retrieved context to the query
  3. Generation: Create an answer from the context

================================================================================

📂 Loading documents...
✓ Loaded 5 documents

❓ Question: How many vacation days do I get?

💡 Answer:
--------------------------------------------------------------------------------
Based on the available information:

Employees are entitled to 15 days of paid vacation per year. Vacation must be 
requested at least 2 weeks in advance and approved by a manager. Unused vacation 
days can be carried over to the next year, up to a maximum of 5 days.

(Found 3 relevant document(s))
--------------------------------------------------------------------------------

📚 Sources:
  • Company Vacation Policy (relevance score: 6)
  • Performance Reviews (relevance score: 2)
  • Remote Work Guidelines (relevance score: 1)

================================================================================
💡 Try other questions:
   python examples/basic_rag/run_pipeline.py "Can I work from home?"
   python examples/basic_rag/run_pipeline.py "What health benefits are available?"
   python examples/basic_rag/run_pipeline.py "How much is the professional development budget?"
================================================================================
```

---

## 🧠 How It Works

### Step-by-Step Breakdown

#### 1. **Document Loading**
```python
# Load documents from a directory or use built-in samples
pipeline = SimpleRAGPipeline(documents_path="./my_documents")
```

The pipeline loads `.txt` files and creates a searchable collection.

#### 2. **Query Processing**
```python
# User asks a question
result = pipeline.query("How many vacation days do I get?")
```

#### 3. **Retrieval (R)**
```python
# Search for relevant documents using keyword matching
relevant_docs = pipeline.search(query, top_k=3)
```

In this basic example, we use simple keyword matching. Production systems use:
- **Vector embeddings** for semantic similarity
- **BM25** for keyword-based search
- **Hybrid search** combining both approaches

#### 4. **Augmentation (A)**
The retrieved documents are used as context for answer generation.

#### 5. **Generation (G)**
```python
# Generate an answer from the retrieved context
answer = pipeline.generate_answer(query, relevant_docs)
```

In this example, we return content from the most relevant document. Production systems use LLMs (GPT-4, Claude, etc.) to:
- Synthesize information from multiple sources
- Format answers naturally
- Add citations and source attribution

---

## 📂 Using Your Own Documents

### Create a Directory with Text Files

```bash
mkdir my_documents
echo "Our company offers 15 vacation days per year." > my_documents/vacation.txt
echo "Remote work is available 3 days per week." > my_documents/remote.txt
```

### Run the Pipeline

```bash
python examples/basic_rag/run_pipeline.py ./my_documents "Tell me about vacation"
```

---

## ⚙️ Configuration

See [config_example.yaml](./config_example.yaml) for configuration options including:
- Document paths and formats
- Retrieval settings
- Output preferences
- Future enhancement options (embedding models, LLMs)

---

## 📋 Sample Output

See [sample_output.txt](./sample_output.txt) for complete example output.

---

## 🆚 Basic vs. Enterprise RAG

| Feature | Basic RAG (This Example) | Enterprise RAG |
|---------|-------------------------|----------------|
| **Retrieval** | Simple keyword matching | Vector embeddings + BM25 hybrid search |
| **Reranking** | None | Cross-encoder models |
| **Generation** | Template-based | LLM-powered (GPT-4, Claude) |
| **Caching** | None | Redis caching for speed |
| **Monitoring** | None | Metrics, logging, tracing |
| **Scale** | Single machine | Distributed, production-ready |
| **Use Case** | Learning, prototyping | Production deployments |

---

## 🎯 Learning Path

### 1. **Start Here** (Basic RAG)
- ✅ Understand the RAG workflow
- ✅ Experiment with simple queries
- ✅ See how retrieval affects answers

### 2. **Next: Enterprise RAG**
See [examples/enterprise_rag/](../enterprise_rag/) for:
- Hybrid search with vector embeddings
- LLM integration
- Production patterns

### 3. **Advanced: Compliance RAG**
See [examples/compliance_rag/](../compliance_rag/) for:
- PII detection and redaction
- Audit logging
- Security and compliance

---

## 🛠️ Extending This Example

### Add Vector Embeddings

Replace the keyword search with semantic embeddings:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed documents
doc_embeddings = model.encode([doc['content'] for doc in documents])

# Embed query and find similar documents
query_embedding = model.encode([query])
similarities = cosine_similarity(query_embedding, doc_embeddings)
```

### Integrate an LLM

Use OpenAI or another LLM for answer generation:

```python
import openai

def generate_answer(query, context_docs):
    context = "\n\n".join([doc['content'] for doc in context_docs])
    
    prompt = f"""Answer the question based on the context below.
    
Context:
{context}

Question: {query}

Answer:"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### Add Persistence

Store documents in a vector database:

```python
from qdrant_client import QdrantClient

client = QdrantClient(path="./rag_db")
# Store and retrieve documents with vector search
```

---

## 📚 Key Concepts

### Retrieval Methods

1. **Keyword Search**: Exact text matching (what this example uses)
2. **Semantic Search**: Meaning-based similarity using embeddings
3. **Hybrid Search**: Combines keyword + semantic for best results

### Document Chunking

For larger documents, split them into smaller chunks:
- Improves retrieval precision
- Fits within LLM context limits
- Enables paragraph-level citations

### Context Window

LLMs have limited context windows (e.g., 4K-128K tokens). RAG helps by:
- Retrieving only relevant portions
- Reducing input size
- Focusing on the most important information

---

## 💡 Common Questions

**Q: Why not just use an LLM directly?**  
A: LLMs have knowledge cutoffs and can hallucinate. RAG grounds answers in your specific, up-to-date documents.

**Q: How do I improve retrieval quality?**  
A: 
- Use better embeddings (e.g., OpenAI's embeddings)
- Implement hybrid search (keyword + semantic)
- Add metadata filtering
- Use reranking models

**Q: What's the difference between RAG and fine-tuning?**  
A: RAG retrieves external knowledge at query time. Fine-tuning trains a model on your data. RAG is often simpler and more flexible.

**Q: Can I use this in production?**  
A: This is a learning example. For production, see [examples/enterprise_rag/](../enterprise_rag/).

---

## 🔗 Next Steps

1. **Experiment**: Try different questions and documents
2. **Learn**: Review the code in `run_pipeline.py`
3. **Upgrade**: Move to [Enterprise RAG](../enterprise_rag/) for production features
4. **Deploy**: See [/deployment/](../../deployment/) for deployment guides

---

## 📖 Additional Resources

- [What is RAG?](../../docs/guides/GETTING_STARTED.md)
- [Production Best Practices](../../docs/best_practices/PRODUCTION.md)
- [Architecture Overview](../../docs/architecture/OVERVIEW.md)

---

**Questions?** Open an issue or contact: riteshrana36@gmail.com
