#!/usr/bin/env python3
"""
Generate synthetic real-world enterprise documents for demonstration purposes.

This script creates realistic but synthetic documents for HR, Finance, and Pharma domains
to be used in RAG pipeline examples and demonstrations.
"""
import os
from pathlib import Path


# Document templates for each domain
FINANCE_DOCS = {
    "audit_guidelines.txt": """Title: Internal Audit Guidelines Q2 2024

Document ID: FIN-AUD-2024-Q2
Classification: Confidential

Policy Summary:
All transactions over $50,000 require dual approval.
Audit evidence retention: 5 years.
Quarterly risk assessment mandatory for all financial departments.

Relevant Standards:
- SOX 404 Compliance
- IFRS Reporting Standards
- GAAP Accounting Principles

Key Controls:
- Segregation of duties enforced
- All financial transactions require supporting documentation
- Monthly reconciliation of all accounts
- Annual external audit mandatory
""",
    "investment_policy.txt": """Title: Investment Policy Statement 2024

Document ID: FIN-INV-2024-001
Classification: Confidential

Objectives:
- Capital preservation
- Liquidity maintenance
- Risk-adjusted returns

Authorized Investments:
- U.S. Treasury securities
- Investment-grade corporate bonds (rated A or higher)
- Money market funds
- FDIC-insured certificates of deposit

Prohibited Investments:
- Individual equities
- Derivatives and options
- Cryptocurrencies
- Any security rated below investment grade

Portfolio Guidelines:
- Maximum single issuer concentration: 5%
- Minimum credit rating: A
- Maximum portfolio duration: 5 years
- Quarterly rebalancing required
""",
    "financial_controls.txt": """Title: Financial Controls Framework 2024

Document ID: FIN-CTL-2024-001

Internal Controls:
- Dual authorization for payments over $10,000
- Monthly bank reconciliation
- Quarterly financial reporting to Board
- Annual compliance audit

Access Controls:
- Role-based access to financial systems
- Multi-factor authentication required
- Quarterly access reviews
- Immediate access revocation upon termination

Documentation Requirements:
- All expenses require receipts
- Purchase orders mandatory for purchases over $1,000
- Contract retention: 7 years
- Audit trail for all transactions
""",
}

HR_DOCS = {
    "employee_policy.txt": """Title: Employee Data Protection Policy 2024

Document ID: HR-POL-2024-001

Summary:
This document outlines HR data handling policies to comply with GDPR and HIPAA regulations.

Key Points:
- Employee data retention period: 7 years
- Access restricted to authorized HR personnel
- Audit logs retained for all employee data access
- Mandatory data anonymization for analytics

Compliance References:
- EU GDPR Article 5
- HIPAA Privacy Rule §164.530

Data Security:
- Encryption at rest and in transit
- Multi-factor authentication required
- Annual security training mandatory
- Incident response plan in place
""",
    "benefits_overview.txt": """Title: Employee Benefits Overview 2024

Document ID: HR-BEN-2024-001

Health Insurance:
- Medical, dental, and vision coverage
- Employer covers 80% of premium
- Dependent coverage available

Retirement Benefits:
- 401(k) with 50% employer match up to 6%
- Immediate vesting for employee contributions
- 3-year vesting for employer contributions

Paid Time Off:
- Vacation: 15-20 days based on tenure
- Sick leave: 10 days per year
- Personal days: 3 days per year
- 10 paid holidays

Parental Leave:
- Maternity leave: 12 weeks paid
- Paternity leave: 6 weeks paid
- Adoption leave: 8 weeks paid
""",
    "compliance_summary.txt": """Title: HR Compliance Summary 2024

Document ID: HR-COMP-2024-001

Employment Law Compliance:
- EEO-1 reporting: March 31 deadline
- FMLA eligibility: 12 months service, 1,250 hours
- FLSA overtime requirements enforced
- I-9 verification within 3 days of hire

Data Privacy:
- GDPR compliance for EU employees
- CCPA compliance for California residents
- Annual privacy training required
- Data breach notification within 72 hours

Benefits Compliance:
- ACA coverage for full-time employees
- COBRA continuation coverage offered
- ERISA compliance for retirement plans
- Form 5500 filing deadline: July 31

Recordkeeping:
- Personnel files: 7 years post-termination
- Payroll records: 3 years
- I-9 forms: 3 years from hire or 1 year from termination
- Benefits enrollment: 6 years
""",
}

PHARMA_DOCS = {
    "fda_reporting_requirements.txt": """Title: FDA Drug Safety Reporting Protocol

Document ID: PHARMA-FDA-2024-001

Regulatory Framework:
- 21 CFR Part 312 (IND Safety Reporting)
- 21 CFR Part 314 (NDA Safety Reporting)
- 21 CFR Part 11 (Electronic Records)

Safety Reporting Timelines:
- Fatal/Life-threatening: 7 days initial, 8 days follow-up
- Serious unexpected: 15 days
- Annual safety reports: 60 days from IND anniversary

Data Retention:
- Adverse event data logs in secure repositories
- Retention period: Product lifetime + 10 years minimum
- Electronic and paper records maintained

Compliance Requirements:
- Data residency must comply with 21 CFR Part 11
- Electronic signatures and audit trails required
- System validation documented
- Regular compliance audits

Applies to: Clinical, Regulatory, QA teams
""",
    "drug_safety_protocols.txt": """Title: Drug Safety and Pharmacovigilance Protocol

Document ID: PHARMA-PV-2024-001

Adverse Event Monitoring:
- Continuous monitoring of all approved products
- Literature surveillance weekly
- Social media monitoring daily
- Patient support program tracking

Signal Detection:
- Statistical signal detection quarterly
- Medical review of all serious events
- Aggregate analysis monthly
- Risk-benefit assessment ongoing

Quality Management:
- GVP (Good Vigilance Practice) compliance
- Standard operating procedures maintained
- Training program for all staff
- Quality metrics tracked monthly

Regulatory Reporting:
- MedWatch submissions per FDA requirements
- Periodic safety update reports
- Risk evaluation and mitigation strategies
- Regulatory intelligence monitoring
""",
    "clinical_trial_protocol.txt": """Title: Clinical Trial Protocol Guidelines

Document ID: PHARMA-CTP-2024-001

ICH-GCP Compliance:
- Good Clinical Practice standards adherence
- Institutional Review Board approval required
- Informed consent process documented
- Protocol amendments properly submitted

Study Design Requirements:
- Clear objectives and endpoints defined
- Statistical analysis plan pre-specified
- Data safety monitoring board established
- Sample size justification documented

Regulatory Requirements:
- IND application for investigational drugs
- Annual reports to FDA
- Safety reports per 21 CFR 312.32
- Protocol registration on ClinicalTrials.gov

Quality Assurance:
- Source data verification
- Site monitoring visits
- Audit trail for all data
- Document retention per regulations

Participant Protection:
- Informed consent mandatory
- Privacy and confidentiality protected
- Right to withdraw anytime
- Safety monitoring throughout study
""",
}


def generate_docs(base_path: str = "data/real_world") -> None:
    """
    Generate synthetic enterprise documents.
    
    Args:
        base_path: Base directory path for generated documents
    """
    # Create base directory
    base_dir = Path(base_path)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate documents for each category
    categories = {
        "finance_reports": FINANCE_DOCS,
        "hr_policies": HR_DOCS,
        "pharma_regulations": PHARMA_DOCS,
    }
    
    doc_count = 0
    for category, docs in categories.items():
        category_dir = base_dir / category
        category_dir.mkdir(exist_ok=True)
        
        for filename, content in docs.items():
            filepath = category_dir / filename
            with open(filepath, "w") as f:
                f.write(content.strip() + "\n")
            doc_count += 1
            print(f"✓ Created: {filepath}")
    
    print(f"\n✅ Successfully generated {doc_count} synthetic documents under {base_path}/")
    print(f"   - Finance reports: {len(FINANCE_DOCS)} files")
    print(f"   - HR policies: {len(HR_DOCS)} files")
    print(f"   - Pharma regulations: {len(PHARMA_DOCS)} files")


if __name__ == "__main__":
    import sys
    
    # Allow custom path as command-line argument
    base_path = sys.argv[1] if len(sys.argv) > 1 else "data/real_world"
    
    print("=" * 80)
    print("Enterprise RAG - Synthetic Data Generator")
    print("=" * 80)
    print(f"\nGenerating synthetic real-world datasets in: {base_path}\n")
    
    generate_docs(base_path)
    
    print("\nThese documents are synthetic but realistic representations of enterprise data.")
    print("They can be used for demonstration, testing, and development purposes.")
    print("=" * 80)
