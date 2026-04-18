"""
Modern Psychology Chatbot Frontend - Streamlit UI
Enhanced interface with better layout, styling, and visualizations
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🧠 Psychology Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #0f172a;
        --light-bg: #f8fafc;
    }
    
    /* Customize main container */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .header-container p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        word-wrap: break-word;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #e0e7ff 0%, #faf5ff 100%);
        border-left: 4px solid #6366f1;
        margin-left: 1rem;
    }
    
    .chat-message.assistant {
        background: linear-gradient(135deg, #f0fdf4 0%, #f3e8ff 100%);
        border-left: 4px solid #10b981;
        margin-right: 1rem;
    }
    
    .chat-message.crisis {
        background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
        border-left: 4px solid #ef4444;
        margin-right: 1rem;
    }
    
    .message-timestamp {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    /* Input styling */
    .input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .input-container:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Metrics card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-top: 3px solid #6366f1;
    }
    
    .metric-card.warning {
        border-top-color: #f59e0b;
    }
    
    .metric-card.danger {
        border-top-color: #ef4444;
    }
    
    .metric-card.success {
        border-top-color: #10b981;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .status-badge.active {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-badge.inactive {
        background: #f3f4f6;
        color: #374151;
    }
    
    .status-badge.crisis {
        background: #fee2e2;
        color: #7f1d1d;
    }
    
    /* Button styling */
    .custom-button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: transform 0.2s ease;
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    .sidebar-section {
        margin-bottom: 2rem;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .sidebar-section h3 {
        color: #6366f1;
        margin-top: 0;
        font-size: 1.1rem;
    }
    
    /* Tabbed interface */
    .tabs-container {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .tab-button {
        padding: 0.75rem 1.5rem;
        background: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        color: #64748b;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .tab-button.active {
        color: #6366f1;
        border-bottom-color: #6366f1;
    }
    
    /* Animation */
    @keyframes slide-in {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chat-message {
        animation: slide-in 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{int(time.time())}"

if "orchestrator_results" not in st.session_state:
    st.session_state.orchestrator_results = []

if "crisis_events" not in st.session_state:
    st.session_state.crisis_events = []

# API configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

# Helper functions
def call_api(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Optional[Dict]:
    """Call backend API safely"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "POST":
            response = requests.post(url, json=data, timeout=API_TIMEOUT)
        else:
            response = requests.get(url, timeout=API_TIMEOUT)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Is the server running?")
        return None
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None

def send_message(user_input: str) -> Optional[Dict]:
    """Send message to chatbot"""
    if not user_input.strip():
        return None
    
    # Add user message to history
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Call API
    response = call_api(
        "/chat",
        method="POST",
        data={
            "message": user_input,
            "context": {}
        }
    )
    
    if response:
        # Add assistant response to history
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": response.get("message", "I'm here to help."),
            "timestamp": datetime.now().isoformat(),
            "agent": response.get("agent", "Unknown"),
            "crisis_detected": response.get("crisis_detected", False)
        })
        
        # Track orchestrator results
        st.session_state.orchestrator_results.append(response)
        
        # Track crisis events
        if response.get("crisis_detected"):
            st.session_state.crisis_events.append({
                "timestamp": datetime.now().isoformat(),
                "description": f"Crisis detected - Risk level: {response.get('risk_level', 'unknown')}"
            })
        
        return response
    
    return None

# Header
st.markdown("""
<div class="header-container">
    <h1>🧠 Psychology Support Chatbot</h1>
    <p>AI-powered mental health support with LangGraph orchestration</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Session Dashboard")
    
    # Session info
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.metric("Session ID", st.session_state.session_id[:12] + "...")
        st.metric("Messages", len(st.session_state.conversation_history))
        st.metric("Crisis Events", len(st.session_state.crisis_events))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Orchestrator status
    st.markdown("### 🤖 Orchestrator Status")
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        
        status_response = call_api("/orchestrator/status")
        if status_response and status_response.get("status") == "ready":
            st.markdown(f'<span class="status-badge active">✓ Ready</span>', unsafe_allow_html=True)
            
            agents = status_response.get("agents", [])
            st.write(f"**Agents:** {len(agents)}")
            
            for agent in agents[:3]:
                st.caption(f"✓ {agent['name']}")
        else:
            st.markdown(f'<span class="status-badge inactive">⚠ Initializing</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Knowledge base
    st.markdown("### 📚 Knowledge Base")
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        
        kb_response = call_api("/knowledge/sources")
        if kb_response:
            sources = kb_response.get("sources", [])
            st.write(f"**{kb_response.get('total_entries')} entries** available")
            st.caption(kb_response.get("total_content", ""))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Actions
    st.markdown("### ⚙️ Actions")
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        
        if st.button("📄 Generate Report", key="report_btn", use_container_width=True):
            st.info("Report generation coming in Phase 3A...")
        
        if st.button("🗑️ Clear Conversation", key="clear_btn", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.orchestrator_results = []
            st.session_state.crisis_events = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.markdown("### 💬 Conversation")
    
    # Chat display container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.conversation_history:
            role = message["role"]
            content = message["content"]
            timestamp = message.get("timestamp", "")
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <strong>You:</strong><br>
                    {content}
                    <div class="message-timestamp">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                agent = message.get("agent", "Assistant")
                crisis = message.get("crisis_detected", False)
                
                message_class = "crisis" if crisis else "assistant"
                st.markdown(f"""
                <div class="chat-message {message_class}">
                    <strong>🧠 {agent}:</strong><br>
                    {content}
                    <div class="message-timestamp">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("### 📝 Your Message")
    
    col_input, col_send = st.columns([5, 1], gap="small")
    
    with col_input:
        user_input = st.text_input(
            "Enter your message here...",
            key="message_input",
            placeholder="How are you feeling today?",
            label_visibility="collapsed"
        )
    
    with col_send:
        if st.button("📤", key="send_btn", help="Send message", use_container_width=True):
            if user_input:
                with st.spinner("Thinking..."):
                    send_message(user_input)
                
                # Clear input
                st.session_state.message_input = ""
                st.rerun()

with col2:
    st.markdown("### 📈 Session Analytics")
    
    # Metrics
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        
        total_messages = len(st.session_state.conversation_history)
        total_exchanges = total_messages // 2
        
        st.metric("Total Exchanges", total_exchanges)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Agent distribution
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        
        agents_used = {}
        for result in st.session_state.orchestrator_results:
            agent = result.get("agent_used", "Unknown")
            agents_used[agent] = agents_used.get(agent, 0) + 1
        
        if agents_used:
            st.write("**Agents Used:**")
            for agent, count in agents_used.items():
                st.caption(f"✓ {agent}: {count}")
        else:
            st.caption("No agents used yet")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Crisis status
    with st.container():
        crisis_count = len(st.session_state.crisis_events)
        card_class = "danger" if crisis_count > 0 else "success"
        
        st.markdown(f'<div class="metric-card {card_class}">', unsafe_allow_html=True)
        
        if crisis_count > 0:
            st.warning(f"⚠️ **Crisis Events:** {crisis_count}")
        else:
            st.success("✓ No crisis events detected")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sentiment trend
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        
        if len(st.session_state.conversation_history) > 0:
            # Simple sentiment from last message
            last_msg = st.session_state.conversation_history[-1].get("content", "").lower()
            
            positive_indicators = ["better", "good", "great", "happy", "hope"]
            if any(word in last_msg for word in positive_indicators):
                st.success("📈 Trending positive")
            else:
                st.info("📊 Neutral")
        else:
            st.caption("No messages yet")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem;">
    <p>🧠 Psychology Chatbot v2.0 | Powered by LangGraph & FAISS | <a href="#" style="color: #6366f1;">Help</a> | <a href="#" style="color: #6366f1;">Privacy</a></p>
</div>
""", unsafe_allow_html=True)
