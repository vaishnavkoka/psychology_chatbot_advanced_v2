#!/usr/bin/env python3
"""
Example: Evaluate RAG System using the RE Dataset

This script demonstrates how to evaluate a RAG system
using the requirement engineering synthetic dataset.
"""

import json
from typing import List, Dict, Any
from pathlib import Path


class RAGEvaluator:
    """Simple RAG evaluator for demonstration."""
    
    def __init__(self, dataset_path: str):
        """Load dataset."""
        with open(dataset_path) as f:
            self.data = json.load(f)
        self.documents = {doc['id']: doc for doc in self.data['documents']}
        self.qa_pairs = self.data['qa_pairs']
    
    def evaluate_retrieval(self, rag_system_func) -> Dict[str, Any]:
        """
        Evaluate retrieval component.
        
        Assumes rag_system_func takes a question and returns:
        [{"id": "REQ-001", "score": 0.95}, ...]
        """
        correct_retrievals = 0
        mrr_sum = 0  # Mean Reciprocal Rank
        
        for qa in self.qa_pairs:
            question = qa['question']
            expected_doc = qa['ground_truth_doc']
            
            # Mock: Your actual RAG system would retrieve here
            # retrieved_docs = rag_system_func(question)
            retrieved_docs = [
                {"id": expected_doc, "score": 0.95},  # Mock correct retrieval
                {"id": "REQ-999", "score": 0.50}
            ]
            
            retrieved_ids = [doc['id'] for doc in retrieved_docs]
            
            # Check if correct document was retrieved
            if expected_doc in retrieved_ids:
                correct_retrievals += 1
                # Calculate MRR (position of first relevant doc)
                rank = retrieved_ids.index(expected_doc) + 1
                mrr_sum += 1 / rank
        
        return {
            "metric": "Retrieval Accuracy",
            "accuracy": correct_retrievals / len(self.qa_pairs),
            "mrr": mrr_sum / len(self.qa_pairs),
            "total_questions": len(self.qa_pairs),
            "correct_retrievals": correct_retrievals
        }
    
    def evaluate_answer_generation(self) -> Dict[str, Any]:
        """
        Evaluate answer generation component.
        
        In real evaluation, you would:
        1. Generate answers from your RAG system
        2. Compare with ground truth answers
        3. Calculate metrics like ROUGE, BLEU, semantic similarity
        """
        return {
            "metric": "Answer Generation",
            "note": "Implement with your LLM and embedding model",
            "required_metrics": [
                "Semantic Similarity (embedding-based)",
                "ROUGE-1/2/L scores",
                "Exact match percentage",
                "LLM-based judge score"
            ],
            "sample_comparison": {
                "question": self.qa_pairs[0]['question'],
                "expected_answer": self.qa_pairs[0]['answer'],
                "generated_answer": "[Your RAG system output]",
                "similarity_score": 0.87  # Example score
            }
        }
    
    def analyze_by_difficulty(self) -> Dict[str, Any]:
        """Analyze performance by question difficulty."""
        by_difficulty = {}
        
        for difficulty in ['easy', 'medium', 'hard']:
            count = sum(1 for qa in self.qa_pairs if qa['difficulty'] == difficulty)
            by_difficulty[difficulty] = count
        
        return by_difficulty
    
    def analyze_by_question_type(self) -> Dict[str, Any]:
        """Analyze performance by question type."""
        by_type = {}
        
        for qa in self.qa_pairs:
            qtype = qa['question_type']
            by_type[qtype] = by_type.get(qtype, 0) + 1
        
        return by_type
    
    def print_sample_questions(self, n: int = 5):
        """Display sample questions."""
        print(f"\n📋 Sample Questions from Dataset:\n")
        for i, qa in enumerate(self.qa_pairs[:n], 1):
            print(f"{i}. [{qa['question_type'].upper()}] {qa['question']}")
            print(f"   📄 Doc: {qa['document_title']}")
            print(f"   ⭐ Difficulty: {qa['difficulty']}")
            print()


def main():
    """Run evaluation demonstration."""
    dataset_path = Path(__file__).parent / "requirement_engineering_rag_eval.json"
    
    if not dataset_path.exists():
        print(f"❌ Dataset not found at {dataset_path}")
        return
    
    print("=" * 60)
    print("🚀 RAG Evaluation - Requirement Engineering Dataset")
    print("=" * 60)
    
    evaluator = RAGEvaluator(str(dataset_path))
    
    # Print dataset info
    print(f"\n📊 Dataset Statistics:")
    print(f"   • Documents: {len(evaluator.documents)}")
    print(f"   • Q&A Pairs: {len(evaluator.qa_pairs)}")
    
    # Show sample questions
    evaluator.print_sample_questions(3)
    
    # Analyze by difficulty
    print("\n📈 Distribution by Difficulty:")
    by_difficulty = evaluator.analyze_by_difficulty()
    for diff, count in by_difficulty.items():
        print(f"   • {diff.capitalize()}: {count} questions")
    
    # Analyze by type
    print("\n📈 Distribution by Question Type:")
    by_type = evaluator.analyze_by_question_type()
    for qtype, count in sorted(by_type.items()):
        print(f"   • {qtype.capitalize()}: {count} questions")
    
    # Mock retrieval evaluation
    print("\n" + "=" * 60)
    print("📋 Mock Retrieval Evaluation Results:")
    print("=" * 60)
    retrieval_results = evaluator.evaluate_retrieval(None)
    for key, value in retrieval_results.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.2%}")
        else:
            print(f"   {key}: {value}")
    
    # Answer generation notes
    print("\n" + "=" * 60)
    print("📋 Answer Generation Evaluation:")
    print("=" * 60)
    answer_results = evaluator.evaluate_answer_generation()
    for key, value in answer_results.items():
        if isinstance(value, list):
            print(f"   {key}:")
            for item in value:
                print(f"     • {item}")
        else:
            print(f"   {key}: {value}")
    
    print("\n" + "=" * 60)
    print("💡 Next Steps:")
    print("=" * 60)
    print("""
1. Load your trained RAG system
2. Implement retrieve() and generate() functions
3. Run evaluation against this dataset
4. Calculate metrics (NDCG, ROUGE, Semantic Similarity)
5. Analyze results by difficulty and question type
6. Iterate on model improvements
    """)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
