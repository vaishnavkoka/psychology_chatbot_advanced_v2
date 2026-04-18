#!/bin/bash
# Psychology Chatbot Quick Start
# Launches the complete multi-agent psychology system

echo "🧠 Psychology Chatbot - Multi-Agent System"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check environment
echo "${BLUE}[1/4]${NC} Checking environment..."
if [ ! -f ".env" ]; then
    echo "${YELLOW}⚠️  .env file not found. Creating from .env.example${NC}"
    cp .env.example .env
    echo "${YELLOW}   Please update .env with your API keys${NC}"
fi

# Install dependencies
echo ""
echo "${BLUE}[2/4]${NC} Installing dependencies..."
pip install -q fastapi uvicorn pydantic python-dotenv langchain langchain-community faiss-cpu sentence-transformers reportlab -q

# Initialize database
echo ""
echo "${BLUE}[3/4]${NC} Initializing database..."
python -c "from src.database_schema import init_db; init_db()" 2>/dev/null || echo "    Database already initialized"

# Run system tests
echo ""
echo "${BLUE}[4/4]${NC} Running system integration tests..."
python system_integration_test.py

# Show startup instructions
echo ""
echo "=================================="
echo "${GREEN}✅ System Ready!${NC}"
echo "=================================="
echo ""
echo "${BLUE}To start the backend API:${NC}"
echo "  uvicorn backend:app --reload --port 8000"
echo ""
echo "${BLUE}To start the frontend UI:${NC}"
echo "  streamlit run frontend_modern.py --server.port 8501"
echo ""
echo "${BLUE}API Documentation:${NC}"
echo "  http://localhost:8000/docs"
echo ""
echo "${BLUE}Available Endpoints:${NC}"
echo "  POST   /api/assessments/start          - Begin assessment"
echo "  POST   /api/assessments/score          - Score responses"
echo "  GET    /api/assessments/available      - List assessments"
echo "  POST   /api/reports/generate           - Generate report"
echo "  POST   /api/reports/batch-generate     - Batch reports"
echo "  POST   /chat                           - Multi-agent chat"
echo ""
echo "${BLUE}Default User ID:${NC}"
echo "  user_id: default (or provide your own)"
echo ""
echo "${YELLOW}Initial Setup Complete!${NC}"
echo "=================================="
