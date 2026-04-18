#!/bin/bash
# Comprehensive Deployment Guide
# Complete instructions for deploying Psychology Chatbot to production

echo "🚀 PSYCHOLOGY CHATBOT - DEPLOYMENT GUIDE"
echo "========================================================================"
echo ""

# ============================================================
# SECTION 1: PREREQUISITES
# ============================================================

echo "📋 SECTION 1: PREREQUISITES"
echo "---"
echo "1. Python 3.9+ installed"
echo "2. Git installed"
echo "3. API Keys obtained:"
echo "   - GROQ API Key (from console.groq.com)"
echo "   - HuggingFace API Key (from huggingface.co)"
echo "   - Tavily API Key (from tavily.com)"
echo "   - Serper API Key (from serper.dev)"
echo "   - Cohere API Key (from cohere.com)"
echo ""

# ============================================================
# SECTION 2: LOCAL SETUP
# ============================================================

echo "📱 SECTION 2: LOCAL SETUP"
echo "---"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created"
else
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# ============================================================
# SECTION 3: ENVIRONMENT CONFIGURATION
# ============================================================

echo ""
echo "⚙️  SECTION 3: ENVIRONMENT CONFIGURATION"
echo "---"

if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your API keys:"
    echo "   nano .env"
    echo ""
else
    echo "✅ .env file exists"
fi

# ============================================================
# SECTION 4: DATABASE INITIALIZATION
# ============================================================

echo ""
echo "🗄️  SECTION 4: DATABASE INITIALIZATION"
echo "---"

echo "🔧 Initializing database..."
python3 -c "from src.database_schema import init_db; init_db()"
echo "✅ Database initialized"

# ============================================================
# SECTION 5: SYSTEM VERIFICATION
# ============================================================

echo ""
echo "✅ SECTION 5: SYSTEM VERIFICATION"
echo "---"

echo "Running integration tests..."
python3 system_integration_test.py

# ============================================================
# SECTION 6: STARTING SERVICES
# ============================================================

echo ""
echo "🚀 SECTION 6: STARTING SERVICES"
echo "---"
echo ""
echo "To start the system, open 2 terminals:"
echo ""
echo "Terminal 1 - Backend API:"
echo "  cd /home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced"
echo "  source venv/bin/activate"
echo "  uvicorn backend:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "Terminal 2 - Frontend UI:"
echo "  cd /home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced"
echo "  source venv/bin/activate"
echo "  streamlit run frontend_premium.py --server.port 8501"
echo ""

# ============================================================
# SECTION 7: DOCKER DEPLOYMENT
# ============================================================

echo ""
echo "🐳 SECTION 7: DOCKER DEPLOYMENT (OPTIONAL)"
echo "---"
echo ""
echo "Build and run with Docker:"
echo "  docker-compose up -d"
echo ""
echo "Access the application:"
echo "  Backend API: http://localhost:8000"
echo "  Frontend UI: http://localhost:8501"
echo "  API Docs: http://localhost:8000/docs"
echo ""

# ============================================================
# SECTION 8: API ENDPOINTS REFERENCE
# ============================================================

echo ""
echo "📚 SECTION 8: API ENDPOINTS REFERENCE"
echo "---"
echo ""
echo "Assessment Endpoints:"
echo "  POST   /api/assessments/start           - Begin assessment"
echo "  POST   /api/assessments/score           - Score responses"
echo "  GET    /api/assessments/available       - List all assessments"
echo "  GET    /api/assessments/{type}/info     - Assessment details"
echo "  GET    /api/assessments/history/{user}  - User history"
echo ""
echo "Report Endpoints:"
echo "  POST   /api/reports/generate            - Generate single report"
echo "  POST   /api/reports/batch-generate      - Multiple reports"
echo "  GET    /api/reports/formats             - Supported formats"
echo ""
echo "Chat Endpoint:"
echo "  POST   /chat                            - Multi-agent conversation"
echo ""
echo "Health Check:"
echo "  GET    /health                          - System status"
echo ""

# ============================================================
# SECTION 9: TESTING
# ============================================================

echo ""
echo "🧪 SECTION 9: TESTING"
echo "---"
echo ""
echo "Run edge case tests:"
echo "  pytest tests/test_edge_cases.py -v"
echo ""
echo "Test specific assessment:"
echo "  curl -X POST http://localhost:8000/api/assessments/start \\\\"
echo "    -H 'Content-Type: application/json' \\\\"
echo "    -d '{\"assessment_type\": \"phq9\", \"user_id\": \"test_user\"}'"
echo ""

# ============================================================
# SECTION 10: MONITORING & LOGS
# ============================================================

echo ""
echo "📊 SECTION 10: MONITORING & LOGS"
echo "---"
echo ""
echo "Backend logs: logs/backend.log"
echo "Frontend logs: logs/frontend.log"
echo "Database: psychology_chatbot.db"
echo "Vector store: data/vector_store/"
echo "Reports: generated_reports/"
echo ""

echo ""
echo "========================================================================"
echo "✅ SETUP COMPLETE!"
echo "========================================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Open 2 terminals and start services (see Section 6)"
echo "3. Access UI at http://localhost:8501"
echo ""
echo "For help:"
echo "- View API docs: http://localhost:8000/docs"
echo "- Check source: https://github.com/vaishnavkoka/psychology-chatbot"
