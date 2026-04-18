"""
Data Ingestion Pipeline for Psychology Chatbot
Converts multi-format datasets into embeddings and populates FAISS vector store
"""

import os
import csv
import json
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path
import pickle
from datetime import datetime

# Vector and embedding imports
import numpy as np
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document
except ImportError:
    print("Installing required packages...")
    os.system("pip install langchain langchain-community sentence-transformers faiss-cpu -q")
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PsychologyDataIngestion:
    """Ingestion pipeline for psychology knowledge base"""
    
    def __init__(self, data_dir: str = "data", vector_store_path: str = "data/vector_store"):
        self.data_dir = Path(data_dir)
        self.vector_store_path = Path(vector_store_path)
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        logger.info("🔧 Initializing embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        
        self.vector_store = None
        self.documents = []
        self.indexed_sources = set()
        
        logger.info("✅ Data ingestion pipeline initialized")

    def ingest_csv_files(self) -> List[Document]:
        """Ingest CSV files and convert to documents"""
        logger.info("📊 Processing CSV files...")
        
        documents = []
        csv_files = list(self.data_dir.glob("*.csv"))
        
        for csv_file in csv_files:
            logger.info(f"  Processing {csv_file.name}...")
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for idx, row in enumerate(reader):
                        # Create document from CSV row
                        content = self._format_csv_row_to_text(csv_file.stem, row)
                        
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": csv_file.stem,
                                "source_file": csv_file.name,
                                "row_index": idx,
                                "type": "csv",
                                "ingestion_date": datetime.now().isoformat()
                            }
                        )
                        documents.append(doc)
                
                logger.info(f"  ✅ Ingested {csv_file.name}: {len([d for d in documents if d.metadata['source'] == csv_file.stem])} records")
                
            except Exception as e:
                logger.error(f"  ❌ Error processing {csv_file.name}: {e}")
        
        return documents

    def _format_csv_row_to_text(self, source_name: str, row: Dict) -> str:
        """Format a CSV row into readable text for embedding"""
        # Get headers to use as context
        formatted_parts = [f"Source: {source_name.replace('_', ' ').title()}"]
        
        for key, value in row.items():
            if value:
                formatted_parts.append(f"{key}: {value}")
        
        return " | ".join(formatted_parts)

    def ingest_txt_files(self) -> List[Document]:
        """Ingest TXT files and split into intelligently sized chunks"""
        logger.info("📄 Processing TXT files...")
        
        documents = []
        txt_files = list(self.data_dir.glob("*.txt"))
        
        for txt_file in txt_files:
            logger.info(f"  Processing {txt_file.name}...")
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split by sections (look for # headers)
                sections = self._split_document_by_sections(content)
                
                for section_idx, (section_title, section_content) in enumerate(sections):
                    doc = Document(
                        page_content=f"## {section_title}\n\n{section_content}",
                        metadata={
                            "source": txt_file.stem,
                            "source_file": txt_file.name,
                            "section": section_title,
                            "section_index": section_idx,
                            "type": "txt",
                            "ingestion_date": datetime.now().isoformat()
                        }
                    )
                    documents.append(doc)
                
                logger.info(f"  ✅ Ingested {txt_file.name}: {len(sections)} sections")
                
            except Exception as e:
                logger.error(f"  ❌ Error processing {txt_file.name}: {e}")
        
        return documents

    def _split_document_by_sections(self, content: str) -> List[Tuple[str, str]]:
        """Split document into sections based on markdown headers"""
        sections = []
        lines = content.split('\n')
        
        current_section = "Introduction"
        current_content = []
        
        for line in lines:
            if line.startswith('# ') or line.startswith('## ') or line.startswith('### '):
                # Save previous section
                if current_content:
                    text = '\n'.join(current_content).strip()
                    if text:
                        sections.append((current_section, text))
                
                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Don't forget final section
        if current_content:
            text = '\n'.join(current_content).strip()
            if text:
                sections.append((current_section, text))
        
        return sections if sections else [("Content", content)]

    def ingest_json_files(self) -> List[Document]:
        """Ingest existing JSON assessment data"""
        logger.info("📋 Processing JSON files...")
        
        documents = []
        json_dir = self.data_dir / "psychology_db"
        
        if not json_dir.exists():
            logger.warning(f"  ⚠️ JSON directory not found: {json_dir}")
            return documents
        
        json_files = list(json_dir.glob("*.json"))
        
        for json_file in json_files:
            logger.info(f"  Processing {json_file.name}...")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract documents from JSON structure
                extracted_docs = self._extract_json_documents(data, json_file.stem)
                documents.extend(extracted_docs)
                
                logger.info(f"  ✅ Ingested {json_file.name}: {len(extracted_docs)} items")
                
            except Exception as e:
                logger.error(f"  ❌ Error processing {json_file.name}: {e}")
        
        return documents

    def _extract_json_documents(self, data: Any, source_name: str) -> List[Document]:
        """Extract documents from JSON data"""
        documents = []
        
        if isinstance(data, dict):
            # If it's a dict with a main key containing a list
            for key, value in data.items():
                if isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, dict):
                            content = json.dumps(item, indent=2)
                            doc = Document(
                                page_content=content,
                                metadata={
                                    "source": source_name,
                                    "item_index": idx,
                                    "type": "json",
                                    "ingestion_date": datetime.now().isoformat()
                                }
                            )
                            documents.append(doc)
        
        return documents

    def build_vector_store(self) -> FAISS:
        """Ingest all data and build FAISS vector store"""
        logger.info("🏗️ Building vector store...")
        
        # Collect all documents
        all_documents = []
        all_documents.extend(self.ingest_csv_files())
        all_documents.extend(self.ingest_txt_files())
        all_documents.extend(self.ingest_json_files())
        
        logger.info(f"📦 Total documents collected: {len(all_documents)}")
        
        if not all_documents:
            logger.warning("⚠️ No documents found to index!")
            return None
        
        # Create vector store
        logger.info("🔍 Creating FAISS vector store...")
        self.vector_store = FAISS.from_documents(
            all_documents,
            self.embeddings
        )
        
        # Save vector store
        logger.info(f"💾 Saving vector store to {self.vector_store_path}...")
        self.vector_store.save_local(str(self.vector_store_path))
        
        logger.info(f"✅ Vector store created with {len(all_documents)} documents")
        
        return self.vector_store

    def load_vector_store(self) -> FAISS:
        """Load existing FAISS vector store"""
        if not self.vector_store_path.exists():
            logger.warning(f"Vector store not found at {self.vector_store_path}")
            return None
        
        try:
            logger.info(f"📂 Loading vector store from {self.vector_store_path}...")
            self.vector_store = FAISS.load_local(
                str(self.vector_store_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("✅ Vector store loaded successfully")
            return self.vector_store
        except Exception as e:
            logger.error(f"❌ Error loading vector store: {e}")
            return None

    def search(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Search vector store for similar documents"""
        if self.vector_store is None:
            logger.error("Vector store not loaded!")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about ingested data"""
        stats = {
            "vector_store_exists": self.vector_store_path.exists(),
            "csv_files": len(list(self.data_dir.glob("*.csv"))),
            "txt_files": len(list(self.data_dir.glob("*.txt"))),
            "json_files": len(list((self.data_dir / "psychology_db").glob("*.json"))) if (self.data_dir / "psychology_db").exists() else 0,
            "vector_store_path": str(self.vector_store_path),
            "last_updated": None
        }
        
        if self.vector_store_path.exists():
            # Try to get modification time
            try:
                mtime = os.path.getmtime(self.vector_store_path / "index.faiss")
                stats["last_updated"] = datetime.fromtimestamp(mtime).isoformat()
            except:
                pass
        
        return stats


def initialize_psychology_knowledge_base() -> FAISS:
    """
    Initialize and build the psychology knowledge base
    Call this once on startup
    """
    ingestion = PsychologyDataIngestion()
    
    # Check if vector store exists
    if ingestion.vector_store_path.exists():
        logger.info("Vector store found, loading...")
        vector_store = ingestion.load_vector_store()
    else:
        logger.info("Vector store not found, building from data...")
        vector_store = ingestion.build_vector_store()
    
    # Print statistics
    stats = ingestion.get_statistics()
    logger.info(f"📊 Knowledge Base Statistics:")
    logger.info(f"   CSV Files: {stats['csv_files']}")
    logger.info(f"   TXT Files: {stats['txt_files']}")
    logger.info(f"   JSON Files: {stats['json_files']}")
    logger.info(f"   Last Updated: {stats['last_updated'] or 'N/A'}")
    
    return vector_store, ingestion


# Example usage and testing
if __name__ == "__main__":
    print("🚀 Psychology Knowledge Base Initialization")
    print("=" * 50)
    
    # Initialize the knowledge base
    vector_store, ingestion = initialize_psychology_knowledge_base()
    
    # Test search
    if vector_store:
        print("\n🔍 Testing search functionality...")
        test_queries = [
            "What are symptoms of depression?",
            "How can I manage anxiety?",
            "Crisis hotline numbers",
            "Cognitive behavioral therapy"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            results = ingestion.search(query, k=2)
            for i, (doc, score) in enumerate(results):
                print(f"  Result {i+1} (score: {score:.4f})")
                print(f"    Source: {doc.metadata.get('source', 'N/A')}")
                print(f"    Content: {doc.page_content[:100]}...")
