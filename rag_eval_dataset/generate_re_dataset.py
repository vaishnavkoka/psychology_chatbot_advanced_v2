#!/usr/bin/env python3
"""
Synthetic Requirement Engineering Dataset Generator for RAG Evaluation

Generates realistic requirement-based Q&A pairs for evaluating RAG systems
focused on software requirements, specifications, and feature documentation.
"""

import json
import random
from typing import List, Dict, Any
from datetime import datetime

class REDatasetGenerator:
    """Generate synthetic requirement engineering datasets for RAG evaluation."""
    
    def __init__(self):
        self.documents = self._create_requirement_documents()
        self.qa_pairs = []
    
    def _create_requirement_documents(self) -> List[Dict[str, str]]:
        """Create synthetic requirement documents."""
        return [
            {
                "id": "REQ-001",
                "title": "User Authentication System Requirements",
                "content": """
The user authentication system must support multiple authentication methods:
1. Email/Password authentication with secure password hashing
2. OAuth 2.0 integration with third-party providers (Google, GitHub)
3. Multi-factor authentication (MFA) via email or authenticator app
4. Session management with configurable timeout (default 24 hours)
5. Password recovery via email verification
6. Account lockout after 5 failed login attempts for 30 minutes

Functional Requirements:
- Users must be able to register with valid email and password
- Password must be at least 12 characters with uppercase, lowercase, numbers, special chars
- Users can enable/disable MFA in account settings
- Session tokens must be refreshed every 15 minutes of activity
- Failed login attempts must be logged for security auditing

Non-Functional Requirements:
- Authentication should complete within 2 seconds
- System must support 10,000 concurrent users
- All authentication data must comply with GDPR
- Passwords must be hashed using bcrypt with salt
                """
            },
            {
                "id": "REQ-002",
                "title": "Search and Filtering Capabilities",
                "content": """
The search system must support:
1. Full-text search across all document fields
2. Advanced filtering by multiple criteria
3. Faceted search with aggregations
4. Real-time search suggestions/autocomplete
5. Search result ranking by relevance
6. Support for Boolean operators (AND, OR, NOT)

Search Performance:
- Search results must return within 500ms
- Autocomplete suggestions within 100ms
- Support searches across 1 million documents
- Pagination with configurable page size (10-100 items)

Advanced Features:
- Synonym matching for common terms
- Fuzzy matching for typos (edit distance <= 2)
- Search within date ranges
- Sorting by relevance, date, or custom fields
- Saved searches for authenticated users
                """
            },
            {
                "id": "REQ-003",
                "title": "Data Export and Reporting",
                "content": """
Users must be able to export data in multiple formats:
1. CSV export with customizable columns
2. PDF reports with branding and customization
3. Excel exports with multiple sheets
4. JSON API responses
5. Scheduled exports via email

Export Constraints:
- Maximum export size: 100,000 records
- Exports must respect user permissions
- Exported data must include audit trail
- All exports must be encrypted at rest

Report Features:
- Predefined report templates (Summary, Detailed, Executive)
- Custom report builder with drag-and-drop interface
- Scheduled reports (daily, weekly, monthly)
- Email delivery with HTML and PDF formats
- Report sharing with access control
                """
            },
            {
                "id": "REQ-004",
                "title": "API Rate Limiting and Quotas",
                "content": """
The API must implement rate limiting to prevent abuse:
1. Per-user rate limiting: 1000 requests/hour for free tier
2. Per-user rate limiting: 10,000 requests/hour for premium tier
3. Per-IP rate limiting: 100 requests/minute (anonymous)
4. Burst allowance: 20% above limit for 5 minutes
5. Rate limit headers in all responses

Rate Limit Response:
- Return 429 (Too Many Requests) when limit exceeded
- Include Retry-After header with wait time
- Log all rate limit violations for analytics
- Alert users when approaching limits
- Gradual backoff: exponential retry with jitter

Quota Management:
- Daily API quota counter resets at UTC midnight
- Quota visibility in user dashboard
- Ability to increase quotas through billing
- Priority support for enterprise customers
                """
            },
            {
                "id": "REQ-005",
                "title": "Data Privacy and Security",
                "content": """
Security and privacy requirements:
1. End-to-end encryption for sensitive data
2. SSL/TLS 1.3 for all communications
3. GDPR compliance with data deletion requests
4. Regular security audits and penetration testing
5. Data retention policies with automatic deletion

Compliance Requirements:
- SOC 2 Type II certification
- PCI DSS compliance for payment data
- HIPAA compliance for healthcare data
- CCPA compliance for California residents
- Regular third-party security assessments

Access Control:
- Role-Based Access Control (RBAC) with 5 default roles
- Attribute-Based Access Control (ABAC) for fine-grained permissions
- Multi-tenant data isolation
- Audit logs for all data access
- IP whitelisting for enterprise accounts
                """
            },
            {
                "id": "REQ-006",
                "title": "Notification System Requirements",
                "content": """
The notification system must support:
1. Real-time in-app notifications via WebSocket
2. Email notifications with daily digest option
3. SMS notifications for critical alerts
4. Push notifications for mobile apps
5. Notification preferences and unsubscribe options

Notification Types:
- System notifications (maintenance, updates)
- User activity notifications (mentions, comments)
- Alert notifications (threshold breaches, errors)
- Task notifications (reminders, deadlines)
- Promotional notifications (opt-in only)

Notification Management:
- Users can customize notification frequency (real-time, hourly, daily)
- Users can enable/disable notification channels per type
- Do-not-disturb hours configuration
- Notification history and archive
- Notification search and filtering
                """
            }
        ]
    
    def _generate_qa_pairs(self) -> List[Dict[str, Any]]:
        """Generate Q&A pairs from documents."""
        qa_patterns = {
            "REQ-001": [
                {
                    "q": "What authentication methods are supported?",
                    "a": "The system supports email/password, OAuth 2.0 (Google, GitHub), and multi-factor authentication via email or authenticator app.",
                    "type": "factual"
                },
                {
                    "q": "What are the password requirements?",
                    "a": "Passwords must be at least 12 characters and contain uppercase, lowercase, numbers, and special characters.",
                    "type": "specific"
                },
                {
                    "q": "What is the session timeout policy?",
                    "a": "Sessions have a configurable timeout with a default of 24 hours. Tokens are refreshed every 15 minutes of activity.",
                    "type": "specific"
                },
                {
                    "q": "How are users protected against brute force attacks?",
                    "a": "The system locks accounts after 5 failed login attempts for 30 minutes, and logs all failed attempts for security auditing.",
                    "type": "security"
                },
                {
                    "q": "Can users recover forgotten passwords?",
                    "a": "Yes, users can recover their password through email verification.",
                    "type": "process"
                }
            ],
            "REQ-002": [
                {
                    "q": "What search operators are supported?",
                    "a": "The system supports Boolean operators including AND, OR, and NOT for advanced searches.",
                    "type": "feature"
                },
                {
                    "q": "What is the expected search response time?",
                    "a": "Search results must return within 500ms, while autocomplete suggestions must respond within 100ms.",
                    "type": "performance"
                },
                {
                    "q": "Does the system handle spelling mistakes in searches?",
                    "a": "Yes, fuzzy matching is supported for typos with up to 2 character edit distance.",
                    "type": "feature"
                },
                {
                    "q": "How many documents can the search system handle?",
                    "a": "The system supports searching across 1 million documents.",
                    "type": "scalability"
                },
                {
                    "q": "Can users save their searches?",
                    "a": "Yes, authenticated users can save searches for future use.",
                    "type": "feature"
                }
            ],
            "REQ-003": [
                {
                    "q": "What export formats are supported?",
                    "a": "The system supports CSV, PDF, Excel, and JSON export formats, with scheduled email delivery.",
                    "type": "feature"
                },
                {
                    "q": "What is the maximum export size?",
                    "a": "The maximum export size is 100,000 records.",
                    "type": "constraint"
                },
                {
                    "q": "How many predefined report templates are available?",
                    "a": "There are three predefined templates: Summary, Detailed, and Executive.",
                    "type": "feature"
                },
                {
                    "q": "Can exports be scheduled and emailed automatically?",
                    "a": "Yes, users can schedule daily, weekly, or monthly reports with email delivery.",
                    "type": "process"
                },
                {
                    "q": "Are exported records encrypted?",
                    "a": "Yes, all exports must be encrypted at rest.",
                    "type": "security"
                }
            ],
            "REQ-004": [
                {
                    "q": "What are the rate limits for different user tiers?",
                    "a": "Free tier: 1000 requests/hour, Premium tier: 10,000 requests/hour, Anonymous: 100 requests/minute per IP.",
                    "type": "specific"
                },
                {
                    "q": "What HTTP status code is returned for rate limit violations?",
                    "a": "HTTP 429 (Too Many Requests) is returned with a Retry-After header.",
                    "type": "technical"
                },
                {
                    "q": "When do quota counters reset?",
                    "a": "Daily API quotas reset at UTC midnight.",
                    "type": "process"
                },
                {
                    "q": "Can users increase their API quotas?",
                    "a": "Yes, users can increase quotas through billing upgrades.",
                    "type": "process"
                },
                {
                    "q": "Is there a burst allowance above the rate limit?",
                    "a": "Yes, there is a 20% burst allowance above the limit for 5 minutes.",
                    "type": "feature"
                }
            ],
            "REQ-005": [
                {
                    "q": "What compliance standards are required?",
                    "a": "The system must comply with GDPR, CCPA, SOC 2 Type II, PCI DSS, and HIPAA.",
                    "type": "compliance"
                },
                {
                    "q": "How is sensitive data encrypted?",
                    "a": "Sensitive data uses end-to-end encryption and all communications use SSL/TLS 1.3.",
                    "type": "security"
                },
                {
                    "q": "What access control models are supported?",
                    "a": "The system supports Role-Based Access Control (5 default roles) and Attribute-Based Access Control for fine-grained permissions.",
                    "type": "feature"
                },
                {
                    "q": "How are audit logs maintained?",
                    "a": "All data access is logged in audit trails for security and compliance purposes.",
                    "type": "security"
                },
                {
                    "q": "Is multi-tenant data isolation provided?",
                    "a": "Yes, the system enforces multi-tenant data isolation.",
                    "type": "architecture"
                }
            ],
            "REQ-006": [
                {
                    "q": "What notification channels are available?",
                    "a": "In-app (WebSocket), email, SMS, and push notifications.",
                    "type": "feature"
                },
                {
                    "q": "Can users customize notification frequency?",
                    "a": "Yes, users can set frequency to real-time, hourly, daily, or disable specific notification types.",
                    "type": "feature"
                },
                {
                    "q": "What types of notifications are sent?",
                    "a": "System, user activity, alert, task, and promotional notifications.",
                    "type": "information"
                },
                {
                    "q": "Can users set do-not-disturb hours?",
                    "a": "Yes, users can configure do-not-disturb hours when notifications are suppressed.",
                    "type": "feature"
                },
                {
                    "q": "Is there a notification history feature?",
                    "a": "Yes, users can view, search, and archive their notification history.",
                    "type": "feature"
                }
            ]
        }
        
        qa_list = []
        for doc_id, patterns in qa_patterns.items():
            doc = next(d for d in self.documents if d["id"] == doc_id)
            for pattern in patterns:
                qa_list.append({
                    "id": f"{doc_id}-Q{len(qa_list) % 10 + 1}",
                    "question": pattern["q"],
                    "answer": pattern["a"],
                    "ground_truth_doc": doc_id,
                    "document_title": doc["title"],
                    "question_type": pattern["type"],
                    "difficulty": random.choice(["easy", "medium", "hard"]),
                    "document_context": doc["content"][:500]  # First 500 chars for context
                })
        
        return qa_list
    
    def generate_jsonl(self, output_path: str) -> int:
        """Generate JSONL format for RAG evaluation."""
        self.qa_pairs = self._generate_qa_pairs()
        
        with open(output_path, 'w') as f:
            for qa in self.qa_pairs:
                f.write(json.dumps(qa) + '\n')
        
        return len(self.qa_pairs)
    
    def generate_json(self, output_path: str) -> int:
        """Generate JSON format for RAG evaluation."""
        self.qa_pairs = self._generate_qa_pairs()
        
        data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "domain": "Requirement Engineering",
                "num_documents": len(self.documents),
                "num_qa_pairs": len(self.qa_pairs)
            },
            "documents": self.documents,
            "qa_pairs": self.qa_pairs
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return len(self.qa_pairs)
    
    def generate_csv(self, output_path: str) -> int:
        """Generate CSV format for RAG evaluation."""
        import csv
        self.qa_pairs = self._generate_qa_pairs()
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'question', 'answer', 'ground_truth_doc', 
                'document_title', 'question_type', 'difficulty'
            ])
            writer.writeheader()
            for qa in self.qa_pairs:
                row = {k: v for k, v in qa.items() if k not in ['document_context']}
                writer.writerow(row)
        
        return len(self.qa_pairs)
    
    def generate_all(self, output_dir: str):
        """Generate all formats."""
        self.qa_pairs = self._generate_qa_pairs()
        
        jsonl_path = f"{output_dir}/requirement_engineering_rag_eval.jsonl"
        json_path = f"{output_dir}/requirement_engineering_rag_eval.json"
        csv_path = f"{output_dir}/requirement_engineering_rag_eval.csv"
        
        with open(jsonl_path, 'w') as f:
            for qa in self.qa_pairs:
                f.write(json.dumps(qa) + '\n')
        
        with open(json_path, 'w') as f:
            data = {
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "domain": "Requirement Engineering",
                    "num_documents": len(self.documents),
                    "num_qa_pairs": len(self.qa_pairs),
                    "version": "1.0"
                },
                "documents": self.documents,
                "qa_pairs": self.qa_pairs
            }
            json.dump(data, f, indent=2)
        
        import csv
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'question', 'answer', 'ground_truth_doc', 
                'document_title', 'question_type', 'difficulty'
            ])
            writer.writeheader()
            for qa in self.qa_pairs:
                row = {k: v for k, v in qa.items() if k not in ['document_context']}
                writer.writerow(row)
        
        return {
            "jsonl": len(self.qa_pairs),
            "json": len(self.qa_pairs),
            "csv": len(self.qa_pairs),
            "files": [jsonl_path, json_path, csv_path]
        }

if __name__ == "__main__":
    import sys
    import os
    
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(output_dir, exist_ok=True)
    
    generator = REDatasetGenerator()
    result = generator.generate_all(output_dir)
    
    print(f"✅ Dataset generated successfully!\n")
    print(f"📊 Statistics:")
    print(f"   - Documents: {len(generator.documents)}")
    print(f"   - Q&A Pairs: {result['json']}")
    print(f"\n📁 Files created:")
    for file_path in result['files']:
        file_size = os.path.getsize(file_path) / 1024
        print(f"   ✅ {os.path.basename(file_path)} ({file_size:.1f} KB)")
