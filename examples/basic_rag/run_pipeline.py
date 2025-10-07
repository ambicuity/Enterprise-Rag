#!/usr/bin/env python3
"""
Basic RAG Pipeline Example

This is a simple, beginner-friendly RAG pipeline that demonstrates the core concepts:
1. Load documents
2. Search for relevant documents
3. Generate an answer from the retrieved context

Perfect for learning RAG fundamentals before moving to enterprise implementations.
"""
import sys
from pathlib import Path
from typing import List, Dict, Any


class SimpleRAGPipeline:
    """
    A minimal RAG pipeline for learning purposes.
    
    This demonstrates the three core steps of RAG:
    1. Retrieval: Finding relevant documents
    2. Augmentation: Adding context to the query
    3. Generation: Creating an answer from the context
    """
    
    def __init__(self, documents_path: str = None):
        """
        Initialize the pipeline with documents.
        
        Args:
            documents_path: Path to directory containing .txt documents
        """
        self.documents = []
        
        if documents_path:
            self.documents = self._load_documents(documents_path)
        else:
            # Use sample documents if no path provided
            self.documents = self._create_sample_documents()
        
        print(f"✓ Loaded {len(self.documents)} documents")
    
    def _create_sample_documents(self) -> List[Dict[str, Any]]:
        """Create sample documents for demonstration."""
        return [
            {
                "id": 1,
                "title": "Company Vacation Policy",
                "content": "Employees are entitled to 15 days of paid vacation per year. "
                          "Vacation must be requested at least 2 weeks in advance and approved by a manager. "
                          "Unused vacation days can be carried over to the next year, up to a maximum of 5 days."
            },
            {
                "id": 2,
                "title": "Remote Work Guidelines",
                "content": "Employees may work remotely up to 3 days per week with manager approval. "
                          "Remote workers must be available during core hours (10 AM - 3 PM) and maintain "
                          "regular communication with their team. A home office stipend of $500 is provided annually."
            },
            {
                "id": 3,
                "title": "Health Benefits",
                "content": "The company provides comprehensive health insurance covering medical, dental, and vision. "
                          "Employee premiums are 20% of the total cost, with the company covering 80%. "
                          "Dependents can be added to the plan. Annual enrollment period is in November."
            },
            {
                "id": 4,
                "title": "Performance Reviews",
                "content": "Performance reviews are conducted annually in January. Employees receive feedback on "
                          "their accomplishments, areas for improvement, and career development goals. "
                          "Reviews are used to determine annual salary adjustments and bonus eligibility."
            },
            {
                "id": 5,
                "title": "Professional Development",
                "content": "The company supports professional development with a $2,000 annual budget per employee. "
                          "This can be used for courses, conferences, certifications, or books. "
                          "Employees should submit a request form to their manager for approval."
            }
        ]
    
    def _load_documents(self, documents_path: str) -> List[Dict[str, Any]]:
        """Load documents from a directory."""
        documents = []
        path = Path(documents_path)
        
        if not path.exists():
            print(f"⚠️  Path not found: {documents_path}")
            print("Using sample documents instead...")
            return self._create_sample_documents()
        
        for i, doc_file in enumerate(path.glob("*.txt"), start=1):
            with open(doc_file, "r") as f:
                content = f.read()
            
            documents.append({
                "id": i,
                "title": doc_file.stem.replace("_", " ").title(),
                "content": content
            })
        
        return documents if documents else self._create_sample_documents()
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant documents using simple keyword matching.
        
        In a production system, this would use:
        - Vector embeddings for semantic search
        - BM25 for keyword matching
        - Hybrid search combining both approaches
        
        Args:
            query: The search query
            top_k: Number of documents to return
            
        Returns:
            List of relevant documents with scores
        """
        query_lower = query.lower()
        scored_docs = []
        
        # Simple keyword matching for demonstration
        for doc in self.documents:
            score = 0
            content_lower = doc["content"].lower()
            
            # Count how many query words appear in the document
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 3:  # Skip short words
                    score += content_lower.count(word)
            
            if score > 0:
                scored_docs.append({
                    **doc,
                    "score": score
                })
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]
    
    def generate_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        Generate an answer from the retrieved documents.
        
        In a production system, this would use an LLM (GPT-4, Claude, etc.).
        For this demo, we create a simple answer from the retrieved content.
        
        Args:
            query: The user's question
            context_docs: Retrieved documents
            
        Returns:
            Generated answer
        """
        if not context_docs:
            return "I couldn't find any relevant information to answer your question."
        
        # For demo purposes, we'll return content from the most relevant document
        # In production, an LLM would synthesize information from all documents
        top_doc = context_docs[0]
        
        answer = f"Based on the available information:\n\n{top_doc['content']}\n\n"
        
        if len(context_docs) > 1:
            answer += f"(Found {len(context_docs)} relevant document(s))"
        
        return answer
    
    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Main query method that orchestrates the RAG pipeline.
        
        Steps:
        1. Search for relevant documents (Retrieval)
        2. Use documents as context (Augmentation)
        3. Generate answer (Generation)
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with answer and source documents
        """
        # Step 1: Retrieve relevant documents
        relevant_docs = self.search(question, top_k)
        
        # Step 2 & 3: Generate answer from context
        answer = self.generate_answer(question, relevant_docs)
        
        return {
            "question": question,
            "answer": answer,
            "sources": relevant_docs
        }


def main():
    """Run the basic RAG pipeline example."""
    print("=" * 80)
    print("🎓 Basic RAG Pipeline Example")
    print("=" * 80)
    print()
    print("This example demonstrates the three core steps of RAG:")
    print("  1. Retrieval: Search for relevant documents")
    print("  2. Augmentation: Add retrieved context to the query")
    print("  3. Generation: Create an answer from the context")
    print()
    print("=" * 80)
    print()
    
    # Initialize pipeline
    print("📂 Loading documents...")
    documents_path = sys.argv[1] if len(sys.argv) > 1 else None
    pipeline = SimpleRAGPipeline(documents_path)
    print()
    
    # Example questions
    example_questions = [
        "How many vacation days do I get?",
        "Can I work from home?",
        "What health benefits are available?",
        "How much is the professional development budget?",
    ]
    
    # Get question from command line or use first example
    if len(sys.argv) > 2:
        question = " ".join(sys.argv[2:])
    else:
        question = example_questions[0]
    
    # Run the query
    print(f"❓ Question: {question}")
    print()
    
    result = pipeline.query(question)
    
    # Display results
    print("💡 Answer:")
    print("-" * 80)
    print(result["answer"])
    print("-" * 80)
    print()
    
    print("📚 Sources:")
    for doc in result["sources"]:
        print(f"  • {doc['title']} (relevance score: {doc['score']})")
    print()
    
    print("=" * 80)
    print("💡 Try other questions:")
    for q in example_questions:
        if q != question:
            print(f"   python examples/basic_rag/run_pipeline.py \"{q}\"")
    print("=" * 80)


if __name__ == "__main__":
    main()
