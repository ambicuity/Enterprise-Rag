#!/usr/bin/env python3
"""
Compliance-Focused RAG Pipeline Example

This example demonstrates RAG with compliance and security features for regulated industries:
- PII detection and redaction
- Audit logging for all queries
- Access control simulation
- Data classification
- Source citation tracking
- Encryption-ready architecture

Perfect for: Finance, Healthcare, Legal, and Pharmaceutical industries
"""
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import hashlib


class ComplianceRAGPipeline:
    """
    A compliance-focused RAG pipeline with security and audit features.
    
    Key Features:
    - PII detection and redaction
    - Complete audit trail
    - Data classification
    - Access control
    - Citation tracking
    """
    
    # Common PII patterns (simplified for demo)
    PII_PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    }
    
    def __init__(self, documents_path: str = None, user_id: str = "default_user"):
        """
        Initialize the compliance RAG pipeline.
        
        Args:
            documents_path: Path to documents (default: sample documents)
            user_id: User identifier for audit logging
        """
        self.user_id = user_id
        self.audit_log = []
        self.documents = []
        
        if documents_path:
            self.documents = self._load_documents(documents_path)
        else:
            self.documents = self._create_sample_documents()
        
        print(f"✓ Loaded {len(self.documents)} classified documents")
        self._log_action("SYSTEM_INIT", f"Loaded {len(self.documents)} documents")
    
    def _create_sample_documents(self) -> List[Dict[str, Any]]:
        """Create sample compliance-focused documents."""
        return [
            {
                "id": "HIPAA-001",
                "title": "Patient Data Retention Policy",
                "content": "All patient records must be retained for a minimum of 7 years per HIPAA regulations. "
                          "Medical records for minors must be kept until the patient reaches age 21. "
                          "Electronic health records must be encrypted at rest and in transit using AES-256. "
                          "Access to patient data requires multi-factor authentication and is logged.",
                "classification": "CONFIDENTIAL",
                "category": "healthcare_compliance",
                "requires_authorization": True
            },
            {
                "id": "GDPR-002",
                "title": "Data Subject Rights",
                "content": "Under GDPR, individuals have the right to access their personal data, request corrections, "
                          "and request deletion (right to be forgotten). Organizations must respond to data subject "
                          "requests within 30 days. Personal data must not be transferred outside the EU without "
                          "adequate safeguards. All data processing activities must have a legal basis.",
                "classification": "CONFIDENTIAL",
                "category": "privacy_compliance",
                "requires_authorization": True
            },
            {
                "id": "SOX-003",
                "title": "Financial Controls",
                "content": "Sarbanes-Oxley Act requires public companies to maintain accurate financial records. "
                          "All financial transactions must have dual approval and complete audit trails. "
                          "Internal controls must be documented and tested annually. Executive certification "
                          "of financial statements is required. Retention period for audit materials is 7 years.",
                "classification": "CONFIDENTIAL",
                "category": "financial_compliance",
                "requires_authorization": True
            },
            {
                "id": "FDA-004",
                "title": "Adverse Event Reporting",
                "content": "FDA requires reporting of serious adverse events within specific timeframes: "
                          "fatal or life-threatening events within 7 days, other serious events within 15 days. "
                          "All adverse event records must be maintained for the lifetime of the drug plus 10 years. "
                          "Safety data must comply with 21 CFR Part 312 and be submitted electronically via FDA ESG.",
                "classification": "CONFIDENTIAL",
                "category": "pharma_compliance",
                "requires_authorization": True
            },
            {
                "id": "PCI-005",
                "title": "Payment Card Data Security",
                "content": "PCI DSS requires encryption of cardholder data during transmission over public networks. "
                          "Card data must not be stored after authorization unless encrypted. Access to cardholder "
                          "data must be restricted on a need-to-know basis. Regular penetration testing and "
                          "vulnerability scans are mandatory. Incident response plans must be tested annually.",
                "classification": "RESTRICTED",
                "category": "payment_compliance",
                "requires_authorization": True
            }
        ]
    
    def _load_documents(self, documents_path: str) -> List[Dict[str, Any]]:
        """Load and classify documents from a directory."""
        documents = []
        path = Path(documents_path)
        
        if not path.exists():
            print(f"⚠️  Path not found: {documents_path}")
            print("Using sample documents instead...")
            return self._create_sample_documents()
        
        for i, doc_file in enumerate(path.glob("*.txt"), start=1):
            with open(doc_file, "r") as f:
                content = f.read()
            
            # Auto-classify based on content
            classification = self._classify_document(content)
            
            documents.append({
                "id": f"DOC-{i:03d}",
                "title": doc_file.stem.replace("_", " ").title(),
                "content": content,
                "classification": classification,
                "category": "user_document",
                "requires_authorization": classification in ["CONFIDENTIAL", "RESTRICTED"]
            })
        
        return documents if documents else self._create_sample_documents()
    
    def _classify_document(self, content: str) -> str:
        """
        Auto-classify document based on content.
        In production, this would use ML models or metadata.
        """
        content_lower = content.lower()
        
        # Check for sensitive keywords
        if any(word in content_lower for word in ['confidential', 'restricted', 'secret', 'patient', 'ssn']):
            return "CONFIDENTIAL"
        elif any(word in content_lower for word in ['internal', 'proprietary']):
            return "INTERNAL"
        else:
            return "PUBLIC"
    
    def _detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII in text."""
        detected_pii = []
        
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                detected_pii.append({
                    'type': pii_type,
                    'value': match.group(),
                    'position': match.span()
                })
        
        return detected_pii
    
    def _redact_pii(self, text: str) -> str:
        """Redact PII from text."""
        redacted_text = text
        
        for pii_type, pattern in self.PII_PATTERNS.items():
            redacted_text = re.sub(pattern, f'[REDACTED-{pii_type.upper()}]', redacted_text)
        
        return redacted_text
    
    def _log_action(self, action: str, details: str, metadata: Dict[str, Any] = None):
        """Log an action for audit purposes."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': self.user_id,
            'action': action,
            'details': details,
            'metadata': metadata or {}
        }
        self.audit_log.append(log_entry)
    
    def _check_authorization(self, document: Dict[str, Any]) -> bool:
        """
        Check if user is authorized to access the document.
        In production, this would integrate with identity management systems.
        """
        # For demo, we'll allow access but log it
        if document.get('requires_authorization'):
            self._log_action(
                "AUTHORIZATION_CHECK",
                f"Access to {document['classification']} document {document['id']}",
                {'document_id': document['id'], 'classification': document['classification']}
            )
        return True
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant documents with PII detection.
        
        Args:
            query: Search query
            top_k: Number of documents to return
            
        Returns:
            List of relevant documents
        """
        # Check for PII in query
        pii_detected = self._detect_pii(query)
        if pii_detected:
            self._log_action(
                "PII_DETECTED_IN_QUERY",
                f"Query contains {len(pii_detected)} PII instances",
                {'pii_types': [p['type'] for p in pii_detected]}
            )
            query = self._redact_pii(query)
        
        # Log the search
        self._log_action("SEARCH", f"Query: {query}", {'top_k': top_k})
        
        query_lower = query.lower()
        scored_docs = []
        
        # Simple keyword matching
        for doc in self.documents:
            # Check authorization
            if not self._check_authorization(doc):
                continue
            
            score = 0
            content_lower = doc["content"].lower()
            
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 3:
                    score += content_lower.count(word)
            
            if score > 0:
                scored_docs.append({
                    **doc,
                    "score": score
                })
        
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        retrieved = scored_docs[:top_k]
        
        self._log_action(
            "RETRIEVAL",
            f"Retrieved {len(retrieved)} documents",
            {'document_ids': [d['id'] for d in retrieved]}
        )
        
        return retrieved
    
    def generate_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an answer with compliance features.
        
        Returns:
            Dict with answer, citations, and compliance metadata
        """
        if not context_docs:
            return {
                'answer': "No relevant information found.",
                'citations': [],
                'pii_detected': False,
                'classification': 'PUBLIC'
            }
        
        # Determine overall classification (highest level from sources)
        classifications = [doc.get('classification', 'PUBLIC') for doc in context_docs]
        classification_levels = {'PUBLIC': 0, 'INTERNAL': 1, 'CONFIDENTIAL': 2, 'RESTRICTED': 3}
        overall_classification = max(classifications, key=lambda c: classification_levels.get(c, 0))
        
        # Generate answer from most relevant document
        top_doc = context_docs[0]
        answer = f"{top_doc['content']}\n\n"
        
        if len(context_docs) > 1:
            answer += f"Additional information from {len(context_docs)-1} related document(s)."
        
        # Create citations
        citations = [
            {
                'document_id': doc['id'],
                'title': doc['title'],
                'classification': doc['classification'],
                'relevance_score': doc['score']
            }
            for doc in context_docs
        ]
        
        # Detect PII in answer
        pii_detected = self._detect_pii(answer)
        
        self._log_action(
            "ANSWER_GENERATED",
            f"Generated answer with classification: {overall_classification}",
            {
                'classification': overall_classification,
                'citations': len(citations),
                'pii_detected': len(pii_detected) > 0
            }
        )
        
        return {
            'answer': answer,
            'citations': citations,
            'pii_detected': len(pii_detected) > 0,
            'classification': overall_classification,
            'redacted_answer': self._redact_pii(answer) if pii_detected else answer
        }
    
    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Main query method with full compliance pipeline.
        
        Args:
            question: User's question
            top_k: Number of documents to retrieve
            
        Returns:
            Dict with answer and compliance metadata
        """
        # Check for PII in question
        pii_in_question = self._detect_pii(question)
        
        # Retrieve documents
        relevant_docs = self.search(question, top_k)
        
        # Generate answer
        result = self.generate_answer(question, relevant_docs)
        
        # Add question info
        result['question'] = question
        result['pii_in_question'] = len(pii_in_question) > 0
        
        return result
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """Return the audit log."""
        return self.audit_log
    
    def export_audit_log(self, filepath: str):
        """Export audit log to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.audit_log, f, indent=2)
        print(f"✓ Audit log exported to {filepath}")


def main():
    """Run the compliance RAG pipeline example."""
    print("=" * 80)
    print("🔒 Compliance-Focused RAG Pipeline Example")
    print("=" * 80)
    print()
    print("This example demonstrates RAG with compliance and security features:")
    print("  • PII Detection & Redaction")
    print("  • Audit Logging")
    print("  • Data Classification")
    print("  • Access Control")
    print("  • Citation Tracking")
    print()
    print("=" * 80)
    print()
    
    # Get user ID (in production, this would come from auth system)
    user_id = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].endswith('.txt') else "demo_user"
    
    # Initialize pipeline
    print(f"📂 Initializing compliance pipeline for user: {user_id}...")
    documents_path = None
    if len(sys.argv) > 2:
        documents_path = sys.argv[2]
    
    pipeline = ComplianceRAGPipeline(documents_path, user_id=user_id)
    print()
    
    # Example questions
    example_questions = [
        "What are HIPAA data retention requirements?",
        "Explain GDPR data subject rights",
        "What are SOX financial control requirements?",
        "How should adverse events be reported to the FDA?",
    ]
    
    # Get question from command line or use first example
    if len(sys.argv) > 2 and sys.argv[2].endswith('.txt'):
        question = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else example_questions[0]
    elif len(sys.argv) > 2:
        question = " ".join(sys.argv[2:])
    else:
        question = example_questions[0]
    
    # Run query
    print(f"❓ Question: {question}")
    print()
    
    result = pipeline.query(question)
    
    # Display results
    print("🔐 Compliance Analysis:")
    print("-" * 80)
    print(f"Classification: {result['classification']}")
    print(f"PII Detected in Question: {'⚠️  Yes' if result['pii_in_question'] else '✓ No'}")
    print(f"PII Detected in Answer: {'⚠️  Yes' if result['pii_detected'] else '✓ No'}")
    print("-" * 80)
    print()
    
    print("💡 Answer:")
    print("-" * 80)
    # Use redacted answer if PII detected
    answer_to_show = result.get('redacted_answer', result['answer'])
    print(answer_to_show)
    print("-" * 80)
    print()
    
    print("📚 Citations (with Classifications):")
    for citation in result['citations']:
        print(f"  • [{citation['classification']}] {citation['title']} (ID: {citation['document_id']})")
    print()
    
    print("📋 Audit Trail:")
    print("-" * 80)
    audit_log = pipeline.get_audit_log()
    print(f"Total logged actions: {len(audit_log)}")
    print("Recent actions:")
    for entry in audit_log[-5:]:
        print(f"  [{entry['timestamp']}] {entry['action']}: {entry['details']}")
    print("-" * 80)
    print()
    
    print("=" * 80)
    print("💡 Try other questions:")
    for q in example_questions:
        if q != question:
            print(f"   python examples/compliance_rag/run_pipeline.py {user_id} \"{q}\"")
    print()
    print("Export audit log:")
    print("   python -c \"from run_pipeline import *; p = ComplianceRAGPipeline(); p.export_audit_log('audit.json')\"")
    print("=" * 80)


if __name__ == "__main__":
    main()
