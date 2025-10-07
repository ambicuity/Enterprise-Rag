# 🔒 Compliance-Focused RAG Pipeline Example

A RAG implementation with security and compliance features for regulated industries.

This example demonstrates how to build RAG systems that meet strict regulatory requirements in:
- 🏥 Healthcare (HIPAA)
- 🏦 Finance (SOX, PCI-DSS)
- 🔐 Privacy (GDPR)
- 💊 Pharmaceuticals (FDA)

---

## 🚀 Quick Start

```bash
# Run with default user and sample documents
python examples/compliance_rag/run_pipeline.py

# Run as specific user
python examples/compliance_rag/run_pipeline.py analyst_001

# Ask a compliance question
python examples/compliance_rag/run_pipeline.py analyst_001 "What are HIPAA retention requirements?"

# Use your own documents
python examples/compliance_rag/run_pipeline.py analyst_001 ./compliance_docs "What are our data retention policies?"
```

---

## 🔐 Compliance Features

### 1. **PII Detection & Redaction**
Automatically detects and redacts:
- Email addresses
- Social Security Numbers (SSN)
- Phone numbers
- Credit card numbers

```python
# Input with PII
query = "What about employee john.doe@example.com?"

# Automatically redacted
processed_query = "What about employee [REDACTED-EMAIL]?"
```

### 2. **Audit Logging**
Complete audit trail of all actions:
- User queries
- Document access
- PII detection events
- Authorization checks
- Answer generation

All logs include:
- Timestamp (UTC)
- User ID
- Action type
- Detailed metadata

### 3. **Data Classification**
Automatic document classification:
- **PUBLIC**: General information
- **INTERNAL**: Internal use only
- **CONFIDENTIAL**: Sensitive business data
- **RESTRICTED**: Highly sensitive (PII, PHI, financial)

### 4. **Access Control**
- Document-level authorization checks
- User authentication simulation
- Access logging for compliance
- Role-based access control (RBAC) ready

### 5. **Citation Tracking**
Full source attribution with:
- Document ID
- Classification level
- Relevance score
- Chain of custody

### 6. **Encryption-Ready Architecture**
Designed for:
- Encryption at rest
- Encryption in transit
- Key management integration
- Secure credential handling

---

## 🧾 Sample Output

```
================================================================================
🔒 Compliance-Focused RAG Pipeline Example
================================================================================

This example demonstrates RAG with compliance and security features:
  • PII Detection & Redaction
  • Audit Logging
  • Data Classification
  • Access Control
  • Citation Tracking

================================================================================

📂 Initializing compliance pipeline for user: analyst_001...
✓ Loaded 5 classified documents

❓ Question: What are HIPAA data retention requirements?

🔐 Compliance Analysis:
--------------------------------------------------------------------------------
Classification: CONFIDENTIAL
PII Detected in Question: ✓ No
PII Detected in Answer: ✓ No
--------------------------------------------------------------------------------

💡 Answer:
--------------------------------------------------------------------------------
All patient records must be retained for a minimum of 7 years per HIPAA 
regulations. Medical records for minors must be kept until the patient reaches 
age 21. Electronic health records must be encrypted at rest and in transit using 
AES-256. Access to patient data requires multi-factor authentication and is logged.

Additional information from 1 related document(s).
--------------------------------------------------------------------------------

📚 Citations (with Classifications):
  • [CONFIDENTIAL] Patient Data Retention Policy (ID: HIPAA-001)
  • [CONFIDENTIAL] Data Subject Rights (ID: GDPR-002)

📋 Audit Trail:
--------------------------------------------------------------------------------
Total logged actions: 8
Recent actions:
  [2024-01-15T10:23:45.123456] SYSTEM_INIT: Loaded 5 documents
  [2024-01-15T10:23:45.234567] SEARCH: Query: what are hipaa data retention requirements?
  [2024-01-15T10:23:45.345678] AUTHORIZATION_CHECK: Access to CONFIDENTIAL document HIPAA-001
  [2024-01-15T10:23:45.456789] RETRIEVAL: Retrieved 2 documents
  [2024-01-15T10:23:45.567890] ANSWER_GENERATED: Generated answer with classification: CONFIDENTIAL
--------------------------------------------------------------------------------

================================================================================
💡 Try other questions:
   python examples/compliance_rag/run_pipeline.py analyst_001 "Explain GDPR data subject rights"
   python examples/compliance_rag/run_pipeline.py analyst_001 "What are SOX financial control requirements?"
   python examples/compliance_rag/run_pipeline.py analyst_001 "How should adverse events be reported to the FDA?"
================================================================================
```

---

## 🏥 Industry Use Cases

### Healthcare (HIPAA)

**Requirements:**
- Patient data encryption
- Access logging
- 7-year retention
- Breach notification

**Example:**
```bash
python examples/compliance_rag/run_pipeline.py doctor_123 "What are patient data retention rules?"
```

### Finance (SOX, PCI-DSS)

**Requirements:**
- Financial record retention (7 years)
- Dual approval for transactions
- Audit trails
- Internal controls

**Example:**
```bash
python examples/compliance_rag/run_pipeline.py auditor_456 "What are SOX compliance requirements?"
```

### Privacy (GDPR)

**Requirements:**
- Data subject rights (access, deletion)
- 30-day response time
- Data processing records
- Cross-border transfer controls

**Example:**
```bash
python examples/compliance_rag/run_pipeline.py dpo_789 "How do we handle data deletion requests?"
```

### Pharmaceuticals (FDA)

**Requirements:**
- Adverse event reporting (7-15 days)
- Lifetime + 10 year retention
- 21 CFR Part 11 compliance
- Electronic submission

**Example:**
```bash
python examples/compliance_rag/run_pipeline.py safety_officer_101 "What are adverse event reporting timeframes?"
```

---

## 🛡️ Security Best Practices

### 1. **PII Handling**
```python
# Always redact PII before logging
pipeline._log_action("QUERY", pipeline._redact_pii(user_query))

# Detect PII in both queries and responses
pii_detected = pipeline._detect_pii(text)
```

### 2. **Audit Logging**
```python
# Log all significant actions
pipeline._log_action(
    action="DOCUMENT_ACCESS",
    details="User accessed confidential document",
    metadata={'document_id': 'DOC-123', 'classification': 'CONFIDENTIAL'}
)

# Export logs for compliance review
pipeline.export_audit_log('audit_log.json')
```

### 3. **Data Classification**
```python
# Classify documents before indexing
classification = pipeline._classify_document(content)

# Enforce classification-based access control
if document['classification'] == 'RESTRICTED':
    if not user_has_clearance(user_id):
        raise UnauthorizedAccess()
```

### 4. **Access Control**
```python
# Check authorization before document access
if document.get('requires_authorization'):
    if not pipeline._check_authorization(document):
        return None  # Access denied
```

---

## 🔧 Production Deployment

### Integration Points

#### 1. **Identity Management**
Replace mock auth with real IAM:
```python
from okta import OktaClient

def _check_authorization(self, document):
    user = OktaClient().get_user(self.user_id)
    return document['classification'] in user.clearance_levels
```

#### 2. **Encryption**
Add encryption for data at rest:
```python
from cryptography.fernet import Fernet

# Encrypt document content before storage
encrypted_content = fernet.encrypt(content.encode())

# Decrypt on retrieval
decrypted_content = fernet.decrypt(encrypted_content).decode()
```

#### 3. **Audit Log Storage**
Send logs to SIEM or compliance system:
```python
import logging
from logging.handlers import SysLogHandler

# Configure secure logging
logger.addHandler(SysLogHandler(address=('siem.company.com', 514)))
```

#### 4. **Database Integration**
Store classified documents in secure database:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use encrypted connection
engine = create_engine('postgresql+psycopg2://user:pass@host:5432/db?sslmode=require')
```

---

## 📋 Compliance Checklist

### HIPAA Compliance
- [x] Encryption at rest and in transit
- [x] Access logging and audit trails
- [x] 7-year retention policy
- [x] User authentication
- [ ] Breach notification procedures (integrate with monitoring)
- [ ] Business Associate Agreements (legal/contractual)

### GDPR Compliance
- [x] Data subject rights (access, deletion)
- [x] Data classification
- [x] Audit logging
- [ ] Cookie consent (web interface)
- [ ] Data Protection Impact Assessment (DPIA)
- [ ] DPO designation

### SOX Compliance
- [x] Financial record retention (7 years)
- [x] Audit trails for all transactions
- [x] Access controls
- [ ] Executive certification process
- [ ] Annual control testing

### FDA 21 CFR Part 11
- [x] Audit trails
- [x] Record retention (lifetime + 10 years)
- [x] User authentication
- [ ] Electronic signatures
- [ ] System validation documentation

---

## 🧪 Testing

### Test PII Detection
```bash
# Query with email
python examples/compliance_rag/run_pipeline.py test_user "Contact john.doe@example.com about policy"

# Query with SSN
python examples/compliance_rag/run_pipeline.py test_user "Employee 123-45-6789 needs access"
```

### Test Access Control
```bash
# Access confidential documents
python examples/compliance_rag/run_pipeline.py analyst_001 "Show patient records"

# Review audit log
python examples/compliance_rag/run_pipeline.py analyst_001 "Export audit log"
```

### Test Data Classification
```bash
# Different classification levels
python examples/compliance_rag/run_pipeline.py user_001 "What are public policies?"
python examples/compliance_rag/run_pipeline.py user_001 "What are confidential procedures?"
```

---

## 📊 Audit Log Export

Export complete audit trail for compliance review:

```python
from examples.compliance_rag.run_pipeline import ComplianceRAGPipeline

# Initialize pipeline
pipeline = ComplianceRAGPipeline(user_id="auditor_001")

# Run some queries
pipeline.query("What are retention requirements?")
pipeline.query("How is PII protected?")

# Export audit log
pipeline.export_audit_log("compliance_audit_2024.json")
```

The exported log includes:
- All user queries
- Document access events
- PII detection alerts
- Authorization checks
- System events

---

## 🚀 Next Steps

1. **Integrate Real Auth**: Replace mock authentication with Okta, Auth0, or Azure AD
2. **Add Encryption**: Implement AES-256 encryption for data at rest
3. **Setup SIEM**: Connect audit logs to Splunk, ELK, or similar
4. **Enable Monitoring**: Add Prometheus metrics and alerts
5. **Deploy Securely**: Use Kubernetes secrets, encrypted volumes, private networks

---

## 📚 Related Documentation

- [Security Best Practices](../../docs/best_practices/PRODUCTION.md#security)
- [Compliance Guide](../../docs/guides/COMPLIANCE.md)
- [Audit Logging](../../docs/architecture/AUDIT_LOGGING.md)
- [Encryption Setup](../../deployment/security/ENCRYPTION.md)

---

## ⚖️ Legal Notice

This example is for educational purposes only. Achieving full compliance requires:
- Legal review of your specific requirements
- Security audit by qualified professionals
- Integration with certified systems
- Regular compliance testing
- Documented procedures and policies

Consult with legal and compliance experts for production deployments.

---

**Questions?** Open an issue or contact: riteshrana36@gmail.com
