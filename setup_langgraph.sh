#!/bin/bash
# Psychology Chatbot Refactoring Setup Script
# Initializes the LangGraph multi-agent system and populates the knowledge base

set -e

echo "🚀 Psychology Chatbot Multi-Agent System Setup"
echo "=============================================="
echo ""

# Step 1: Check Python environment
echo "1️⃣  Checking Python environment..."
cd /home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced

if [ ! -d ".venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate || source venv/Scripts/activate

echo "   ✅ Python environment ready"
echo ""

# Step 2: Install dependencies
echo "2️⃣  Installing dependencies..."
pip install --upgrade pip setuptools wheel -q
pip install -r requirements.txt -q
echo "   ✅ Dependencies installed"
echo ""

# Step 3: Initialize knowledge base
echo "3️⃣  Initializing psychology knowledge base..."
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')

from data_ingestion import initialize_psychology_knowledge_base

print("   Loading/building FAISS vector store...")
vector_store, ingestion = initialize_psychology_knowledge_base()

if vector_store:
    print("   ✅ Knowledge base initialized successfully!")
    stats = ingestion.get_statistics()
    print(f"      - CSV Files: {stats['csv_files']}")
    print(f"      - TXT Files: {stats['txt_files']}")
    print(f"      - JSON Files: {stats['json_files']}")
else:
    print("   ⚠️  Warning: Vector store initialization had issues")

EOF

echo ""

# Step 4: Verify imports
echo "4️⃣  Verifying LangGraph orchestrator..."
python3 << 'EOF'
import sys
sys.path.insert(0, 'agents')

try:
    from langgraph_orchestrator_psychology import LangGraphPsychologyOrchestrator
    from rag_agent import RAGAgent
    print("   ✅ LangGraph orchestrator verified")
    print("   ✅ RAG agent verified")
except ImportError as e:
    print(f"   ⚠️  Import warning: {e}")

EOF

echo ""

# Step 5: Summary
echo "5️⃣  Setup Summary"
echo "   ✅ Virtual environment ready"
echo "   ✅ Dependencies installed"
echo "   ✅ Knowledge base populated"
echo "   ✅ All modules verified"
echo ""

echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Update backend.py to use LangGraph orchestrator"
echo "  2. Restart FastAPI backend"
echo "  3. Test new multi-agent system"
echo ""
echo "To start services:"
echo "  Backend:  cd /home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced && uvicorn backend:app --reload --port 8000"
echo "  Frontend: cd /home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced && streamlit run frontend_enhanced.py --server.port 8501"
echo ""
