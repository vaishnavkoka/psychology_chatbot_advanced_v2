# Requirement Engineering RAG Evaluation Dataset

Synthetic dataset for evaluating Retrieval-Augmented Generation (RAG) systems specialized in requirement engineering and software specifications.

## 📊 Dataset Overview

**Last Generated**: 2024-04-02

| Metric | Value |
|--------|-------|
| **Documents** | 6 requirement specifications |
| **Q&A Pairs** | 30 question-answer pairs |
| **Question Types** | Factual, Specific, Security, Performance, Feature, Compliance |
| **Difficulty Levels** | Easy, Medium, Hard |
| **Formats** | JSONL, JSON, CSV |

---

## 📁 Files

### `requirement_engineering_rag_eval.jsonl` (24.7 KB)
One JSON object per line. Ideal for streaming/batch processing.

**Structure**:
```json
{
  "id": "REQ-001-Q1",
  "question": "What authentication methods are supported?",
  "answer": "The system supports email/password, OAuth 2.0...",
  "ground_truth_doc": "REQ-001",
  "document_title": "User Authentication System Requirements",
  "question_type": "factual",
  "difficulty": "hard",
  "document_context": "The user authentication system must support..."
}
```

### `requirement_engineering_rag_eval.json` (32.1 KB)
Complete dataset with metadata and full requirement documents.

**Structure**:
```json
{
  "metadata": {
    "created": "ISO timestamp",
    "domain": "Requirement Engineering",
    "num_documents": 6,
    "num_qa_pairs": 30,
    "version": "1.0"
  },
  "documents": [...],
  "qa_pairs": [...]
}
```

### `requirement_engineering_rag_eval.csv` (5.6 KB)
Tabular format for spreadsheet applications and simple processing.

**Columns**: `id, question, answer, ground_truth_doc, document_title, question_type, difficulty`

---

## 📋 Content Coverage

### Requirement Categories

1. **User Authentication (REQ-001)** - 5 Q&A pairs
   - Authentication methods, password requirements, MFA, session management, security

2. **Search & Filtering (REQ-002)** - 5 Q&A pairs
   - Full-text search, filtering, autocomplete, performance, scalability

3. **Data Export & Reporting (REQ-003)** - 5 Q&A pairs
   - Export formats, constraints, report templates, scheduling

4. **API Rate Limiting (REQ-004)** - 5 Q&A pairs
   - Rate limits, quotas, burst allowance, response headers

5. **Data Privacy & Security (REQ-005)** - 5 Q&A pairs
   - Encryption, compliance, access control, audit logs

6. **Notifications (REQ-006)** - 5 Q&A pairs
   - Notification channels, preferences, customization

### Question Types

- **Factual**: Direct questions about requirements
- **Specific**: Detailed technical specifications
- **Security**: Security and compliance related
- **Performance**: Performance and scalability
- **Feature**: Feature and capability questions
- **Process**: Process and workflow questions
- **Technical**: Technical implementation details
- **Compliance**: Regulatory and compliance requirements
- **Architecture**: System design and architecture
- **Information**: General information requests

---

## 🎯 Using for RAG Evaluation

### 1. Retrieval Evaluation

Test if your RAG system retrieves the correct document:

```python
import json
import pandas as pd

# Load evaluations data
with open('requirement_engineering_rag_eval.json') as f:
    data = json.load(f)

# For each Q&A pair
for qa in data['qa_pairs']:
    question = qa['question']
    expected_doc = qa['ground_truth_doc']
    
    # Your RAG system
    retrieved_docs = your_rag.retrieve(question)
    
    # Check if correct doc was retrieved
    retrieved_ids = [doc['id'] for doc in retrieved_docs]
    retrieval_correct = expected_doc in retrieved_ids
```

### 2. Answer Quality Evaluation

Test if your RAG system generates accurate answers:

```python
# Using Azure AI Evaluation SDK (RAGAS)
from ragas import evaluate
from ragas.metrics import answer_correctness, answer_relevancy

for qa in data['qa_pairs']:
    question = qa['question']
    expected_answer = qa['answer']
    
    # Your RAG system
    generated_answer = your_rag.generate(question)
    
    # Evaluate
    score = evaluate(
        question=question,
        expected_answer=expected_answer,
        generated_answer=generated_answer
    )
```

### 3. Context Relevance Evaluation

Test if retrieved context matches the question:

```python
for qa in data['qa_pairs']:
    question = qa['question']
    context = qa['document_context']
    
    # Score relevance of context to question
    relevance = measure_relevance(question, context)
```

---

## 📈 Metrics You Can Calculate

### Retrieval Metrics
- **MRR (Mean Reciprocal Rank)**: Position of first relevant document
- **NDCG (Normalized Discounted Cumulative Gain)**: Ranking quality
- **Recall@k**: Percentage of relevant docs retrieved in top-k
- **Precision@k**: Accuracy of top-k retrieved documents

### Generation Metrics
- **BLEU Score**: N-gram overlap with reference answer
- **ROUGE Score**: Recall and precision of n-grams
- **Semantic Similarity**: Cosine similarity of embeddings
- **Answer Correctness**: LLM-based evaluation

### Combined Metrics
- **RAGAS Score**: Combines retrieval and generation quality
- **F1 Score**: Harmonic mean of precision and recall

---

## 💡 Sampling Strategies

### Stratified Sampling (by question type)
```python
df = pd.read_csv('requirement_engineering_rag_eval.csv')
sample = df.groupby('question_type').apply(lambda x: x.sample(n=1))
```

### Difficulty-Based Sampling
```python
easy = df[df['difficulty'] == 'easy']
medium = df[df['difficulty'] == 'medium']
hard = df[df['difficulty'] == 'hard']
```

### Document-Focused Sampling
```python
by_doc = df.groupby('ground_truth_doc')
for doc_id, group in by_doc:
    # Evaluate per-document performance
```

---

## 🔄 Loading Formats

### JSONL (Streaming)
```python
import json
with open('requirement_engineering_rag_eval.jsonl') as f:
    for line in f:
        qa = json.loads(line)
        # Process qa
```

### JSON (Full Load)
```python
import json
with open('requirement_engineering_rag_eval.json') as f:
    data = json.load(f)
    documents = data['documents']
    qa_pairs = data['qa_pairs']
```

### CSV (Pandas)
```python
import pandas as pd
df = pd.read_csv('requirement_engineering_rag_eval.csv')
# df.groupby('document_title')...
```

---

## 📊 Data Characteristics

- **Average Question Length**: ~7 words
- **Average Answer Length**: ~25 words
- **Max Answer Length**: ~150 words
- **Ground Truth Document per Q**: 1 (single most relevant)
- **Question Type Distribution**: Evenly distributed
- **Difficulty Distribution**: Balanced (easy, medium, hard)

---

## 🚀 Getting Started

### Quick Test
```bash
# Check dataset integrity
python3 -c "
import json
with open('requirement_engineering_rag_eval.json') as f:
    data = json.load(f)
    print(f'Documents: {len(data[\"documents\"])}')
    print(f'Q&A Pairs: {len(data[\"qa_pairs\"])}')
    print(f'Sample Q: {data[\"qa_pairs\"][0][\"question\"]}')
"
```

### With Azure AI Evaluation
```bash
pip install ragas azure-ai-evaluation
python3 evaluate_with_ragas.py
```

---

## 📝 Notes

- **Ground Truth**: Each Q&A pair has exactly one ground truth document
- **Context**: Full document context is available for relevance evaluation
- **Synthetic**: All data is synthetic but realistic for requirement engineering domain
- **Expandable**: Script can generate more pairs by modifying patterns in `generate_re_dataset.py`

---

**Created**: April 2, 2024  
**Version**: 1.0  
**Domain**: Requirement Engineering  
**Use Case**: RAG System Evaluation
