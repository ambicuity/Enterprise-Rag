# Utility Scripts

This directory contains utility scripts for data generation, benchmarking, and other operational tasks.

## 📂 Structure

```
scripts/
├── data_generation/          # Synthetic data generation scripts
│   └── generate_real_world_docs.py
└── benchmarking/             # Performance benchmarking tools
```

## 🔧 Data Generation

### Generate Real-World Documents

Create synthetic enterprise documents for demonstration and testing:

```bash
python scripts/data_generation/generate_real_world_docs.py
```

**What it does:**
- Generates 9 realistic documents across 3 domains (Finance, HR, Pharma)
- Creates proper directory structure under `data/real_world/`
- Produces industry-accurate content (GDPR, SOX, FDA regulations, etc.)
- Safe for version control (no real or sensitive data)

**Output:**
```
data/real_world/
├── finance_reports/
│   ├── audit_guidelines.txt
│   ├── investment_policy.txt
│   └── financial_controls.txt
├── hr_policies/
│   ├── employee_policy.txt
│   ├── benefits_overview.txt
│   └── compliance_summary.txt
└── pharma_regulations/
    ├── fda_reporting_requirements.txt
    ├── drug_safety_protocols.txt
    └── clinical_trial_protocol.txt
```

**Custom path:**
```bash
python scripts/data_generation/generate_real_world_docs.py /path/to/custom/directory
```

## 📊 Benchmarking

*(To be implemented)*

Performance benchmarking tools will include:
- Retrieval quality metrics (precision, recall, NDCG)
- Latency measurements (p50, p95, p99)
- Cost analysis (tokens, API calls, infrastructure)
- Throughput testing (queries per second)

## 🚀 Usage Examples

### 1. Initial Setup

Generate sample data for development:
```bash
python scripts/data_generation/generate_real_world_docs.py
```

### 2. Testing

Use generated data to test RAG pipeline:
```bash
python examples/enterprise_rag/run_pipeline.py
```

### 3. Custom Datasets

Generate data in a custom location:
```bash
python scripts/data_generation/generate_real_world_docs.py data/custom_dataset
```

## 🧪 Development

### Adding New Scripts

When adding new utility scripts:

1. **Create appropriate subdirectory** (e.g., `scripts/monitoring/`)
2. **Add executable permissions**: `chmod +x script.py`
3. **Include docstring** explaining purpose and usage
4. **Update this README** with usage instructions
5. **Add to requirements** if new dependencies needed

### Script Conventions

- Use `#!/usr/bin/env python3` shebang
- Include comprehensive docstrings
- Accept command-line arguments for flexibility
- Print informative progress messages
- Handle errors gracefully
- Return non-zero exit codes on failure

## 📝 Available Scripts

### Data Generation

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_real_world_docs.py` | Create synthetic enterprise documents | `python scripts/data_generation/generate_real_world_docs.py` |

### Benchmarking

| Script | Purpose | Usage |
|--------|---------|-------|
| *(Coming soon)* | Performance benchmarks | TBD |

## 🔍 Script Details

### generate_real_world_docs.py

**Purpose**: Generate synthetic but realistic enterprise documents

**Features:**
- Creates 3 document categories (Finance, HR, Pharma)
- Includes industry-specific terminology and regulations
- Generates proper document metadata
- Safe for public repositories

**Output Format**: Plain text (.txt) for version control

**Example Output:**
```
================================================================================
Enterprise RAG - Synthetic Data Generator
================================================================================

Generating synthetic real-world datasets in: data/real_world

✓ Created: data/real_world/finance_reports/audit_guidelines.txt
✓ Created: data/real_world/finance_reports/investment_policy.txt
✓ Created: data/real_world/finance_reports/financial_controls.txt
✓ Created: data/real_world/hr_policies/employee_policy.txt
✓ Created: data/real_world/hr_policies/benefits_overview.txt
✓ Created: data/real_world/hr_policies/compliance_summary.txt
✓ Created: data/real_world/pharma_regulations/fda_reporting_requirements.txt
✓ Created: data/real_world/pharma_regulations/drug_safety_protocols.txt
✓ Created: data/real_world/pharma_regulations/clinical_trial_protocol.txt

✅ Successfully generated 9 synthetic documents under data/real_world/
   - Finance reports: 3 files
   - HR policies: 3 files
   - Pharma regulations: 3 files

These documents are synthetic but realistic representations of enterprise data.
They can be used for demonstration, testing, and development purposes.
================================================================================
```

## 🛠️ Extending Scripts

### Adding More Document Types

Edit `generate_real_world_docs.py` to add new categories:

```python
NEW_CATEGORY_DOCS = {
    "document1.txt": """Document content here...""",
    "document2.txt": """More content...""",
}

categories = {
    "finance_reports": FINANCE_DOCS,
    "hr_policies": HR_DOCS,
    "pharma_regulations": PHARMA_DOCS,
    "new_category": NEW_CATEGORY_DOCS,  # Add new category
}
```

### Creating New Scripts

Template for new utility scripts:

```python
#!/usr/bin/env python3
"""
Script description here.
"""
import sys
from pathlib import Path


def main():
    """Main function."""
    # Your logic here
    pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

## 📚 Related

- [Data Directory](../data/README.md)
- [Examples](../examples/README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

---

For questions or contributions, see [CONTRIBUTING.md](../CONTRIBUTING.md)
