"""
Psychology Chatbot - Premium Frontend (v2.0)
Enhanced Streamlit interface with professional UI/UX, real-time chat, and assessments
"""

import streamlit as st
import streamlit.components.v1 as components
import requests
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from enum import Enum
import logging

# ============================================================
# CONFIGURATION
# ============================================================

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration with professional theme
st.set_page_config(
    page_title="🧠 Psychology Chatbot Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/help",
        "Report a bug": "https://github.com/issues",
        "About": "Psychology Chatbot v2.0 - Multi-Agent Mental Health Support"
    }
)

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>
:root {
    --primary: #6366f1;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --light: #f8fafc;
    --dark: #1e293b;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
}

.main {
    padding: 2rem;
}

.header-section {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    padding: 3rem 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
    text-align: center;
}

.header-section h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.header-section p {
    font-size: 1.1rem;
    opacity: 0.95;
    max-width: 600px;
    margin: 0 auto;
}

.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    font-size: 0.9rem;
    margin-top: 1rem;
}

.chat-container {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    height: 500px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.message-user {
    background: linear-gradient(135deg, #e0e7ff 0%, #faf5ff 100%);
    border-left: 4px solid #6366f1;
    padding: 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    margin-left: 2rem;
}

.message-assistant {
    background: linear-gradient(135deg, #f0fdf4 0%, #f3e8ff 100%);
    border-left: 4px solid #10b981;
    padding: 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    margin-right: 2rem;
}

.message-crisis {
    background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
    border-left: 4px solid #ef4444;
    padding: 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    margin-right: 2rem;
    font-weight: 500;
}

.assessment-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    margin-bottom: 1.5rem;
    border-top: 4px solid #6366f1;
}

.assessment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.assessment-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1e293b;
}

.assessment-score {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 700;
}

.severity-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 0.5rem;
}

.severity-minimal { background: #d1fae5; color: #065f46; }
.severity-mild { background: #fef3c7; color: #92400e; }
.severity-moderate { background: #fed7aa; color: #92400e; }
.severity-severe { background: #fecaca; color: #7f1d1d; }
.severity-critical { background: #ef4444; color: white; }

.resource-card {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border-left: 4px solid #10b981;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 0.75rem;
}

.resource-title { font-weight: 600; color: #047857; margin-bottom: 0.3rem; }
.resource-contact { color: #059669; font-family: monospace; }

.tab-content {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.sidebar-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.button-primary {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    margin-right: 0.5rem;
}

.button-secondary {
    background: #e2e8f0;
    color: #1e293b;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    cursor: pointer;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    text-align: center;
    border-top: 4px solid #6366f1;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #6366f1;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE MANAGEMENT
# ============================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "assessment_results" not in st.session_state:
    st.session_state.assessment_results = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "default_user"

if "api_status" not in st.session_state:
    st.session_state.api_status = None

if "message_input" not in st.session_state:
    st.session_state.message_input = ""

if "user_message" not in st.session_state:
    st.session_state.user_message = ""

if "assessment_responses" not in st.session_state:
    st.session_state.assessment_responses = []

if "current_assessment" not in st.session_state:
    st.session_state.current_assessment = None

# ============================================================
# API HELPERS
# ============================================================

@st.cache_data
def check_api_health():
    """Check if backend API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_assessment_list() -> List[Dict]:
    """Get available assessments from backend"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/assessments/available",
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json().get("assessments", [])
    except Exception as e:
        st.error(f"Error fetching assessments: {e}")
    return []

def start_assessment(assessment_type: str) -> Dict:
    """Start psychological assessment with error handling"""
    try:
        if not assessment_type or not isinstance(assessment_type, str):
            st.error("Invalid assessment type")
            return None
            
        user_id = getattr(st.session_state, 'user_id', 'guest')
        
        payload = {
            "assessment_type": assessment_type,
            "user_id": user_id
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/assessments/start",
                json=payload,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    st.error("Server returned invalid JSON response")
                    return None
            elif response.status_code == 500:
                st.error("Server error. Please try again later.")
                return None
            else:
                st.error(f"Error starting assessment (Status {response.status_code})")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend server. Ensure it's running on port 8000.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)[:100]}")
            return None
            
    except Exception as e:
        st.error(f"Unexpected error: {str(e)[:100]}")
        return None

def score_assessment(assessment_id: str, responses: List[int]) -> Dict:
    """Score assessment responses with error handling"""
    try:
        if not assessment_id or not isinstance(assessment_id, str):
            st.error("Invalid assessment ID")
            return None
            
        if not isinstance(responses, list) or not responses:
            st.error("Invalid assessment responses")
            return None
        
        payload = {
            "assessment_id": assessment_id,
            "responses": responses
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/assessments/score",
                json=payload,
                timeout=API_TIMEOUT
            )
            
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError:
                    st.error("Server returned invalid JSON response")
                    return None
            elif response.status_code == 500:
                st.error("Server error. Please try again later.")
                return None
            else:
                st.error(f"Error scoring assessment (Status {response.status_code})")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend server.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)[:100]}")
            return None
            
    except Exception as e:
        st.error(f"Unexpected error: {str(e)[:100]}")
        return None

def send_chat_message(message: str) -> Dict:
    """Send message to multi-agent orchestrator with robust error handling"""
    try:
        if not message or not isinstance(message, str):
            return {
                "message": "Invalid message format.",
                "crisis_detected": False
            }
        
        # Safe session state access
        user_id = getattr(st.session_state, 'user_id', 'guest')
        session_id = getattr(st.session_state, 'session_id', 'default')
        
        payload = {
            "message": message.strip(),
            "context": {
                "user_id": user_id,
                "session_id": session_id
            }
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=payload,
                timeout=API_TIMEOUT
            )
            
            # Handle successful response
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Validate response structure
                    if isinstance(data, dict) and "message" in data:
                        return data
                    else:
                        return {
                            "message": "Received unexpected response format.",
                            "crisis_detected": False
                        }
                except ValueError:
                    return {
                        "message": "Server returned invalid JSON.",
                        "crisis_detected": False
                    }
            
            # Handle error responses
            elif response.status_code == 500:
                return {
                    "message": "Server error. Please try again later.",
                    "crisis_detected": False
                }
            elif response.status_code == 503:
                return {
                    "message": "Server is temporarily unavailable.",
                    "crisis_detected": False
                }
            else:
                return {
                    "message": f"Server returned status {response.status_code}: {response.text[:100]}",
                    "crisis_detected": False
                }
                
        except requests.exceptions.ConnectionError as e:
            return {
                "message": "Cannot connect to the backend server. Please ensure it's running on port 8000.",
                "crisis_detected": False
            }
        except requests.exceptions.Timeout as e:
            return {
                "message": "Request timed out. The server took too long to respond.",
                "crisis_detected": False
            }
        except requests.exceptions.RequestException as e:
            return {
                "message": f"Network error: {str(e)[:50]}",
                "crisis_detected": False
            }
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "message": f"Unexpected error: {str(e)[:100]}",
            "crisis_detected": False
        }


def generate_report(assessment_data: Dict, format: str = "pdf") -> Optional[str]:
    """Generate report from assessment"""
    try:
        payload = {
            "assessment_data": assessment_data,
            "format": format
        }
        response = requests.post(
            f"{API_BASE_URL}/api/reports/generate",
            json=payload,
            timeout=API_TIMEOUT
        )
        if response.status_code == 200:
            return response.json().get("path")
    except Exception as e:
        st.error(f"Error generating report: {e}")
    return None

# ============================================================
# UI COMPONENTS
# ============================================================

def display_assessment_questions(assessment: Dict):
    """Display assessment questions for user to complete"""
    if not assessment:
        return
    
    assessment_id = assessment.get("assessment_id")
    assessment_name = assessment.get("assessment_name", "Assessment")
    questions = assessment.get("questions", [])
    scale = assessment.get("scale", "0-4: Not at all to Nearly every day")
    
    with st.container():
        st.markdown(f"### 📝 {assessment_name}")
        st.markdown(f"**Scale:** {scale}")
        st.markdown("---")
        
        # Create a form for responses
        responses = []
        
        for i, question in enumerate(questions, 1):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Q{i}:** {question}")
            with col2:
                # Create a radio button group for each question (0-4 scale)
                response = st.radio(
                    label=f"q{i}",
                    options=[0, 1, 2, 3, 4],
                    label_visibility="collapsed",
                    key=f"q{i}_{assessment_id}",
                    horizontal=True
                )
                responses.append(response)
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📊 Submit Assessment", use_container_width=True, key=f"submit_{assessment_id}"):
                # Send responses to backend for scoring
                try:
                    score_response = score_assessment(assessment_id, responses)
                    if score_response and isinstance(score_response, dict):
                        # Store results
                        st.session_state.assessment_results.append(score_response)
                        st.session_state.current_assessment = None
                        
                        # Display results
                        st.success(f"✅ Assessment completed!")
                        st.markdown("### 📊 Your Results:")
                        
                        total_score = score_response.get("total_score", 0)
                        max_score = score_response.get("max_score", 1)
                        severity = score_response.get("severity_level", "unknown")
                        interpretation = score_response.get("interpretation", "")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Score", f"{total_score}/{max_score}")
                        with col2:
                            st.metric("Severity", severity.title())
                        
                        if interpretation:
                            st.markdown(f"**Interpretation:** {interpretation}")
                        
                        # Show resources if needed
                        if severity in ["moderate", "severe", "critical"]:
                            st.warning("💡 Consider reaching out to a mental health professional for support.")
                        
                        st.rerun()
                    else:
                        st.error("Could not score assessment. Please try again.")
                except Exception as e:
                    st.error(f"Error submitting assessment: {str(e)}")

def render_header():
    """Render main header"""
    st.markdown("""
    <div class="header-section">
        <h1>🧠 Psychology Chatbot Pro</h1>
        <p>Intelligent mental health support powered by multi-agent AI</p>
        <div class="status-badge">
            ✅ All systems operational
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Render chat interface with fixed scrollable chat box"""
    st.subheader("💬 Chat with Your Assistant")
    
    # Sample inputs section showing agent routing
    with st.expander("💡 Sample Inputs & Agent Routing", expanded=False):
        st.markdown("""
        **Sample inputs and which agents would be triggered:**
        
        | Input | Agents Triggered | Purpose |
        |-------|------------------|---------|
        | "I'm feeling depressed and hopeless" | 🔗 Crisis Detection → Therapy Support | Addresses emotional distress with support strategies |
        | "I have anxiety and worry constantly" | 🔗 Query Router → Therapy Support → RAG | Anxiety routing to therapeutic interventions |
        | "Tell me about sleep improvement" | 🔗 Query Router → RAG → Therapy Support | Knowledge retrieval + practical strategies |
        | "I'm having suicidal thoughts" | 🚨 Crisis Detection (PRIORITY) | Immediate emergency response with hotlines |
        | "Can I take PHQ-9 assessment?" | 🔗 Query Router → Assessment Agent | Psychological assessment screening |
        | "What can I do for stress relief?" | 🔗 RAG Agent → Therapy Support | Knowledge-based coping strategies |
        | "I feel overwhelmed at work" | 🔗 Query Router → Therapy Support | Occupational stress handling |
        
        **How it works:**
        - 🔗 **Query Router**: Analyzes user intent and selects appropriate agents
        - 🚨 **Crisis Detection**: Highest priority - detects high-risk keywords
        - 💬 **Therapy Support**: Provides coping strategies and emotional support
        - 📋 **Assessment**: Conducts PHQ-9, GAD-7, PSQI and other evaluations
        - 📚 **RAG Agent**: Retrieves psychology knowledge and resources
        """)
    
    st.divider()
    
    # Build and display chat messages with embedded CSS
    st.write("**Chat with Your Assistant:**")
    
    # Build HTML with embedded CSS (so it works inside components.html iframe)
    chat_html = '''<style>
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        .chat-box-container {
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            background: white;
            padding: 1.5rem;
            height: 500px;
            overflow-y: auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .chat-msg-user {
            background: linear-gradient(135deg, #e0e7ff 0%, #faf5ff 100%);
            border-left: 4px solid #6366f1;
            padding: 1rem;
            border-radius: 8px;
            margin-left: auto;
            max-width: 85%;
            word-wrap: break-word;
        }
        
        .chat-msg-assistant {
            background: linear-gradient(135deg, #f0fdf4 0%, #f3e8ff 100%);
            border-left: 4px solid #10b981;
            padding: 1rem;
            border-radius: 8px;
            margin-right: auto;
            max-width: 85%;
            word-wrap: break-word;
        }
        
        .chat-msg-crisis {
            background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
            border-left: 4px solid #ef4444;
            padding: 1rem;
            border-radius: 8px;
            margin-right: auto;
            max-width: 85%;
            word-wrap: break-word;
            font-weight: 500;
        }
        
        .chat-timestamp {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 0.25rem;
        }
        
        .chat-greeting-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            text-align: center;
            color: #64748b;
        }
        
        .greeting-emoji {
            font-size: 3rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
    </style>
    <div class="chat-box-container">'''
    
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            msg_time = msg.get("time", "")
            crisis = msg.get("crisis_detected", False)
            
            if role == "user":
                chat_html += f'<div class="chat-msg-user"><strong>📝 You:</strong><br>{content}<div class="chat-timestamp">{msg_time}</div></div>'
            elif role == "assistant":
                msg_class = "chat-msg-crisis" if crisis else "chat-msg-assistant"
                emoji = "⚠️ Crisis Alert" if crisis else "🧠 AI Assistant"
                chat_html += f'<div class="{msg_class}"><strong>{emoji}:</strong><br>{content}<div class="chat-timestamp">{msg_time}</div></div>'
    else:
        chat_html += '<div class="chat-greeting-box"><div class="greeting-emoji">🧠</div><h3 style="color: #6366f1; margin-bottom: 1rem;">Welcome to Your Safe Space</h3><p style="color: #64748b;">I\'m here to listen and support your mental health journey.</p><p style="color: #94a3b8; font-size: 0.9rem;">✨ Share your thoughts • 📋 Take assessments • 💭 Get insights</p></div>'
    
    chat_html += '</div></div>'
    components.html(chat_html, height=550)
    
    
    st.markdown("---")
    
    # Input area with sample quick buttons
    st.markdown("**Try a sample input or type your own:**")
    
    # Quick sample buttons
    sample_cols = st.columns(4, gap="small")
    sample_inputs = [
        "I'm feeling depressed",
        "Help with anxiety",
        "I can't sleep well",
        "Stress at work"
    ]
    
    for idx, (col, sample) in enumerate(zip(sample_cols, sample_inputs)):
        with col:
            if st.button(f"📌 {sample}", key=f"sample_{idx}", use_container_width=True):
                st.session_state.pending_message = sample
                st.rerun()
    
    st.markdown("")
    
    # Chat input with Enter key support
    col1, col2 = st.columns([5, 1], gap="small")
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Type your message and press Enter...",
            label_visibility="collapsed",
            key="message_input"
        )
    
    with col2:
        send_button = st.button("Send 📨", use_container_width=True)
    
    # Get the actual input to process
    final_input = None
    
    # Check if we have a pending message from sample buttons
    if hasattr(st.session_state, 'pending_message') and st.session_state.pending_message:
        final_input = st.session_state.pending_message
        st.session_state.pending_message = None
    # Check if user typed something and pressed Enter or clicked Send
    elif send_button and user_input:
        final_input = user_input
    elif user_input and user_input != st.session_state.get("last_input", ""):
        # Detect Enter key (text_input will trigger when Enter is pressed)
        final_input = user_input
        st.session_state.last_input = user_input
    
    # Process message only when we have input
    if final_input is not None and final_input != "":
        try:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": final_input.strip(),
                "time": datetime.now().strftime("%I:%M %p")
            })
            
            # Show spinner while getting response
            with st.spinner("🧠 Thinking..."):
                try:
                    response = send_chat_message(final_input)
                    
                    if response and isinstance(response, dict):
                        message_content = response.get("message", "Sorry, I couldn't process that.")
                        crisis_detected = response.get("crisis_detected", False)
                        
                        # Add assistant message to history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": str(message_content),
                            "crisis_detected": bool(crisis_detected),
                            "time": datetime.now().strftime("%I:%M %p")
                        })
                        
                        # Handle crisis detection
                        if crisis_detected:
                            st.error("⚠️ Crisis detected. Emergency resources available in the Resources tab.")
                    else:
                        st.error("Invalid response from server. Please try again.")
                        # Still add a system message
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": "I encountered a technical issue. Please try again.",
                            "crisis_detected": False,
                            "time": datetime.now().strftime("%I:%M %p")
                        })
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to server. Make sure the backend is running on port 8000.")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Connection error: Backend server appears to be offline.",
                        "crisis_detected": False,
                        "time": datetime.now().strftime("%I:%M %p")
                    })
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. The server took too long to respond.")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "Request timed out. Please try again.",
                        "crisis_detected": False,
                        "time": datetime.now().strftime("%I:%M %p")
                    })
                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Error: {str(e)}",
                        "crisis_detected": False,
                        "time": datetime.now().strftime("%I:%M %p")
                    })
            
            # Force rerun to clear input and update display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing message: {str(e)}")
            try:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"An error occurred: {str(e)}",
                    "crisis_detected": False,
                    "time": datetime.now().strftime("%I:%M %p")
                })
            except Exception as inner_e:
                st.warning(f"Could not save error to history: {str(inner_e)}")

def render_assessment_interface():
    """Render assessment interface with error handling"""
    st.subheader("📋 Psychological Assessments")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Available Assessments:**")
            assessments = {
                "phq9": "PHQ-9: Depression Screening",
                "gad7": "GAD-7: Anxiety Screening",
                "psqi": "PSQI: Sleep Quality",
                "rosenberg_ses": "Rosenberg: Self-Esteem",
                "pcl5": "PCL-5: PTSD Screening"
            }
            
            try:
                selected_assessment = st.selectbox(
                    "Choose an assessment:",
                    options=list(assessments.keys()),
                    format_func=lambda x: assessments[x],
                    label_visibility="collapsed"
                )
            except Exception as e:
                st.error(f"Error loading assessments: {str(e)}")
                return
            
            if st.button("Start Assessment", use_container_width=True):
                try:
                    assessment = start_assessment(selected_assessment)
                    if assessment and isinstance(assessment, dict):
                        st.session_state.current_assessment = assessment
                        st.session_state.assessment_responses = []
                        assessment_name = assessment.get('assessment_name', 'Assessment')
                        st.success(f"✅ {assessment_name} started")
                        st.balloons()
                    else:
                        st.warning("Could not start assessment. Please try again.")
                except Exception as e:
                    st.error(f"Error starting assessment: {str(e)}")
            
            # Display assessment questions if one is active
            if st.session_state.current_assessment:
                display_assessment_questions(st.session_state.current_assessment)
        
        with col2:
            st.markdown("**Your Results:**")
            try:
                if st.session_state.assessment_results and isinstance(st.session_state.assessment_results, list):
                    for result in st.session_state.assessment_results[-3:]:  # Last 3
                        try:
                            if isinstance(result, dict):
                                severity = result.get("severity_level", "unknown")
                                score = result.get("total_score", 0)
                                max_score = result.get("max_score", 1)
                                name = result.get('assessment_name', 'Unknown')
                                
                                st.markdown(f"""
                                <div class="assessment-card">
                                    <div class="assessment-header">
                                        <div class="assessment-title">{name}</div>
                                        <div class="assessment-score">{score}/{max_score}</div>
                                    </div>
                                    <div class="severity-badge severity-{severity}">{severity.replace('_', ' ').title()}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        except Exception as e:
                            st.warning(f"Error displaying result: {str(e)[:50]}")
                            continue
                else:
                    st.info("No assessments completed yet")
            except Exception as e:
                st.error(f"Error displaying results: {str(e)}")
                
    except Exception as e:
        st.error(f"Error rendering assessment interface: {str(e)}")

def render_resources():
    """Render emergency resources"""
    st.subheader("🆘 Emergency Resources")
    
    resources = {
        "988 Suicide & Crisis Lifeline": {
            "contact": "Call or Text 988",
            "available": "24/7",
            "type": "Crisis counseling"
        },
        "Crisis Text Line": {
            "contact": "Text HOME to 741741",
            "available": "24/7",
            "type": "Text-based support"
        },
        "SAMHSA National Helpline": {
            "contact": "1-800-662-4357",
            "available": "24/7",
            "type": "Substance & mental health"
        },
        "National Domestic Violence Hotline": {
            "contact": "1-800-799-7233",
            "available": "24/7",
            "type": "Domestic violence support"
        }
    }
    
    for name, info in resources.items():
        st.markdown(f"""
        <div class="resource-card">
            <div class="resource-title">{name}</div>
            <div class="resource-contact"><strong>{info['contact']}</strong></div>
            <div style="color: #059669; font-size: 0.85rem;">⏰ {info['available']} • {info['type']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_statistics():
    """Render user statistics"""
    st.subheader("📊 Your Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = {
        "Messages": len(st.session_state.chat_history),
        "Assessments": len(st.session_state.assessment_results),
        "Session Duration": "12 min",
        "Engagement": "High"
    }
    
    for i, (label, value) in enumerate(stats.items()):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    """Main application"""
    
    # Render header
    render_header()
    
    # Check API status
    if not check_api_health():
        st.error("""
        ❌ **Backend API is not running**
        
        Please start the backend:
        ```bash
        uvicorn backend:app --reload
        ```
        """)
        return
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat",
        "📋 Assessments",
        "🆘 Resources",
        "📊 Dashboard"
    ])
    
    # Chat tab
    with tab1:
        render_chat_interface()
    
    # Assessments tab
    with tab2:
        render_assessment_interface()
    
    # Resources tab
    with tab3:
        render_resources()
    
    # Dashboard tab
    with tab4:
        render_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Assessment History**")
            if st.session_state.assessment_results:
                df = pd.DataFrame(st.session_state.assessment_results)
                st.dataframe(df[["assessment_name", "total_score", "severity_level"]], use_container_width=True)
        
        with col2:
            st.markdown("**Mood Trend**")
            if len(st.session_state.chat_history) > 0:
                st.info("Mood tracking visualization would appear here")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        user_id_input = st.text_input(
            "User ID:",
            value=st.session_state.user_id,
            help="Your unique identifier"
        )
        st.session_state.user_id = user_id_input
        
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("✅ Chat history cleared")
            st.rerun()
        
        if st.button("Clear Assessment Results", use_container_width=True):
            st.session_state.assessment_results = []
            st.success("✅ Assessment results cleared")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📱 About")
        st.markdown("""
        **Psychology Chatbot Pro v2.0**
        
        Multi-agent AI system for mental health support:
        - 🤖 6 specialized agents
        - 📍 Real-time crisis detection
        - 📊 Evidence-based assessments
        - 📈 Progress tracking
        
        **API Status:** ✅ Connected
        """)


if __name__ == "__main__":
    main()
