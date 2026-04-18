"""
Psychology Chatbot Frontend - Enhanced Streamlit UI
Interactive interface with crisis detection and safety measures
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Psychology Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Styles with more accessible design
st.markdown("""
    <style>
    .header-color { color: #2E86AB; font-weight: bold; font-size: 28px; }
    .support-box { background-color: #F0F8FF; padding: 15px; border-radius: 10px; border-left: 4px solid #2E86AB; }
    .assessment-box { background-color: #F0FFF4; padding: 15px; border-radius: 10px; border-left: 4px solid #31a24c; }
    .mindfulness-box { background-color: #FFF9E6; padding: 15px; border-radius: 10px; border-left: 4px solid #f39c12; }
    .warning-box { background-color: #FFE6E6; padding: 15px; border-radius: 10px; border-left: 5px solid #FF6B6B; }
    .critical-box { background-color: #FF6B6B; padding: 20px; border-radius: 10px; border-left: 5px solid #cc0000; color: white; font-weight: bold; }
    .caution-box { background-color: #FFD700; padding: 15px; border-radius: 10px; border-left: 5px solid #FF8C00; font-weight: bold; }
    .info-box { background-color: #E3F2FD; padding: 15px; border-radius: 10px; border-left: 4px solid #2196F3; }
    .success-box { background-color: #E8F5E9; padding: 15px; border-radius: 10px; border-left: 4px solid #4CAF50; }
    .chat-message { padding: 10px; margin: 10px 0; border-radius: 8px; }
    .user-message { background-color: #E3F2FD; margin-left: 20px; }
    .bot-message { background-color: #F5F5F5; margin-right: 20px; }
    </style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assessment_results" not in st.session_state:
    st.session_state.assessment_results = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "crisis_history" not in st.session_state:
    st.session_state.crisis_history = []
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"

# Helper functions
def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def detect_crisis(message):
    """Detect crisis in message"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/safety/detect-crisis",
            json={"message": message},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error in crisis detection: {e}")
        return None

def get_emergency_resources():
    """Get emergency resources"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/safety/emergency-resources",
            timeout=2
        )
        return response.json() if response.status_code == 200 else None
    except:
        return None

def get_assessments():
    """Get available assessments"""
    try:
        response = requests.get(f"{BACKEND_URL}/assessments")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching assessments: {e}")
        return None

def get_exercises():
    """Get mindfulness exercises"""
    try:
        response = requests.get(f"{BACKEND_URL}/exercises")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching exercises: {e}")
        return None

def conduct_assessment(assessment_id, responses):
    """Conduct assessment"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/assessment/conduct",
            json={"assessment_id": assessment_id, "responses": responses}
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error conducting assessment: {e}")
        return None

def get_support(issue, severity=3):
    """Get support message"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/support",
            json={"issue": issue, "severity": severity}
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error getting support: {e}")
        return None

def chat_with_bot(message, context=None):
    """Send message to chatbot with crisis detection"""
    try:
        # First, detect crisis
        crisis_data = detect_crisis(message)
        
        # Send to chat endpoint
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": message, "context": context},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            # Include crisis data in result
            if crisis_data:
                result["crisis_data"] = crisis_data
            return result
        return None
    except Exception as e:
        st.error(f"Error in chat: {e}")
        return None

def display_crisis_warning(crisis_data):
    """Display crisis warning based on risk level"""
    if not crisis_data:
        return
    
    risk_level = crisis_data.get("risk_level", "green")
    confidence = crisis_data.get("confidence", 0)
    safety_message = crisis_data.get("safety_message", "")
    
    if risk_level == "red":
        st.markdown(f'<div class="critical-box">🚨 CRITICAL ALERT 🚨<br>{safety_message}</div>', 
                   unsafe_allow_html=True)
        
        # Display emergency resources
        emergency = get_emergency_resources()
        if emergency and emergency.get("resources"):
            st.markdown("### 📞 Emergency Resources Available NOW:")
            resources = emergency.get("resources", {}).get("US", {})
            for resource_type, resource_info in resources.items():
                if isinstance(resource_info, dict):
                    st.info(f"**{resource_info.get('name', resource_type)}**\n{resource_info.get('number', resource_info.get('text', ''))}\n{resource_info.get('description', '')}")
    
    elif risk_level == "orange":
        st.markdown(f'<div class="caution-box">⚠️ CAUTION: Professional Help Recommended<br>{safety_message}</div>', 
                   unsafe_allow_html=True)
    
    elif risk_level == "yellow":
        st.markdown(f'<div class="warning-box">💙 Mental Health Support Available<br>{safety_message}</div>', 
                   unsafe_allow_html=True)

def display_header():
    """Display application header with safety information"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<p class="header-color">🧠 Psychology Chatbot</p>', unsafe_allow_html=True)
        st.markdown("*Comprehensive mental health support and assessment platform*")
    
    with col2:
        if check_backend():
            st.success("✅ System Online")
        else:
            st.error("❌ System Offline")

def display_crisis_disclaimer():
    """Display crisis support disclaimer"""
    st.markdown("""
    ---
    ⚠️ **Important**: This chatbot provides supportive guidance but is **NOT a substitute for professional mental health care**.
    
    ✅ **For Immediate Help:**
    - 🆘 **Call 911** (US Emergency)
    - 📞 **Call 988** (Suicide & Crisis Lifeline - US, 24/7)
    - 💬 **Text "HELLO" to 741741** (Crisis Text Line - US, 24/7)
    
    If you're experiencing a mental health crisis, **please seek professional help immediately**.
    ---
    """)

def page_home():
    """Home page"""
    display_header()
    display_crisis_disclaimer()
    
    st.markdown("## Welcome to Your Mental Health Support Portal 💚")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="assessment-box">
        <h3>📊 Self Assessments</h3>
        <p>Take validated psychological assessments to understand your mental health better.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="support-box">
        <h3>💬 Support Chat</h3>
        <p>Chat with our AI assistant for immediate emotional support and guidance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="mindfulness-box">
        <h3>🧘 Mindfulness</h3>
        <p>Practice guided mindfulness exercises to manage stress and anxiety.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("## Quick Start")
    
    quick_options = st.radio(
        "What would you like to do?",
        ["Chat with Assistant", "Take an Assessment", "Practice Mindfulness", "Get Resources"],
        horizontal=True
    )
    
    if quick_options == "Chat with Assistant":
        st.session_state.current_page = "chat"
        st.rerun()
    elif quick_options == "Take an Assessment":
        st.session_state.current_page = "assessments"
        st.rerun()
    elif quick_options == "Practice Mindfulness":
        st.session_state.current_page = "mindfulness"
        st.rerun()
    elif quick_options == "Get Resources":
        st.session_state.current_page = "resources"
        st.rerun()

def page_chat():
    """Chat page with crisis detection"""
    display_header()
    
    st.markdown("## Emotional Support Chat")
    st.markdown("Share what's on your mind. Our AI assistant is here to listen and support you.")
    
    # Display previous messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 **You**: {message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 **Assistant**: {message["content"]}</div>', 
                       unsafe_allow_html=True)
            
            # Display crisis warnings if present
            if "crisis_data" in message:
                display_crisis_warning(message["crisis_data"])
    
    # Input area with Enter key support
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="Share what you're experiencing... (Press Enter to send)",
            key="chat_input"
        )
    
    with col2:
        st.write("")  # spacing
        send_clicked = st.button("📤", type="primary")
    
    # Submit on Enter key or button click
    if user_input or send_clicked:
        if user_input.strip():
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get bot response with crisis detection
            with st.spinner("Analyzing and responding..."):
                response = chat_with_bot(user_input)
            
            if response:
                # Add bot message
                bot_message = response.get("message", "I understand you're going through something. Tell me more.")
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": bot_message,
                    "crisis_data": response.get("crisis_data")
                })
                
                # Display the response and any crisis warnings
                st.markdown(f'<div class="chat-message bot-message">🤖 **Assistant**: {bot_message}</div>', 
                           unsafe_allow_html=True)
                
                if "crisis_data" in response:
                    display_crisis_warning(response["crisis_data"])
                
                # Clear the input field
                st.session_state.chat_input = ""
                st.rerun()
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

def page_assessments():
    """Assessments page"""
    display_header()
    
    st.markdown("## Psychological Assessments")
    st.markdown("Take validated assessments to understand your mental health better.")
    
    assessments_data = get_assessments()
    
    if not assessments_data or not assessments_data.get("assessments"):
        st.error("Failed to load assessments")
        return
    
    assessments = assessments_data.get("assessments", [])
    
    for assessment in assessments:
        with st.expander(f"📋 {assessment['name']} - {assessment['type']}"):
            st.markdown(f"{assessment['questions_count']} questions | Estimated time: 5-10 minutes")
            
            if st.button(f"Start Assessment", key=assessment["id"]):
                st.session_state.current_page = f"assessment_{assessment['id']}"
                st.rerun()
    
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

def page_conduct_assessment(assessment_id):
    """Conduct a specific assessment"""
    display_header()
    
    st.markdown(f"## Taking Assessment")
    assessments_data = get_assessments()
    
    if not assessments_data:
        st.error("Failed to load assessments")
        if st.button("← Back"):
            st.session_state.current_page = "assessments"
            st.rerun()
        return
    
    assessments = {a['id']: a for a in assessments_data.get("assessments", [])}
    if assessment_id not in assessments:
        st.error("Assessment not found")
        if st.button("← Back"):
            st.session_state.current_page = "assessments"
            st.rerun()
        return
    
    assessment = assessments[assessment_id]
    st.markdown(f"### {assessment['name']}")
    st.markdown(f"{assessment['description']}")
    
    st.markdown("---")
    st.markdown("**Answer each question on a scale of 0-4**")
    
    # Create a form to capture responses
    with st.form(f"assessment_form_{assessment_id}"):
        responses = []
        for idx, question in enumerate(assessment.get("questions", []), 1):
            response = st.radio(
                f"{idx}. {question}",
                options=[0, 1, 2, 3, 4],
                key=f"q_{assessment_id}_{idx}"
            )
            responses.append(response)
        
        if st.form_submit_button("Submit Assessment", type="primary"):
            with st.spinner("Analyzing results..."):
                result = conduct_assessment(assessment_id, responses)
                if result:
                    st.session_state.assessment_results = result
                    st.success("✅ Assessment completed!")
                    st.markdown(f"**Score:** {result.get('score', 'N/A')}")
                    st.markdown(f"**Interpretation:** {result.get('interpretation', 'N/A')}")
                    st.markdown("---")
                    st.markdown("**Recommendations:**")
                    for rec in result.get('recommendations', []):
                        st.markdown(f"• {rec}")
                    if st.button("Continue →"):
                        st.session_state.current_page = "assessments"
                        st.rerun()
                else:
                    st.error("Error processing assessment")

def page_mindfulness():
    """Mindfulness page"""
    display_header()
    
    st.markdown("## Mindfulness Exercises")
    st.markdown("Practice guided exercises to reduce stress and improve wellbeing.")
    
    exercises_data = get_exercises()
    
    if not exercises_data or not exercises_data.get("exercises"):
        st.error("Failed to load exercises")
        return
    
    exercises = exercises_data.get("exercises", [])
    
    for exercise in exercises:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{exercise.get('name', 'Exercise')}**")
        with col2:
            st.markdown(f"⏱️ {exercise.get('duration', '5')} min")
        with col3:
            st.markdown(f"Level: {exercise.get('difficulty', 'Beginner')}")
    
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

def page_resources():
    """Resources page"""
    display_header()
    display_crisis_disclaimer()
    
    st.markdown("## Mental Health Resources")
    
    emergency = get_emergency_resources()
    if emergency and emergency.get("resources"):
        st.markdown("### 🆘 Emergency Resources (24/7)")
        resources = emergency.get("resources", {}).get("US", {})
        for resource_type, resource_info in resources.items():
            if isinstance(resource_info, dict):
                with st.container():
                    st.markdown(f'<div class="critical-box">{resource_info.get("name", resource_type)}</div>', 
                               unsafe_allow_html=True)
                    if "number" in resource_info:
                        st.markdown(f"📞 {resource_info['number']}")
                    if "text" in resource_info:
                        st.markdown(f"💬 {resource_info['text']}")
                    if "description" in resource_info:
                        st.markdown(f"ℹ️ {resource_info['description']}")
                    if "url" in resource_info:
                        st.markdown(f"🌐 [{resource_info.get('name', 'Visit')}]({resource_info['url']})")
    
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()

# Main app routing
if not check_backend():
    st.error("⚠️ Backend server is not running. Please start it with: `uvicorn backend:app --reload`")
    st.stop()

# Route to appropriate page
if st.session_state.current_page == "home":
    page_home()
elif st.session_state.current_page == "chat":
    page_chat()
elif st.session_state.current_page == "assessments":
    page_assessments()
elif st.session_state.current_page.startswith("assessment_"):
    # Extract assessment ID from page name
    assessment_id = st.session_state.current_page.replace("assessment_", "")
    page_conduct_assessment(assessment_id)
elif st.session_state.current_page == "mindfulness":
    page_mindfulness()
elif st.session_state.current_page == "resources":
    page_resources()
else:
    page_home()

# Sidebar navigation
st.sidebar.markdown("## Navigation")
pages = {
    "🏠 Home": "home",
    "💬 Chat": "chat",
    "📊 Assessments": "assessments",
    "🧘 Mindfulness": "mindfulness",
    "📚 Resources": "resources"
}

for page_name, page_key in pages.items():
    if st.sidebar.button(page_name, use_container_width=True):
        st.session_state.current_page = page_key
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About This Chatbot
✅ **Supportive Guidance** - AI-powered emotional support
✅ **Assessments** - Validated psychological tools
✅ **Crisis Detection** - Automatic safety measures
✅ **Resources** - Emergency contact information
""")

st.sidebar.markdown("""
### Safety Information
🆘 **Need help now?**
- **Call 988** (US, 24/7)
- **Text HOME to 741741**
- **Call 911** for emergencies
""")
