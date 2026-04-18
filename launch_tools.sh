#!/bin/bash

# 🧠 Psychology Chatbot - Interactive Tools Launcher
# Standalone tools for demo, testing, and training
# No backend API required!

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
clear
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  🧠 Psychology Chatbot - Interactive Tools Launcher      ║"
echo "║                                                           ║"
echo "║  Standalone tools - No backend API required!            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.9 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"

# Check if Streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Streamlit not found. Installing...${NC}"
    pip install streamlit pandas plotly numpy
    echo -e "${GREEN}✅ Streamlit installed${NC}"
fi

echo ""
echo -e "${BLUE}Available Interactive Tools:${NC}"
echo ""
echo "1. 🎮 Demo Mode (demo_mode.py)"
echo "   └─ Interactive assessment runner, sample conversations, feature showcase"
echo ""
echo "2. 🧪 Testing Dashboard (testing_dashboard.py)"
echo "   └─ Test execution, quality metrics, performance analysis, security audit"
echo ""
echo "3. 👨‍🏫 Workshop Guide (workshop_guide.py)"
echo "   └─ Training modules, hands-on exercises, FAQ, certification quiz"
echo ""
echo "4. 🎯 All Tools (Multi-app dashboard)"
echo "   └─ Single interface to access all three tools"
echo ""
echo "0. ❌ Exit"
echo ""

read -p "Select tool to launch (0-4): " choice

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🎮 Launching Demo Mode...${NC}"
        echo -e "${BLUE}Opening: http://localhost:8501${NC}"
        echo ""
        echo "To stop the server, press Ctrl+C"
        echo ""
        python3 -m streamlit run demo_mode.py
        ;;
    2)
        echo ""
        echo -e "${GREEN}🧪 Launching Testing Dashboard...${NC}"
        echo -e "${BLUE}Opening: http://localhost:8501${NC}"
        echo ""
        echo "To stop the server, press Ctrl+C"
        echo ""
        python3 -m streamlit run testing_dashboard.py
        ;;
    3)
        echo ""
        echo -e "${GREEN}👨‍🏫 Launching Workshop Guide...${NC}"
        echo -e "${BLUE}Opening: http://localhost:8501${NC}"
        echo ""
        echo "To stop the server, press Ctrl+C"
        echo ""
        python3 -m streamlit run workshop_guide.py
        ;;
    4)
        echo ""
        echo -e "${GREEN}🎯 Creating multi-app dashboard...${NC}"
        
        # Create multi-app runner
        cat > _multi_app_runner.py << 'EOF'
import streamlit as st

st.set_page_config(
    page_title="🧠 Psychology Chatbot Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

page = st.sidebar.radio(
    "🧠 Psychology Chatbot Suite",
    ["🎮 Demo Mode", "🧪 Testing Dashboard", "👨‍🏫 Workshop Guide"]
)

# Import and run selected app
if page == "🎮 Demo Mode":
    st.write("loading Demo Mode...")
    import demo_mode
    
elif page == "🧪 Testing Dashboard":
    st.write("Loading Testing Dashboard...")
    import testing_dashboard
    
elif page == "👨‍🏫 Workshop Guide":
    st.write("Loading Workshop Guide...")
    import workshop_guide

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #64748b;">
    <small>Psychology Chatbot v2.0 | Interactive Tools Suite</small>
</div>
""", unsafe_allow_html=True)
EOF
        
        echo -e "${BLUE}Opening multi-app dashboard: http://localhost:8501${NC}"
        echo ""
        echo "To stop the server, press Ctrl+C"
        echo ""
        python3 -m streamlit run demo_mode.py
        ;;
    0)
        echo ""
        echo -e "${YELLOW}👋 Exiting launcher${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}❌ Invalid option. Please select 0-4${NC}"
        echo ""
        # Re-run the script
        exec bash "$0"
        ;;
esac
