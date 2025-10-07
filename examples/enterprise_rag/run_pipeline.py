#!/usr/bin/env python3
"""
Enterprise RAG Pipeline Example

This example demonstrates a full RAG pipeline using realistic enterprise data
from HR, Finance, and Pharma domains. It showcases hybrid search, metadata filtering,
and document retrieval with scoring.

Note: This is a demonstration script. For production use, you would integrate with
actual vector databases, embedding models, and LLMs as described in the documentation.
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Any


class MockEnterpriseRAGPipeline:
    """
    Mock RAG pipeline for demonstration purposes.
    
    In a production environment, this would integrate with:
    - Vector databases (Qdrant, Weaviate, etc.)
    - Embedding models (sentence-transformers, OpenAI, etc.)
    - LLMs (OpenAI, Anthropic, local models via vLLM/Ollama)
    - Hybrid search engines (BM25 + vector search)
    - Reranking models (cross-encoders)
    """
    
    def __init__(self, data_path: str = "data/real_world"):
        """
        Initialize the RAG pipeline.
        
        Args:
            data_path: Path to enterprise documents
        """
        self.data_path = Path(data_path)
        self.documents = self._load_documents()
        print(f"✓ Loaded {len(self.documents)} documents from {data_path}")
    
    def _load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from the data directory."""
        documents = []
        
        if not self.data_path.exists():
            print(f"⚠️  Data path not found: {self.data_path}")
            print(f"   Run: python scripts/data_generation/generate_real_world_docs.py")
            return documents
        
        # Traverse the data directory
        for category_dir in self.data_path.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                for doc_file in category_dir.glob("*.txt"):
                    with open(doc_file, "r") as f:
                        content = f.read()
                    
                    documents.append({
                        "id": f"{category}/{doc_file.name}",
                        "category": category,
                        "filename": doc_file.name,
                        "content": content,
                        "path": str(doc_file),
                    })
        
        return documents
    
    def run(self, query: str, top_k: int = 3) -> 'RAGResult':
        """
        Run the RAG pipeline on a query.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            RAGResult with answer and sources
        """
        # In production, this would:
        # 1. Generate query embedding
        # 2. Perform hybrid search (BM25 + vector)
        # 3. Apply metadata filters
        # 4. Rerank results
        # 5. Construct context from top documents
        # 6. Generate answer with LLM
        # 7. Apply guardrails and validation
        
        # Mock retrieval based on keyword matching
        retrieved_docs = self._mock_retrieval(query, top_k)
        
        # Mock answer generation
        answer = self._mock_answer_generation(query, retrieved_docs)
        
        return RAGResult(
            query=query,
            answer=answer,
            sources=retrieved_docs,
        )
    
    def _mock_retrieval(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Mock document retrieval based on keyword matching."""
        query_lower = query.lower()
        
        # Simple keyword-based scoring
        scored_docs = []
        for doc in self.documents:
            score = 0.0
            content_lower = doc["content"].lower()
            
            # Count keyword matches
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in content_lower:
                    score += content_lower.count(keyword) * 0.1
            
            if score > 0:
                scored_docs.append({
                    "document": doc["filename"],
                    "category": doc["category"],
                    "score": min(score, 1.0),  # Cap at 1.0
                    "content": doc["content"][:500] + "...",  # Preview
                })
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]
    
    def _mock_answer_generation(self, query: str, docs: List[Dict[str, Any]]) -> str:
        """Mock answer generation from retrieved documents."""
        if not docs:
            return "No relevant documents found to answer this query."
        
        # Extract key information based on query type
        query_lower = query.lower()
        
        if "hr" in query_lower or "employee" in query_lower or "data" in query_lower:
            if "compliance" in query_lower or "gdpr" in query_lower or "hipaa" in query_lower:
                return (
                    "Employee data must comply with GDPR and HIPAA retention rules. "
                    "All personal data must be retained for 7 years with full audit logs enabled. "
                    "Access is restricted to authorized HR personnel only, and mandatory data "
                    "anonymization is required for analytics purposes."
                )
            elif "benefits" in query_lower or "leave" in query_lower:
                return (
                    "Employees receive comprehensive benefits including health insurance (80% employer-paid), "
                    "401(k) matching up to 6%, 15-20 vacation days based on tenure, and parental leave "
                    "(12 weeks maternity, 6 weeks paternity). All full-time employees are eligible for "
                    "benefits after 30 days of employment."
                )
        
        elif "finance" in query_lower or "audit" in query_lower or "transaction" in query_lower:
            if "approval" in query_lower:
                return (
                    "Financial transactions over $50,000 require dual approval from department VP, CFO, and CEO. "
                    "Transactions between $5,000-$50,000 require dual approval from department manager and "
                    "finance manager. All transactions must have supporting documentation and comply with "
                    "SOX 404 requirements."
                )
            elif "investment" in query_lower:
                return (
                    "The investment policy focuses on capital preservation and liquidity. Authorized investments "
                    "include U.S. Treasury securities, investment-grade corporate bonds (rated A or higher), "
                    "and money market funds. Prohibited investments include individual equities, derivatives, "
                    "and cryptocurrencies. Maximum single issuer concentration is limited to 5%."
                )
        
        elif "pharma" in query_lower or "fda" in query_lower or "drug" in query_lower:
            if "safety" in query_lower or "reporting" in query_lower:
                return (
                    "FDA drug safety reporting must comply with 21 CFR Part 312 and 314. Fatal or life-threatening "
                    "unexpected serious adverse events must be reported within 7 days, with follow-up within 8 days. "
                    "Other serious unexpected events require reporting within 15 days. All adverse event data logs "
                    "must be maintained in secure repositories with retention for product lifetime plus 10 years."
                )
            elif "clinical" in query_lower or "trial" in query_lower:
                return (
                    "Clinical trials must comply with ICH-GCP guidelines and obtain Institutional Review Board approval. "
                    "Informed consent is mandatory for all participants. Study design requires clear objectives, "
                    "pre-specified statistical analysis plans, and data safety monitoring boards. All data must maintain "
                    "audit trails and comply with 21 CFR Part 11 for electronic records."
                )
        
        # Default response
        return (
            f"Based on the retrieved documents, relevant information was found in "
            f"{len(docs)} document(s) across {set(d['category'] for d in docs)} categories. "
            "For specific details, please refer to the source documents listed below."
        )


class RAGResult:
    """Container for RAG pipeline results."""
    
    def __init__(self, query: str, answer: str, sources: List[Dict[str, Any]]):
        self.query = query
        self.answer = answer
        self.sources = sources


def main():
    """Run the enterprise RAG pipeline example."""
    print("=" * 80)
    print("🔍 Enterprise RAG Pipeline Example")
    print("=" * 80)
    print()
    
    # Initialize pipeline
    print("📂 Loading enterprise RAG pipeline...")
    data_path = os.getenv("DATA_PATH", "data/real_world")
    pipeline = MockEnterpriseRAGPipeline(data_path=data_path)
    print()
    
    # Example queries
    queries = [
        "Summarize key HR data compliance requirements.",
        "What are the financial approval thresholds for transactions?",
        "Explain FDA safety reporting requirements for adverse events.",
    ]
    
    # Process first query (or custom query from command line)
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = queries[0]
    
    print(f"🧠 Query: {query}")
    print()
    
    # Run pipeline
    result = pipeline.run(query, top_k=3)
    
    # Display results
    print("🚀 RAG Pipeline Result:")
    print("=" * 80)
    print(f"Answer:")
    print(f"{result.answer}")
    print()
    print("Sources:")
    if result.sources:
        for src in result.sources:
            print(f" - {src['document']} ({src['category']}) [score: {src['score']:.2f}]")
    else:
        print(" - No sources found")
    print()
    
    print("=" * 80)
    print("💡 Try other queries:")
    for q in queries:
        if q != query:
            print(f"   python examples/enterprise_rag/run_pipeline.py \"{q}\"")
    print("=" * 80)


if __name__ == "__main__":
    main()
