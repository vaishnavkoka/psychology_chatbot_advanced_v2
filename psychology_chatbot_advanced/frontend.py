"""
Psychology Chatbot Frontend - Streamlit UI
Interactive interface for psychology support and assessments
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

# Styles
st.markdown("""
    <style>
    .header-color { color: #2E86AB; font-weight: bold; }
    .support-box { background-color: #F0F8FF; padding: 15px; border-radius: 10px; }
    .assessment-box { background-color: #F0FFF4; padding: 15px; border-radius: 10px; }
    .mindfulness-box { background-color: #FFF9E6; padding: 15px; border-radius: 10px; }
    .warning-box { background-color: #FFE6E6; padding: 15px; border-radius: 10px; border-left: 4px solid #FF6B6B; }
    </style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assessment_results" not in st.session_state:
    st.session_state.assessment_results = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Helper functions
def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

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
    """Send message to chatbot"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": message, "context": context}
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error chatting with bot: {e}")
        return None

# Main interface
st.markdown('<h1 class="header-color">🧠 Psychology Support Chatbot</h1>', unsafe_allow_html=True)
st.markdown("*Your personal AI companion for mental health support, assessments, and wellbeing*")

# Check backend status
if not check_backend():
    st.error("⚠️ Backend server is not running. Please start it first.")
    st.info("Run: `python -m uvicorn backend:app --host 0.0.0.0 --port 8000 --reload`")
    st.stop()

st.success("✅ Connected to backend")

# Sidebar
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Choose an option:",
        [
            "💬 Chat Support",
            "📋 Take Assessment",
            "🧘 Mindfulness",
            "📚 Learning",
            "🆘 Emergency"
        ]
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.info(
        """
        This chatbot provides:
        - **Emotional Support**: Talk with AI for immediate support
        - **Assessments**: Screen for depression, anxiety, stress
        - **Techniques**: Learn CBT, mindfulness, coping strategies
        - **Resources**: Access mental health information
        
        ⚠️ **This is NOT a replacement for professional mental health care.**
        If you're in crisis, contact emergency services or use the Emergency tab.
        """
    )
    
    if st.button("🆘 Crisis Resources"):
        st.session_state.current_page = "emergency"

# Chat Support Page
if page == "💬 Chat Support":
    st.markdown('<h2 class="header-color">💬 Chat with Support</h2>', unsafe_allow_html=True)
    st.markdown("Talk about what's on your mind. I'm here to listen and support you.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input("What's on your mind? (Type and press Enter)")
    
    with col2:
        severity = st.select_slider("How are you feeling?", options=["😢", "😞", "😐", "🙂", "😊"], value="😐")
        severity_map = {"😢": 1, "😞": 2, "😐": 3, "🙂": 4, "😊": 5}
    
    if user_input:
        with st.spinner("Listening and preparing response..."):
            response = get_support(user_input, severity_map[severity])
        
        if response:
            st.markdown('<div class="support-box">', unsafe_allow_html=True)
            st.markdown("### 🤖 Response")
            st.write(response.get("message", ""))
            
            if response.get("follow_up"):
                st.markdown("### 💆 Recommendation")
                st.info(response["follow_up"])
            
            if response.get("resources"):
                st.markdown("### 📚 Resources")
                for resource in response["resources"]:
                    st.write(f"- {resource}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick support options
    st.markdown("---")
    st.markdown("### Quick Support Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("😰 I'm anxious"):
            with st.spinner("Providing support..."):
                response = get_support("I'm feeling anxious and worried", 2)
                if response:
                    st.info(response.get("message", ""))
    
    with col2:
        if st.button("😔 I'm sad"):
            with st.spinner("Providing support..."):
                response = get_support("I'm feeling sad and down", 1)
                if response:
                    st.info(response.get("message", ""))
    
    with col3:
        if st.button("😤 I'm stressed"):
            with st.spinner("Providing support..."):
                response = get_support("I'm feeling stressed and overwhelmed", 2)
                if response:
                    st.info(response.get("message", ""))

# Assessment Page
elif page == "📋 Take Assessment":
    st.markdown('<h2 class="header-color">📋 Psychological Assessments</h2>', unsafe_allow_html=True)
    
    assessment_data = get_assessments()
    
    if not assessment_data or not assessment_data.get("assessments"):
        st.warning("No assessments available")
    else:
        st.markdown("Take scientifically-validated assessments to understand your mental health better.")
        st.markdown('These are screening tools - not clinical diagnoses.')
        
        # Assessment selection
        assessments = assessment_data.get("assessments", [])
        assessment_names = [a["name"] for a in assessments]
        selected_name = st.selectbox("Choose an assessment:", assessment_names)
        
        selected = next((a for a in assessments if a["name"] == selected_name), None)
        
        if selected:
            with st.expander("ℹ️ About this assessment", expanded=True):
                st.write(f"**Type:** {selected['type']}")
                st.write(f"**Questions:** {selected['questions_count']}")
                st.markdown("*This is a screening tool developed by mental health professionals.*")
            
            # Assessment questions
            st.markdown("---")
            st.markdown("### Answer the following questions (0 = Not at all, 3 = Nearly every day)")
            
            responses = []
            for i, q in enumerate(selected['questions_count'] * [0], 1):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{i}. {selected['questions_count']}")
                with col2:
                    response = st.slider("", 0, 3, 0, key=f"q_{i}", label_visibility="collapsed")
                    responses.append(response)
            
            if st.button("📊 Get Results", type="primary"):
                with st.spinner("Analyzing your responses..."):
                    time.sleep(1)
                    result = conduct_assessment(selected["id"], responses)
                
                if result:
                    st.markdown('<div class="assessment-box">', unsafe_allow_html=True)
                    st.markdown("### 📊 Your Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Score", result.get("total_score", 0))
                    with col2:
                        st.metric("Assessment", selected_name.split("(")[0])
                    with col3:
                        st.metric("Status", result.get("interpretation", "Unknown"))
                    
                    st.markdown("### Interpretation")
                    st.info(result.get("interpretation", ""))
                    
                    st.markdown("### AI Analysis")
                    st.write(result.get("ai_analysis", ""))
                    
                    if result.get("recommendations"):
                        st.markdown("### Recommendations")
                        for rec in result["recommendations"]:
                            st.write(f"- {rec}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# Mindfulness Page
elif page == "🧘 Mindfulness":
    st.markdown('<h2 class="header-color">🧘 Mindfulness & Exercises</h2>', unsafe_allow_html=True)
    
    exercises_data = get_exercises()
    
    if not exercises_data or not exercises_data.get("exercises"):
        st.warning("No exercises available")
    else:
        st.markdown("Practice mindfulness and relaxation exercises to improve your wellbeing.")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            duration_filter = st.select_slider("Duration:", ["5", "10", "15", "20", "30"], value="10")
        with col2:
            difficulty = st.selectbox("Difficulty:", ["beginner", "intermediate", "advanced"])
        
        # Display exercises
        exercises = exercises_data.get("exercises", [])
        
        for exercise in exercises[:5]:  # Show first 5
            with st.expander(f"🧘 {exercise.get('name', 'Exercise')}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"Duration: {exercise.get('duration', 'N/A')}")
                with col2:
                    st.info(f"Level: {exercise.get('difficulty', 'N/A')}")
                with col3:
                    st.success(f"Benefits: {len(exercise.get('benefits', []))} listed")
                
                st.markdown("### Instructions")
                for i, step in enumerate(exercise.get("instructions", []), 1):
                    st.write(f"{i}. {step}")
                
                st.markdown("### Benefits")
                for benefit in exercise.get("benefits", []):
                    st.write(f"✓ {benefit}")
                
                if st.button(f"Start Exercise: {exercise.get('name', 'Exercise')}", key=exercise.get('id')):
                    st.balloons()
                    st.success("Great! Take your time with this exercise. No rush. 🙏")

# Learning Page
elif page == "📚 Learning":
    st.markdown('<h2 class="header-color">📚 Learn About Mental Health</h2>', unsafe_allow_html=True)
    
    st.markdown("Expand your knowledge about mental health topics and wellbeing strategies.")
    
    tabs = st.tabs(["Topics", "CBT Techniques", "Coping Strategies"])
    
    with tabs[0]:
        st.markdown("### Mental Health Topics")
        st.info("Popular topics you can learn about")
        
        topics = [
            "Depression", "Anxiety", "Stress", "Sleep Issues",
            "Self-Esteem", "Relationships", "Grief", "Emotional Intelligence"
        ]
        
        for topic in topics:
            if st.button(f"📖 {topic}"):
                st.info(f"Content about {topic} would be displayed here.")
                with st.spinner("Loading content..."):
                    time.sleep(1)
                    st.write("*This is where detailed information about the topic would appear.*")
    
    with tabs[1]:
        st.markdown("### CBT Techniques")
        st.info("Cognitive Behavioral Therapy techniques for mental wellness")
        
        techniques = [
            "Thought Challenging",
            "Cognitive Restructuring",
            "Behavioral Activation",
            "Problem-Solving",
            "Exposure Therapy"
        ]
        
        selected_technique = st.selectbox("Select a technique:", techniques)
        st.write(f"*Learn about {selected_technique}*")
    
    with tabs[2]:
        st.markdown("### Coping Strategies")
        st.info("Evidence-based strategies for managing emotions and stress")
        
        strategies = [
            "Physical Activity",
            "Creative Expression",
            "Social Connection",
            "Self-Care Routine",
            "Boundary Setting"
        ]
        
        for strategy in strategies:
            st.write(f"- {strategy}")

# Emergency Page
elif page == "🆘 Emergency":
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown('<h2 class="header-color">🆘 Emergency Resources</h2>', unsafe_allow_html=True)
    st.markdown("""
    **If you are in immediate danger or having thoughts of suicide, please reach out for help immediately.**
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🌍 International Resources")
    
    resources = {
        "🇺🇸 USA": [
            ("National Suicide Prevention Lifeline", "988", "1-988-SUICIDE (1-988-784-2433)"),
            ("Crisis Text Line", "Text HOME", "Text HOME to 741741"),
        ],
        "🇨🇦 Canada": [
            ("Canada Suicide Prevention Service", "1-833-456-4566", "Available 24/7"),
        ],
        "🇬🇧 UK": [
            ("Samaritans", "116 123", "Available 24/7"),
        ],
        "🇦🇺 Australia": [
            ("Lifeline", "13 11 14", "Available 24/7"),
        ],
    }
    
    for country, lines in resources.items():
        with st.expander(country):
            for name, shortcode, number in lines:
                st.write(f"**{name}**")
                st.write(f"- {shortcode}: {number}")
    
    st.markdown("---")
    st.markdown("### ✅ Immediate Steps")
    st.info("""
    1. Call emergency services (911 in USA)
    2. Go to nearest hospital emergency room
    3. Tell someone you trust how you're feeling
    4. Remove anything that could be used to hurt yourself
    5. Stay with a supportive person
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; margin-top: 30px;'>
    <p><small>
    This chatbot is for supportive purposes only and is NOT a replacement for professional mental health care.
    If you're experiencing a mental health crisis, please contact emergency services immediately.
    </small></p>
    <p><small>© 2026 Psychology Chatbot | Built with care for your mental wellbeing</small></p>
</div>
""", unsafe_allow_html=True)
