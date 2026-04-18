# Quick Start - Using the RAG Evaluation Dataset

## 📦 What You Have

```
rag_eval_dataset/
├── generate_re_dataset.py              # Dataset generator
├── evaluate_rag.py                     # Evaluation script
├── README.md                           # Full documentation
├── QUICKSTART.md                       # This file
├── requirement_engineering_rag_eval.jsonl  # Dataset (streaming)
├── requirement_engineering_rag_eval.json   # Dataset (full)
└── requirement_engineering_rag_eval.csv    # Dataset (spreadsheet)
```

## ⚡ 3-Minute Setup

### 1. Load the Data
```python
import json

# Option A: Full dataset
with open('requirement_engineering_rag_eval.json') as f:
    data = json.load(f)
    documents = data['documents']
    qa_pairs = data['qa_pairs']

# Option B: Streaming (memory efficient)
with open('requirement_engineering_rag_eval.jsonl') as f:
    for line in f:
        qa = json.loads(line)
        # Process one Q&A pair
```

### 2. Structure of Each Q&A Pair
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

### 3. Basic Evaluation Loop
```python
import json

with open('requirement_engineering_rag_eval.json') as f:
    data = json.load(f)

correct = 0
for qa in data['qa_pairs']:
    # Your RAG system
    retrieved_doc = your_rag.retrieve(qa['question'])
    generated_answer = your_rag.generate(qa['question'])
    
    # Evaluate retrieval
    if retrieved_doc['id'] == qa['ground_truth_doc']:
        correct += 1
    
    # Evaluate answer (implement metrics)
    similarity = compute_similarity(
        generated_answer, 
        qa['answer']
    )

accuracy = correct / len(data['qa_pairs'])
print(f"Retrieval Accuracy: {accuracy:.1%}")
```

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| Documents | 6 comprehensive requirement specs |
| Q&A Pairs | 30 diverse questions |
| Question Types | 12 different types (factual, security, performance, etc.) |
| Difficulty Levels | Easy (13), Medium (10), Hard (7) |
| Avg Question Length | ~7 words |
| Avg Answer Length | ~25 words |
| Formats | JSONL, JSON, CSV |

## 🎯 Requirements Coverage

Each document covers a real-world requirement area:

1. **User Authentication** (REQ-001)
   - Authentication methods, MFA, password policy, session management

2. **Search & Filtering** (REQ-002)
   - Full-text search, autocomplete, filtering, performance

3. **Data Export & Reporting** (REQ-003)
   - Export formats, scheduling, templates, permissions

4. **API Rate Limiting** (REQ-004)
   - Rate limits, quotas, burst allowance, headers

5. **Data Privacy & Security** (REQ-005)
   - Encryption, compliance (GDPR, CCPA, HIPAA), audit logs

6. **Notifications** (REQ-006)
   - Channels, preferences, customization, frequency

## 💻 Usage Examples

### Example 1: Simple Accuracy Check
```python
import json
from collections import Counter

with open('requirement_engineering_rag_eval.json') as f:
    data = json.load(f)

# Count by difficulty
difficulties = Counter(qa['difficulty'] for qa in data['qa_pairs'])
print("Questions by difficulty:", dict(difficulties))

# Count by type
types = Counter(qa['question_type'] for qa in data['qa_pairs'])
print("Questions by type:", dict(types))
```

### Example 2: Grouping by Document
```python
from collections import defaultdict

qa_by_doc = defaultdict(list)
for qa in data['qa_pairs']:
    qa_by_doc[qa['ground_truth_doc']].append(qa)

for doc_id, qas in sorted(qa_by_doc.items()):
    print(f"{doc_id}: {len(qas)} questions")
```

### Example 3: Filter by Difficulty
```python
easy_qs = [qa for qa in data['qa_pairs'] if qa['difficulty'] == 'easy']
hard_qs = [qa for qa in data['qa_pairs'] if qa['difficulty'] == 'hard']

print(f"Easy: {len(easy_qs)}, Hard: {len(hard_qs)}")
```

### Example 4: Evaluation with Metrics
```python
# Compute retrieval metrics
from sklearn.metrics import precision_recall_fscore_support

predictions = []  # Your RAG retrieved doc IDs
ground_truth = [qa['ground_truth_doc'] for qa in data['qa_pairs']]

matches = [pred == truth for pred, truth in zip(predictions, ground_truth)]
accuracy = sum(matches) / len(matches)
print(f"Accuracy: {accuracy:.1%}")
```

## 🔬 Integration with RAG Systems

### With LangChain
```python
from langchain.document_loaders import JSONLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Load documents
loader = JSONLoader(file_path='requirement_engineering_rag_eval.json', ...)
docs = loader.load()

# Create vectorstore
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())

# Test retrieval
query = "What authentication methods are supported?"
results = vectorstore.similarity_search(query)
```

### With Haystack
```python
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import DensePassageRetriever

doc_store = InMemoryDocumentStore()
retriever = DensePassageRetriever(doc_store)

# Evaluate on dataset
for qa in data['qa_pairs']:
    docs = retriever.retrieve(qa['question'])
    print(f"Q: {qa['question']}")
    print(f"Retrieved: {docs[0]['meta']['doc_id']}")
```

## 📈 Metrics to Track

**Retrieval Metrics:**
- Accuracy (exact match)
- MRR (Mean Reciprocal Rank)
- NDCG (Normalized Discounted Cumulative Gain)
- Success@1, Success@3, Success@5

**Generation Metrics:**
- ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
- BLEU (Bilingual Evaluation Understudy)
- Semantic Similarity (cosine similarity of embeddings)
- LLM-based Judge Score

**Combined Metrics:**
- RAGAS (combines retrieval + generation)
- F1 Score

## 🚀 Next Steps

1. **Load the Dataset** - Pick your preferred format
2. **Implement RAG** - Use LangChain, Haystack, or custom system
3. **Run Evaluation** - Test retrieval and generation
4. **Calculate Metrics** - Use RAGAS or custom metrics
5. **Iterate** - Improve based on results

## 📚 Resources

- Full documentation: `README.md`
- Generator code: `generate_re_dataset.py`
- Evaluation example: `evaluate_rag.py`

## ❓ FAQ

**Q: Can I expand the dataset?**  
A: Yes, modify `generate_re_dataset.py` to add more documents or Q&A patterns.

**Q: Which format should I use?**  
A: JSONL for streaming, JSON for full load, CSV for spreadsheets.

**Q: What evaluation framework do you recommend?**  
A: RAGAS (Azure) or your custom metrics based on your use case.

---

**Ready to evaluate your RAG system? Start here:** ✅
