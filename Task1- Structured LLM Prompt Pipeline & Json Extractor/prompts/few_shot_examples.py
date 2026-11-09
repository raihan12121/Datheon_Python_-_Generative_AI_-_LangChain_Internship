"""
Few-shot exemplars demonstrating target extraction format for invoices and resumes.
Used in prompt engineering to anchor LLM responses to strict JSON output matching Pydantic schemas.
"""

INVOICE_FEW_SHOT_INPUT = """
BILLING STATEMENT
Issued by: CloudTech Solutions Inc. (VAT # US987654321)
1200 Innovation Way, Austin, TX 78701
Email: billing@cloudtech.example.com | Tel: +1 (512) 555-0199

Billed To:
Nexus Retailers LLC (Tax ID: 45-9871234)
Attn: Accounts Payable
88 Market Street, Suite 400, Chicago, IL 60601
Contact: ap@nexusretail.example.com

Invoice Reference: INV-2024-8841
Date of Issue: October 14, 2024
Due Date: November 13, 2024
PO Number: PO-99120

Items:
1. Enterprise Cloud Hosting (12 Months) - SKU: HOST-ENT
   Qty: 1 | Rate: $3,600.00 | Total: $3,600.00
2. Managed Kubernetes Support Tier 2 - SKU: SUPP-K8S
   Qty: 3 | Rate: $450.00 | Total: $1,350.00
3. Security Audit & Pen-Testing Service - SKU: SEC-AUDIT
   Qty: 1 | Rate: $1,200.00 | Discount: $200.00 | Total: $1,000.00

Subtotal: $5,950.00
State Sales Tax (8.25%): $490.88
Total Payable Amount: $6,440.88 USD

Remittance Instructions:
Bank: Austin First National Bank
Account: 9871122334
Routing / ABA: 111000025
Terms: Net 30 days. Late payments subject to 1.5% interest per month.
"""

INVOICE_FEW_SHOT_OUTPUT = {
    "invoice_number": "INV-2024-8841",
    "invoice_date": "2024-10-14",
    "due_date": "2024-11-13",
    "purchase_order_number": "PO-99120",
    "currency": "USD",
    "vendor": {
        "name": "CloudTech Solutions Inc.",
        "tax_id": "US987654321",
        "email": "billing@cloudtech.example.com",
        "phone": "+1 (512) 555-0199",
        "address": "1200 Innovation Way, Austin, TX 78701"
    },
    "customer": {
        "name": "Nexus Retailers LLC",
        "tax_id": "45-9871234",
        "email": "ap@nexusretail.example.com",
        "phone": None,
        "billing_address": "88 Market Street, Suite 400, Chicago, IL 60601",
        "shipping_address": None
    },
    "line_items": [
        {
            "item_code": "HOST-ENT",
            "description": "Enterprise Cloud Hosting (12 Months)",
            "quantity": 1.0,
            "unit_price": 3600.0,
            "discount": 0.0,
            "total_price": 3600.0
        },
        {
            "item_code": "SUPP-K8S",
            "description": "Managed Kubernetes Support Tier 2",
            "quantity": 3.0,
            "unit_price": 450.0,
            "discount": 0.0,
            "total_price": 1350.0
        },
        {
            "item_code": "SEC-AUDIT",
            "description": "Security Audit & Pen-Testing Service",
            "quantity": 1.0,
            "unit_price": 1200.0,
            "discount": 200.0,
            "total_price": 1000.0
        }
    ],
    "subtotal": 5950.0,
    "tax_rate_percent": 8.25,
    "tax_amount": 490.88,
    "shipping_fee": 0.0,
    "discount_amount": 200.0,
    "total_amount": 6440.88,
    "payment": {
        "payment_method": "Bank Transfer",
        "bank_name": "Austin First National Bank",
        "account_number": "9871122334",
        "routing_or_swift": "111000025",
        "payment_terms": "Net 30 days"
    },
    "notes_or_terms": "Late payments subject to 1.5% interest per month."
}


RESUME_FEW_SHOT_INPUT = """
Alex Mercer
alex.mercer@devmail.io | +1-415-555-9021 | San Francisco, CA
LinkedIn: linkedin.com/in/alexmercer-dev | GitHub: github.com/alexmercer-io

SUMMARY
Full-Stack AI Engineer with 4+ years of hands-on experience designing distributed LLM pipelines,
RAG systems, and high-performance microservices with FastAPI and React.

EXPERIENCE
Senior AI Application Developer | Synapse AI Labs, SF (Jan 2022 - Present)
- Architected enterprise LangChain and LlamaIndex knowledge retrieval pipeline reducing hallucination by 38%.
- Built high-throughput FastAPI microservice serving 15,000+ daily inference requests with 99.9% uptime.
- Deployed multi-tenant agent systems using PostgreSQL pgvector and Redis caching.
Technologies: Python, FastAPI, Docker, LangChain, PostgreSQL, Redis, GCP.

Software Engineer | BitWave Systems (Aug 2020 - Dec 2021)
- Developed responsive React frontend dashboards and automated REST API integrations.
- Implemented real-time WebSocket communication layer for concurrent collaborative tools.
Technologies: TypeScript, React, Node.js, Jest, AWS.

EDUCATION
University of California, Berkeley
Bachelor of Science in Computer Science | Graduated May 2020 | GPA: 3.82 / 4.0
Honors: Magna Cum Laude, Dean's Honors List

SKILLS
- Languages: Python, TypeScript, JavaScript, SQL, Bash
- Frameworks & Libraries: FastAPI, PyTorch, LangChain, React, Next.js, Pydantic
- Cloud & Infrastructure: Docker, Kubernetes, GCP (Vertex AI, Cloud Run), AWS (EC2, S3), Git
- Databases: PostgreSQL, pgvector, Redis, Pinecone

PROJECTS
- AgentFlow Engine: Autonomous task execution framework using ReAct reasoning loop. (github.com/alexmercer-io/agentflow)
- DocuSearch: Semantic PDF document search engine powered by dense embeddings and FAISS.

CERTIFICATIONS
- Google Cloud Certified Professional Cloud Architect (Google Cloud, Issued 2023)
- Deep Learning Specialization (DeepLearning.AI / Coursera, Issued 2021)

LANGUAGES: English (Native), Spanish (Conversational)
"""

RESUME_FEW_SHOT_OUTPUT = {
    "candidate": {
        "full_name": "Alex Mercer",
        "email": "alex.mercer@devmail.io",
        "phone": "+1-415-555-9021",
        "location": "San Francisco, CA",
        "linkedin_url": "https://linkedin.com/in/alexmercer-dev",
        "github_url": "https://github.com/alexmercer-io",
        "portfolio_url": None
    },
    "professional_summary": "Full-Stack AI Engineer with 4+ years of hands-on experience designing distributed LLM pipelines, RAG systems, and high-performance microservices with FastAPI and React.",
    "total_years_experience": 4.0,
    "work_experience": [
        {
            "company": "Synapse AI Labs",
            "role_title": "Senior AI Application Developer",
            "location": "SF",
            "start_date": "2022-01",
            "end_date": "Present",
            "is_current": True,
            "responsibilities": [
                "Architected enterprise LangChain and LlamaIndex knowledge retrieval pipeline",
                "Built high-throughput FastAPI microservice",
                "Deployed multi-tenant agent systems"
            ],
            "key_achievements": [
                "Reduced hallucination by 38%",
                "Served 15,000+ daily inference requests with 99.9% uptime"
            ],
            "technologies_used": ["Python", "FastAPI", "Docker", "LangChain", "PostgreSQL", "Redis", "GCP"]
        },
        {
            "company": "BitWave Systems",
            "role_title": "Software Engineer",
            "location": None,
            "start_date": "2020-08",
            "end_date": "2021-12",
            "is_current": False,
            "responsibilities": [
                "Developed responsive React frontend dashboards and automated REST API integrations",
                "Implemented real-time WebSocket communication layer for concurrent collaborative tools"
            ],
            "key_achievements": [],
            "technologies_used": ["TypeScript", "React", "Node.js", "Jest", "AWS"]
        }
    ],
    "education": [
        {
            "institution": "University of California, Berkeley",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "start_year": None,
            "graduation_year": "2020",
            "gpa": "3.82 / 4.0",
            "honors": ["Magna Cum Laude", "Dean's Honors List"]
        }
    ],
    "skills": [
        {
            "category": "Languages",
            "skills": ["Python", "TypeScript", "JavaScript", "SQL", "Bash"]
        },
        {
            "category": "Frameworks & Libraries",
            "skills": ["FastAPI", "PyTorch", "LangChain", "React", "Next.js", "Pydantic"]
        },
        {
            "category": "Cloud & Infrastructure",
            "skills": ["Docker", "Kubernetes", "GCP", "AWS", "Git"]
        },
        {
            "category": "Databases",
            "skills": ["PostgreSQL", "pgvector", "Redis", "Pinecone"]
        }
    ],
    "projects": [
        {
            "title": "AgentFlow Engine",
            "description": "Autonomous task execution framework using ReAct reasoning loop.",
            "role": "Lead Developer",
            "technologies": ["Python", "ReAct"],
            "github_or_live_url": "https://github.com/alexmercer-io/agentflow"
        },
        {
            "title": "DocuSearch",
            "description": "Semantic PDF document search engine powered by dense embeddings and FAISS.",
            "role": None,
            "technologies": ["FAISS", "Embeddings"],
            "github_or_live_url": None
        }
    ],
    "certifications": [
        {
            "name": "Google Cloud Certified Professional Cloud Architect",
            "issuing_organization": "Google Cloud",
            "issue_date": "2023",
            "credential_id_or_url": None
        },
        {
            "name": "Deep Learning Specialization",
            "issuing_organization": "DeepLearning.AI / Coursera",
            "issue_date": "2021",
            "credential_id_or_url": None
        }
    ],
    "languages": ["English", "Spanish"]
}
