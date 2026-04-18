"""
Demo Mode - Psychology Chatbot
Standalone demo that doesn't require backend API
Useful for testing, training, and demonstrations
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict
import json

st.set_page_config(
    page_title="🧠 Psychology Chatbot - Demo Mode",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }
    .header { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 2rem; 
              border-radius: 12px; color: white; margin-bottom: 2rem; }
    .demo-card { background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; 
                 box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-top: 4px solid #6366f1; }
    .assessment-result { background: linear-gradient(135deg, #e0e7ff 0%, #faf5ff 100%); 
                         padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid #6366f1; }
</style>
""", unsafe_allow_html=True)

# Session state
if "demo_assessments" not in st.session_state:
    st.session_state.demo_assessments = []

# Sample assessment data
SAMPLE_ASSESSMENTS = {
    "phq9": {
        "name": "PHQ-9: Depression Screening",
        "sample_response": [1, 2, 1, 2, 3, 1, 2, 1, 0],
        "score": 16,
        "max_score": 27,
        "interpretation": "Moderate depression. Consider therapy.",
        "severity": "moderate"
    },
    "gad7": {
        "name": "GAD-7: Anxiety Screening",
        "sample_response": [2, 2, 2, 2, 1, 2, 1],
        "score": 12,
        "max_score": 21,
        "interpretation": "Moderate anxiety. Self-help and professional support recommended.",
        "severity": "moderate"
    },
    "psqi": {
        "name": "PSQI: Sleep Quality Index",
        "sample_response": [1, 2, 1, 2, 3, 1, 2],
        "score": 12,
        "max_score": 21,
        "interpretation": "Poor sleep quality. Consider sleep studies.",
        "severity": "poor"
    },
    "rosenberg_ses": {
        "name": "Rosenberg Self-Esteem Scale",
        "sample_response": [2, 2, 1, 2, 1, 2, 2, 2, 2, 1],
        "score": 17,
        "max_score": 40,
        "interpretation": "Moderate self-esteem. Therapy may help.",
        "severity": "moderate"
    },
    "pcl5": {
        "name": "PCL-5: PTSD Checklist",
        "sample_response": [2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 3, 1, 2, 1, 2, 1, 2, 2, 1],
        "score": 31,
        "max_score": 80,
        "interpretation": "Moderate PTSD symptoms. Professional evaluation recommended.",
        "severity": "moderate"
    }
}

SAMPLE_CONVERSATIONS = [
    ("I've been feeling really overwhelmed with work lately", 
     "I understand work stress can be overwhelming. Let's talk about what's making it difficult. What specific aspects are causing the most stress?"),
    ("I can't sleep at night, my mind keeps racing", 
     "Racing thoughts at night are often related to anxiety or hyperarousal. Here are some techniques that might help: 1) Box breathing (4-4-4-4), 2) Progressive muscle relaxation, 3) Limiting screen 1 hour before bed"),
    ("I'm feeling hopeless about the future",
     "🚨 I notice you mentioned feeling hopeless. I want to make sure you're safe. Please reach out to 988 (call/text) for immediate support. A counselor can help you work through these feelings with professional support."),
]

st.markdown("""
<div class="header" style="text-align: center;">
    <h1>🧠 Psychology Chatbot - Demo Mode</h1>
    <p>Interactive demonstration of multi-agent mental health support system</p>
    <p style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 8px; display: inline-block; font-size: 0.9rem;">
        ⚡ No backend required - Works standalone
    </p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Assessments",
    "💬 Sample Chat",
    "📊 Demo Results",
    "🎯 Features",
    "📚 Documentation"
])

# ============================================================
# TAB 1: ASSESSMENTS
# ============================================================

with tab1:
    st.header("📋 Sample Assessments")
    st.markdown("Browse and run sample assessments to see how the system works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Available Assessments")
        selected = st.radio(
            "Select an assessment:",
            options=list(SAMPLE_ASSESSMENTS.keys()),
            format_func=lambda x: SAMPLE_ASSESSMENTS[x]["name"],
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("### Preview")
        assessment = SAMPLE_ASSESSMENTS[selected]
        st.markdown(f"""
        <div class="demo-card">
            <h3>{assessment['name']}</h3>
            <p><strong>Questions:</strong> {len(assessment['sample_response'])}</p>
            <p><strong>Score Range:</strong> 0-{assessment['max_score']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("Run Sample Assessment", use_container_width=True, key="run_assessment"):
        assessment = SAMPLE_ASSESSMENTS[selected]
        st.markdown(f"""
        <div class="assessment-result">
            <h3>✅ Results for {assessment['name']}</h3>
            <p><strong>Score:</strong> {assessment['score']}/{assessment['max_score']} ({assessment['score']/assessment['max_score']*100:.1f}%)</p>
            <p><strong>Severity:</strong> <span style="background: #fed7aa; padding: 0.25rem 0.75rem; border-radius: 12px; font-weight: 600;">{assessment['severity'].title()}</span></p>
            <p><strong>Interpretation:</strong> {assessment['interpretation']}</p>
            <hr>
            <p><strong>Recommendations:</strong></p>
            <ul>
                <li>Professional consultation for comprehensive evaluation</li>
                <li>Self-care practices tailored to your needs</li>
                <li>Regular monitoring and follow-up assessments</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.demo_assessments.append({
            "assessment": assessment['name'],
            "score": assessment['score'],
            "max_score": assessment['max_score'],
            "severity": assessment['severity'],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Report generation options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Export PDF"):
                st.info("PDF export functionality would generate formatted report")
        with col2:
            if st.button("📊 Export JSON"):
                st.json(assessment)
        with col3:
            if st.button("📋 Export CSV"):
                st.info("CSV export would create spreadsheet-friendly format")

# ============================================================
# TAB 2: SAMPLE CHAT
# ============================================================

with tab2:
    st.header("💬 Sample Conversations")
    st.markdown("See how the multi-agent system responds to different scenarios")
    
    st.markdown("### Conversation Examples")
    
    for i, (user_msg, assistant_msg) in enumerate(SAMPLE_CONVERSATIONS):
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if i == 2:
                    st.markdown("🚨")
                else:
                    st.markdown("👤")
            
            with col2:
                st.markdown(f"""
                <div style="background: #e0e7ff; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #6366f1;">
                    <strong>User:</strong> {user_msg}
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if i == 2:
                    st.markdown("🤖❌")
                else:
                    st.markdown("🤖")
            
            with col2:
                msg_style = "background: #fee2e2; border-left: 4px solid #ef4444;" if i == 2 else "background: #f0fdf4; border-left: 4px solid #10b981;"
                st.markdown(f"""
                <div style="{msg_style} padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    <strong>Assistant:</strong> {assistant_msg}
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# TAB 3: DEMO RESULTS
# ============================================================

with tab3:
    st.header("📊 Demo Results Summary")
    
    if st.session_state.demo_assessments:
        df = pd.DataFrame(st.session_state.demo_assessments)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assessments Run", len(df))
        with col2:
            st.metric("Average Score", f"{df['score'].mean():.1f}")
        with col3:
            st.metric("Most Common Severity", df['severity'].mode()[0].title() if len(df['severity'].mode()) > 0 else "N/A")
        
        st.markdown("### Assessment History")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if st.button("Clear History"):
            st.session_state.demo_assessments = []
            st.rerun()
    else:
        st.info("Run some assessments above to see results here")

# ============================================================
# TAB 4: FEATURES  
# ============================================================

with tab4:
    st.header("🎯 System Features")
    
    features = {
        "🤖 Multi-Agent Architecture": [
            "AssessmentAgent - Validates & administers 5 psychological assessments",
            "CrisisDetectionAgent - Monitors for mental health crises with resource routing",
            "TherapeuticSupportAgent - Provides evidence-based therapeutic guidance",
            "InsightsAgent - Analyzes patterns and delivers psychoeducation",
            "QueryRouterAgent - Intelligently routes queries to appropriate agents",
            "RAGAgent - Semantic search over psychology knowledge base"
        ],
        "📊 Validated Assessments": [
            "PHQ-9 - 9-question depression screening",
            "GAD-7 - 7-question anxiety screening",
            "PSQI - Sleep quality assessment",
            "Rosenberg Self-Esteem Scale",
            "PCL-5 - PTSD symptom checklist"
        ],
        "🔒 Safety & Security": [
            "Real-time crisis detection",
            "Emergency resource routing (988, Crisis Text Line, SAMHSA)",
            "SQL injection prevention",
            "XSS attack prevention",
            "Input sanitization"
        ],
        "📈 Reporting": [
            "PDF reports with professional formatting",
            "JSON structured export",
            "CSV spreadsheet-compatible",
            "Batch report generation",
            "Progress tracking dashboards"
        ],
        "🌐 API Integration": [
            "GROQ - Primary LLM provider",
            "HuggingFace - Embeddings + alternative models",
            "Tavily - Web research (1000/month free)",
            "Serper - Search API (2500/month free)",
            "Cohere - Backup LLM + reranking"
        ],
        "💾 Data Management": [
            "100+ KB psychology knowledge base",
            "FAISS vector store for semantic search",
            "SQLite/PostgreSQL database",
            "15 diverse data files (CSV, TXT, JSON)",
            "Vector embeddings (384-dimensional)"
        ]
    }
    
    for category, items in features.items():
        with st.expander(f"**{category}**", expanded=False):
            for item in items:
                st.markdown(f"- {item}")

# ============================================================
# TAB 5: DOCUMENTATION
# ============================================================

with tab5:
    st.header("📚 Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Quick Start
        
        **Running the Full System:**
        ```bash
        # Terminal 1: Backend
        uvicorn backend:app --reload
        
        # Terminal 2: Frontend
        streamlit run frontend_premium.py
        ```
        
        **Testing Individual Components:**
        ```bash
        # Run integration tests
        python system_integration_test.py
        
        # Run edge case tests
        pytest tests/test_edge_cases.py
        ```
        """)
    
    with col2:
        st.markdown("""
        ### API Endpoints
        
        **Assessment Endpoints:**
        - `POST /api/assessments/start`
        - `POST /api/assessments/score`
        - `GET /api/assessments/available`
        
        **Reports:**
        - `POST /api/reports/generate`
        - `POST /api/reports/batch-generate`
        
        **Chat:**
        - `POST /chat`
        
        **Health:**
        - `GET /health`
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ### Key Files
    
    | File | Purpose |
    |------|---------|
    | `backend.py` | FastAPI application server |
    | `assessment_routes.py` | Assessment API endpoints |
    | `report_routes.py` | Report generation endpoints |
    | `agents/` | 6 specialized agent implementations |
    | `config/settings.py` | Multi-API configuration |
    | `src/database_schema.py` | SQLAlchemy ORM models |
    | `QUICK_START.sh` | Automated setup script |
    
    ### Resources
    
    - **Emergency Support:** 988 (call/text)
    - **Crisis Text:** Text HOME to 741741
    - **SAMHSA:** 1-800-662-4357
    - **GitHub:** https://github.com/vaishnavkoka/psychology-chatbot
    """)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <p><strong>Psychology Chatbot Pro v2.0</strong></p>
    <p>Multi-agent AI system for mental health support | Built with FastAPI, Streamlit, and LangGraph</p>
    <p style="font-size: 0.9rem;">
        ℹ️ This is a demo mode. For full functionality with API integration, run the complete system.
    </p>
</div>
""", unsafe_allow_html=True)
