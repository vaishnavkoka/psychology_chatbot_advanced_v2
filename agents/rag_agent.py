"""
RAG Agent - Retrieval-Augmented Generation for Psychology Knowledge
Uses FAISS vector store and embeddings for semantic search over mental health knowledge
"""

from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from langchain_core.tools import Tool
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict, List, Optional, Any
import json
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGAgent:
    """
    Retrieval-Augmented Generation agent for psychology knowledge
    Uses embeddings and FAISS for semantic search over mental health documents
    """
    
    def __init__(self, llm, vector_store_path: str = "data/vector_store"):
        self.llm = llm
        self.vector_store_path = vector_store_path
        self.embeddings_model = None
        self.vector_store = None
        
        # Initialize embeddings and vector store
        self._initialize_embeddings()
        self._load_or_create_vector_store()
        
        self.search_tool = Tool(
            name="semantic_search",
            description="Search psychology knowledge base",
            func=self.semantic_search
        )
        
        logger.info("✓ RAG Agent initialized successfully")
        self.retrieved_docs = []

    def retrieve_relevant_knowledge(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant psychology knowledge for a query"""
        
        if self.vector_store is None:
            logger.warning("⚠️ Vector store not available")
            return []
        
        try:
            logger.info(f"🔍 Retrieving knowledge for query: '{query}'")
            results = self.data_ingestion.search(query, k=k)
            
            retrieved_docs = []
            for doc, score in results:
                retrieved_docs.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "type": doc.metadata.get("type", "unknown"),
                    "relevance_score": float(score),
                    "metadata": doc.metadata
                })
                logger.info(f"  ✅ Retrieved: {doc.metadata.get('source', 'Unknown')} (relevance: {score:.4f})")
            
            self.retrieved_docs = retrieved_docs
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"❌ Error retrieving knowledge: {e}")
            return []

    def generate_response_with_knowledge(self, user_query: str, context: Optional[str] = None, additional_info: Optional[str] = None) -> str:
        """Generate response using retrieved knowledge"""
        
        # Retrieve relevant knowledge
        knowledge = self.retrieve_relevant_knowledge(user_query)
        
        # Format knowledge for prompt
        knowledge_context = self._format_knowledge_for_prompt(knowledge)
        
        # Build the prompt
        prompt = f"""You are a compassionate and knowledgeable psychology assistant. 
            
User Query: {user_query}

{f'Conversation Context: {context}' if context else ''}

{f'Additional Information: {additional_info}' if additional_info else ''}

RETRIEVED PSYCHOLOGY KNOWLEDGE:
{knowledge_context}

Based on the retrieved knowledge above, provide a helpful, empathetic response to the user's query.
Important guidelines:
1. Base your response on the retrieved knowledge when relevant
2. Be compassionate and non-judgmental
3. If the query relates to mental health, provide accurate information
4. Suggest professional help when appropriate
5. Keep response to 300-400 words maximum
6. Avoid medical diagnoses - only provide educational information
7. For crisis situations, provide emergency resources

Response:"""
        
        try:
            logger.info("💭 Generating response...")
            message = self.llm.invoke([HumanMessage(content=prompt)])
            response = message.content
            logger.info("✅ Response generated successfully")
            return response
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return "I'm sorry, I encountered an error generating a response. Please try again."

    def _format_knowledge_for_prompt(self, knowledge: List[Dict[str, Any]]) -> str:
        """Format retrieved knowledge for inclusion in prompt"""
        
        if not knowledge:
            return "No specific knowledge retrieved."
        
        formatted_parts = []
        for i, doc in enumerate(knowledge, 1):
            source = doc.get("source", "Unknown")
            score = doc.get("relevance_score", 0)
            content = doc.get("content", "")
            
            # Truncate content if too long
            if len(content) > 500:
                content = content[:500] + "..."
            
            formatted_parts.append(f"""
Source {i}: {source} (Relevance: {score:.1%})
Content: {content}
""")
        
        return "\n---\n".join(formatted_parts)

    def answer_faq(self, topic: str) -> str:
        """Answer frequently asked questions using retrieved knowledge"""
        
        faq_queries = {
            "depression": "What causes depression and how can it be treated?",
            "anxiety": "What are symptoms of anxiety and effective treatments?",
            "panic": "What is panic disorder and how do I handle panic attacks?",
            "therapy": "What types of therapy are available for mental health?",
            "crisis": "What should I do if I'm in crisis?",
            "medication": "How do psychiatric medications work?",
            "self-care": "What self-care practices support mental health?",
            "resources": "What mental health resources are available?"
        }
        
        query = faq_queries.get(topic.lower(), f"Tell me about {topic}")
        return self.generate_response_with_knowledge(query)

    def provide_evidence_based_information(self, topic: str) -> str:
        """Provide evidence-based information about a mental health topic"""
        
        knowledge = self.retrieve_relevant_knowledge(topic, k=7)
        
        prompt = f"""Based on the following retrieved psychology knowledge, provide a comprehensive, evidence-based overview of {topic}:

{self._format_knowledge_for_prompt(knowledge)}

Provide:
1. What is {topic}?
2. Key facts and statistics
3. Common symptoms or characteristics
4. Effective treatments and strategies
5. When to seek professional help
6. Resources and support options

Keep the response informative but accessible to a general audience. Maximum 500 words."""
        
        try:
            message = self.llm.invoke([HumanMessage(content=prompt)])
            return message.content
        except Exception as e:
            logger.error(f"Error providing information: {e}")
            return "Unable to generate information at this time."

    def compare_approaches(self, approach1: str, approach2: str) -> str:
        """Compare two different therapeutic approaches"""
        
        knowledge1 = self.retrieve_relevant_knowledge(approach1, k=3)
        knowledge2 = self.retrieve_relevant_knowledge(approach2, k=3)
        
        prompt = f"""Compare and contrast {approach1} and {approach2} as approaches to mental health treatment:

Knowledge about {approach1}:
{self._format_knowledge_for_prompt(knowledge1)}

Knowledge about {approach2}:
{self._format_knowledge_for_prompt(knowledge2)}

Provide a balanced comparison covering:
1. Key principles of each approach
2. Effectiveness for different conditions
3. Advantages and disadvantages
4. Who might benefit most from each
5. How they might be combined or integrated

Keep response to 350 words."""
        
        try:
            message = self.llm.invoke([HumanMessage(content=prompt)])
            return message.content
        except Exception as e:
            logger.error(f"Error comparing approaches: {e}")
            return "Unable to compare approaches at this time."

    def get_retrieval_metadata(self) -> Dict[str, Any]:
        """Get metadata about the vector store and retrievals"""
        
        return {
            "vector_store_loaded": self.vector_store is not None,
            "last_retrieved_docs_count": len(self.retrieved_docs),
            "last_retrieved_sources": list(set(doc.get("source", "Unknown") for doc in self.retrieved_docs)),
            "available_sources": self._get_available_sources(),
            "knowledge_base_stats": self.data_ingestion.get_statistics()
        }

    def _get_available_sources(self) -> List[str]:
        """Get list of available knowledge sources"""
        
        sources = set()
        stats = self.data_ingestion.get_statistics()
        
        # Add CSV source names
        csv_names = {
            "mental_health_conditions",
            "therapeutic_techniques",
            "crisis_resources"
        }
        sources.update(csv_names)
        
        # Add TXT source names
        txt_names = {
            "understanding_depression",
            "managing_anxiety"
        }
        sources.update(txt_names)
        
        return sorted(list(sources))

    def rebuild_knowledge_base(self) -> bool:
        """Rebuild the FAISS vector store from scratch"""
        
        logger.info("🔄 Rebuilding knowledge base...")
        try:
            self.vector_store = self.data_ingestion.build_vector_store()
            logger.info("✅ Knowledge base rebuilt successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error rebuilding knowledge base: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    print("🚀 RAG Agent Test")
    print("=" * 50)
    
    # Initialize RAG agent
    agent = RAGAgent()
    
    # Test queries
    test_queries = [
        "What are symptoms of depression and how can I manage them?",
        "I'm experiencing anxiety, what should I do?",
        "What is cognitive behavioral therapy?",
    ]
    
    print("\n🔍 Testing RAG responses...\n")
    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 50)
        response = agent.generate_response_with_knowledge(query)
        print(f"Response: {response}\n")
