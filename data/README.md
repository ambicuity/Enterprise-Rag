# Enterprise Data

This directory contains synthetic but realistic enterprise datasets used for demonstration and testing purposes.

## 📂 Structure

```
data/
└── real_world/                    # Simulated enterprise documents
    ├── finance_reports/           # Financial documents
    │   ├── audit_guidelines.txt
    │   ├── investment_policy.txt
    │   └── financial_controls.txt
    ├── hr_policies/               # HR policies
    │   ├── employee_policy.txt
    │   ├── benefits_overview.txt
    │   └── compliance_summary.txt
    └── pharma_regulations/        # Pharmaceutical regulations
        ├── fda_reporting_requirements.txt
        ├── drug_safety_protocols.txt
        └── clinical_trial_protocol.txt
```

## 🎯 Purpose

These documents are **synthetic but industry-accurate** representations of enterprise data, designed to:

- Demonstrate RAG pipeline capabilities
- Provide realistic testing data
- Showcase domain-specific retrieval
- Ensure privacy and compliance (no real data used)

## 📝 Document Domains

### Finance Reports
Real-world financial documents including:
- Internal audit guidelines and procedures
- Investment policy statements
- Financial controls and approval processes
- SOX 404 compliance requirements
- GAAP and IFRS accounting standards

### HR Policies
Human resources documentation covering:
- Employee data protection (GDPR, HIPAA compliance)
- Benefits overview and eligibility
- Compliance requirements (FMLA, ACA, COBRA, ERISA)
- Employment law and recordkeeping
- Privacy and security protocols

### Pharma Regulations
Pharmaceutical industry regulatory documents:
- FDA safety reporting protocols (21 CFR Part 312, 314)
- Drug safety and pharmacovigilance
- Clinical trial protocols (ICH-GCP)
- Adverse event reporting timelines
- Electronic records compliance (21 CFR Part 11)

## 🔧 Generating Data

If the data files don't exist or you want to regenerate them:

```bash
# From repository root
python scripts/data_generation/generate_real_world_docs.py
```

This will create all synthetic documents with industry-accurate content.

## ⚠️ Important Notes

1. **Synthetic Data Only**: All documents are synthetic and do not contain real company data
2. **Compliance Safe**: Safe for version control and public repositories
3. **Industry Accurate**: Content reflects real regulatory and policy structures
4. **Educational Purpose**: Designed for learning and demonstration

## 🚀 Usage

These documents are used by:
- **Examples**: See `examples/enterprise_rag/` for RAG pipeline demonstrations
- **Testing**: Integration tests for document processing and retrieval
- **Benchmarking**: Performance evaluation and optimization

## 📊 Document Statistics

- **Total Documents**: 9 files
- **Domains**: 3 (Finance, HR, Pharma)
- **Total Size**: ~40KB of text
- **Format**: Plain text (.txt) for version control

## 🔍 Example Queries

Try these queries with the RAG pipeline:

**HR Queries:**
- "What are the GDPR compliance requirements for employee data?"
- "Summarize the employee benefits package"
- "What is the data retention policy?"

**Finance Queries:**
- "What are the approval thresholds for transactions?"
- "What investments are prohibited?"
- "Explain the audit requirements"

**Pharma Queries:**
- "What are FDA adverse event reporting timelines?"
- "Explain clinical trial compliance requirements"
- "What is 21 CFR Part 11?"

## 🛠️ Customization

To add your own datasets:

1. **Add Documents**: Place files in appropriate category folder
2. **Update Formats**: Supported: .txt, .pdf, .docx, .xlsx (see `.gitignore`)
3. **Run Pipeline**: Documents are automatically processed
4. **Test Retrieval**: Use `examples/enterprise_rag/run_pipeline.py`

## 📚 Related

- [Example Usage](../examples/enterprise_rag/README.md)
- [Data Generation Script](../scripts/data_generation/generate_real_world_docs.py)
- [Document Processing](../src/document_processing/README.md)

---

**Note**: Binary files (.pdf, .docx) are excluded from version control via `.gitignore`. Only plain text versions are committed for transparency and diff-ability.
