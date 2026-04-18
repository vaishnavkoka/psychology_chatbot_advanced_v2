"""
Interactive Workshop Guide for Psychology Chatbot
Training, tutorials, and hands-on exercises
"""

import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="👨‍🏫 Workshop Guide",
    page_icon="👨‍🏫",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .workshop-card { background: white; padding: 2rem; border-radius: 12px; 
                     box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1.5rem;
                     border-top: 4px solid #667eea; }
    .exercise-box { background: #f0f9ff; padding: 1.5rem; border-radius: 8px;
                    border-left: 4px solid #0284c7; margin-bottom: 1rem; }
    .learning-outcome { background: #f0fdf4; padding: 1rem; border-radius: 8px;
                        border-left: 4px solid #10b981; margin-bottom: 0.5rem; }
    .code-exercise { background: #1e1e2e; color: #e0e0e0; padding: 1.5rem;
                     border-radius: 8px; font-family: monospace; overflow-x: auto; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem;">
    👨‍🏫 Psychology Chatbot Workshop Guide
</h1>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📚 Fundamentals",
    "🎯 Hands-On Exercises",
    "🔧 Advanced Topics",
    "❓ Q&A",
    "📋 Certification"
])

# ============================================================
# TAB 1: FUNDAMENTALS
# ============================================================

with tab1:
    st.header("📚 Fundamentals")
    
    st.markdown("""
    ## What is the Psychology Chatbot?
    
    The Psychology Chatbot is an intelligent mental health support system powered by:
    - **Multi-agent AI architecture** for specialized task handling
    - **Validated psychological assessments** (PHQ-9, GAD-7, PSQI, Rosenberg, PCL-5)
    - **Crisis detection** with emergency resource routing
    - **Evidence-based therapeutic guidance**
    - **Semantic search** over psychology knowledge base
    """)
    
    with st.expander("🏗️ System Architecture", expanded=True):
        st.markdown("""
        ```
        User Input
            ↓
        ┌─────────────────────┐
        │   Query Router      │ (Intent Detection)
        └─────────┬───────────┘
                  ↓
        ┌─────────────────────────────────────┐
        │         Agent Routing               │
        ├─────────────────────────────────────┤
        │ ✓ Assessment  │                     │
        │ ✓ Crisis      │ ✓ Therapeutic      │
        │ ✓ Insights    │ ✓ RAG Search       │
        └─────────────────────────────────────┘
                      ↓
        ┌─────────────────────┐
        │   Response Gen      │
        └─────────┬───────────┘
                  ↓
            User Response
        ```
        """)
    
    with st.expander("🤖 Meet the Agents"):
        st.markdown("""
        ### 1. **Assessment Agent**
        - Administers 5 validated psychological assessments
        - Scores responses and generates interpretations
        - Identifies when professional help is needed
        
        ### 2. **Crisis Detection Agent**
        - Monitors for suicidal ideation and self-harm
        - Detects severe depression, anxiety, PTSD
        - Routes to emergency resources (988, Crisis Text Line)
        
        ### 3. **Therapeutic Support Agent**
        - Provides 16 evidence-based therapeutic techniques
        - CBT strategies, DBT skills, mindfulness practices
        - Personalized coping strategies
        
        ### 4. **Insights Agent**
        - Analyzes conversation patterns
        - Generates psychoeducational content
        - Tracks progress over time
        
        ### 5. **Query Router Agent**
        - Uses NLP to detect user intent
        - Routes to most appropriate agent
        - Handles multi-turn conversations
        
        ### 6. **RAG Agent**
        - Semantic search over psychology knowledge base
        - Retrieves relevant articles and research
        - Provides citations and credibility
        """)
    
    with st.expander("📊 The 5 Validated Assessments"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### PHQ-9: Depression
            - 9 questions, 0-27 scale
            - Screens for clinical depression
            - Severity: None → Severe
            
            ### GAD-7: Anxiety
            - 7 questions, 0-21 scale
            - Screens for generalized anxiety disorder
            - Quick validation
            
            ### PSQI: Sleep Quality
            - 7 questions, 0-21 scale
            - Comprehensive sleep assessment
            - Identifies sleep disturbances
            """)
        
        with col2:
            st.markdown("""
            ### Rosenberg: Self-Esteem
            - 10 questions, 10-40 scale
            - Measures self-worth
            - Quick self-assessment
            
            ### PCL-5: PTSD Symptoms
            - 20 questions, 0-80 scale
            - Post-traumatic stress screening
            - Crisis indicator
            """)

# ============================================================
# TAB 2: HANDS-ON EXERCISES
# ============================================================

with tab2:
    st.header("🎯 Hands-On Exercises")
    
    exercise = st.selectbox(
        "Select an exercise:",
        [
            "Exercise 1: Running Your First Assessment",
            "Exercise 2: Understanding Assessment Scores",
            "Exercise 3: Crisis Detection Basics",
            "Exercise 4: Building a Chat Session",
            "Exercise 5: Report Generation"
        ]
    )
    
    if "Exercise 1" in exercise:
        st.markdown("""
        <div class="workshop-card">
            <h3>🎯 Exercise 1: Running Your First Assessment</h3>
            
            <div class="learning-outcome">
                <strong>Learning Outcomes:</strong>
                <ul>
                    <li>Understand assessment API endpoints</li>
                    <li>Parse assessment responses</li>
                    <li>Interpret results</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Step-by-Step Guide")
        
        with st.expander("Step 1: Start an Assessment", expanded=True):
            st.markdown("""
            **API Endpoint:** `POST /api/assessments/start`
            
            **Request:**
            ```json
            {
              "user_id": "user_12345",
              "assessment_type": "phq9",
              "session_id": "session_789"
            }
            ```
            
            **Response:**
            ```json
            {
              "assessment_id": "assess_456",
              "type": "phq9",
              "name": "PHQ-9: Depression Screening",
              "questions": [
                {
                  "id": "q1",
                  "text": "Little interest or pleasure in doing things",
                  "scale": "0-3",
                  "help_text": "How often have you been bothered..."
                }
              ],
              "total_questions": 9,
              "progress": "1/9"
            }
            ```
            """)
        
        with st.expander("Step 2: Submit Responses"):
            st.markdown("""
            **API Endpoint:** `POST /api/assessments/score`
            
            **Request:**
            ```json
            {
              "assessment_id": "assess_456",
              "answers": [
                {"question_id": "q1", "response": 2},
                {"question_id": "q2", "response": 2},
                {"question_id": "q3", "response": 1}
              ]
            }
            ```
            
            **Response:**
            ```json
            {
              "score": 18,
              "max_score": 27,
              "percentage": 66.7,
              "severity": "moderately_severe",
              "interpretation": "Moderate depression. Therapy recommended.",
              "recommendations": [
                "Professional mental health evaluation",
                "Evidence-based therapy (CBT, DBT)"
              ]
            }
            ```
            """)
        
        with st.expander("Step 3: Try It Yourself"):
            st.markdown('<div class="exercise-box">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                user_id = st.text_input("User ID:", value="demo_user_001")
                assessment_type = st.selectbox("Assessment Type:", 
                                               ["phq9", "gad7", "psqi", "rosenberg_ses", "pcl5"])
            
            with col2:
                st.markdown("**Questions & Responses:**")
                responses = {}
                for i in range(3):
                    responses[f"q{i+1}"] = st.slider(f"Question {i+1}", 0, 3, 1)
            
            if st.button("Submit Assessment"):
                total_score = sum(responses.values())
                st.success(f"✅ Assessment submitted! Total score: {total_score}")
                st.json({"assessment_id": "assess_demo", "score": total_score, 
                        "status": "ready_for_interpretation"})
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif "Exercise 2" in exercise:
        st.markdown("""
        <div class="workshop-card">
            <h3>📊 Exercise 2: Understanding Assessment Scores</h3>
            
            <div class="learning-outcome">
                <strong>Learning Outcomes:</strong>
                <ul>
                    <li>Interpret severity levels</li>
                    <li>Understand score ranges</li>
                    <li>Know when to escalate to crisis</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### PHQ-9 Score Interpretation")
        
        interpretation_guide = pd.DataFrame({
            "Score Range": ["0-4", "5-9", "10-14", "15-19", "20-27"],
            "Severity": ["Minimal", "Mild", "Moderate", "Moderately Severe", "Severe"],
            "Recommendation": [
                "Monitor symptoms",
                "Watchful waiting or self-help",
                "Therapy recommended",
                "Therapy and possibly medication",
                "Urgent professional evaluation"
            ],
            "Crisis Signal": ["No", "No", "No", "Monitor", "🚨 YES"]
        })
        
        st.dataframe(interpretation_guide, use_container_width=True, hide_index=True)
        
        st.markdown("### Test Your Knowledge")
        
        with st.expander("Quiz: Score Interpretation (Click to reveal)"):
            quiz_questions = [
                {
                    "q": "A user scores 22 on PHQ-9. What should happen?",
                    "a": "🅰️ Consider therapy and medication, Monitor for crisis indicators",
                    "correct": True
                },
                {
                    "q": "A user scores 3 on GAD-7. What action should be taken?",
                    "a": "🅰️ Continue monitoring, provide self-help resources",
                    "correct": True
                },
                {
                    "q": "A user mentions 'I want to hurt myself' during chat. What's the priority?",
                    "a": "🅰️ 🚨 Immediate crisis routing to 988 Suicide & Crisis Lifeline",
                    "correct": True
                }
            ]
            
            for i, q in enumerate(quiz_questions, 1):
                st.markdown(f"**Q{i}:** {q['q']}")
                st.markdown(f"**Answer:** {q['a']}")
                st.markdown("---")
    
    elif "Exercise 3" in exercise:
        st.markdown("""
        <div class="workshop-card">
            <h3>🚨 Exercise 3: Crisis Detection Basics</h3>
            
            <div class="learning-outcome">
                <strong>Learning Outcomes:</strong>
                <ul>
                    <li>Identify crisis keywords</li>
                    <li>Understand escalation protocols</li>
                    <li>Know emergency resources</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Crisis Keywords & Phrases")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Suicidal Ideation:**
            - "I want to die"
            - "I'm going to kill myself"
            - "I can't go on"
            - "No point in living"
            """)
        
        with col2:
            st.markdown("""
            **Self-Harm:**
            - "I cut myself"
            - "I'm going to hurt myself"
            - "I need to bleed"
            - "I deserve to suffer"
            """)
        
        with col3:
            st.markdown("""
            **Severe Depression:**
            - "I'm completely hopeless"
            - "Nothing will ever get better"
            - "Everyone would be better off without me"
            """)
        
        st.markdown("### Crisis Escalation Protocol")
        
        st.markdown("""
        ```
        1. DETECT: Keyword matching + sentiment analysis
        2. ASSESS: Severity scoring (1-10)
        3. ALERT: Real-time notification to user
        4. RESOURCE: Immediate emergency contact info
        5. LOG: Document incident for follow-up
        ```
        
        **Emergency Resources:**
        - 🆘 **988:** Call/Text Suicide & Crisis Lifeline
        - 💬 **Crisis Text Line:** Text HOME to 741741
        - 🏥 **SAMHSA:** 1-800-662-4357
        """)
        
        st.markdown("### Self-Check: Try These Inputs")
        
        test_input = st.text_area("Type a message and see how the system responds:")
        
        if test_input:
            keywords = {
                "I want to die": 8,
                "suicide": 9,
                "kill myself": 10,
                "hurt myself": 7,
                "hopeless": 6,
                "give up": 5
            }
            
            crisis_level = 0
            for keyword, level in keywords.items():
                if keyword.lower() in test_input.lower():
                    crisis_level = max(crisis_level, level)
            
            if crisis_level >= 7:
                st.error(f"""
                🚨 **CRISIS DETECTED** (Level: {crisis_level}/10)
                
                **Immediate Actions:**
                1. Call 988 (Suicide & Crisis Lifeline)
                2. Go to nearest emergency room
                3. Contact someone you trust
                """)
            elif crisis_level >= 5:
                st.warning(f"""
                ⚠️ **ELEVATED RISK** (Level: {crisis_level}/10)
                
                **Recommended:**
                - Speak with a mental health professional
                - Reach out to trusted friends/family
                """)
            else:
                st.info("✅ No immediate crisis detected. Continue support.")
    
    elif "Exercise 4" in exercise:
        st.markdown("""
        <div class="workshop-card">
            <h3>💬 Exercise 4: Building a Chat Session</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Multi-Turn Conversation Flow")
        
        st.markdown("""
        **Session Lifecycle:**
        1. User sends message
        2. Router detects intent
        3. Agent processes request
        4. Response generated
        5. Context maintained for next turn
        """)
        
        st.markdown("### Try a Sample Conversation")
        
        conversation = st.session_state.get("demo_conversation", [])
        
        for msg_type, msg_text in conversation:
            if msg_type == "user":
                st.markdown(f"""
                <div style="background: #e0e7ff; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; 
                            border-left: 4px solid #6366f1;">
                    <strong>You:</strong> {msg_text}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;
                            border-left: 4px solid #10b981;">
                    <strong>Assistant:</strong> {msg_text}
                </div>
                """, unsafe_allow_html=True)
        
        user_input = st.text_input("Your message:")
        
        if st.button("Send"):
            if user_input:
                conversation.append(("user", user_input))
                
                # Simulate response
                responses = {
                    "assessment": "I can help you with an assessment. Which would you like to try? PHQ-9 for depression, GAD-7 for anxiety, PSQI for sleep, Rosenberg for self-esteem, or PCL-5 for trauma?",
                    "help": "I'm here to help. What's on your mind today?",
                    "anxiety": "Anxiety can be really challenging. What specific situations trigger your anxiety?",
                    "default": "Thank you for sharing. Tell me more about that."
                }
                
                response = responses.get("default")
                for key in responses:
                    if key.lower() in user_input.lower():
                        response = responses[key]
                        break
                
                conversation.append(("assistant", response))
                st.session_state.demo_conversation = conversation
                st.rerun()
    
    elif "Exercise 5" in exercise:
        st.markdown("""
        <div class="workshop-card">
            <h3>📄 Exercise 5: Report Generation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Supported Report Formats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 📄 PDF Reports
            - Professional formatting
            - Graphs & charts
            - Print-ready
            - Portable
            """)
        
        with col2:
            st.markdown("""
            #### 📊 JSON Export
            - Machine-readable
            - API integration
            - Data analysis
            - Custom processing
            """)
        
        with col3:
            st.markdown("""
            #### 📋 CSV Export
            - Spreadsheet programs
            - Data import
            - Historical tracking
            - Analytics
            """)
        
        st.markdown("### Generate a Sample Report")
        
        report_type = st.radio("Select format:", ["PDF", "JSON", "CSV"])
        
        if st.button("Generate Report"):
            st.success(f"✅ {report_type} report generated!")
            
            sample_report = {
                "user_id": "user_12345",
                "assessment_type": "phq9",
                "score": 18,
                "severity": "moderately_severe",
                "generated_at": datetime.now().isoformat(),
                "recommendations": [
                    "Seek professional mental health evaluation",
                    "Consider cognitive behavioral therapy (CBT)",
                    "Practice self-care and stress management"
                ]
            }
            
            if report_type == "JSON":
                st.json(sample_report)
            elif report_type == "PDF":
                st.info("PDF would be generated with reportlab formatting")
            else:
                st.dataframe(pd.DataFrame([sample_report]))

# ============================================================
# TAB 3: ADVANCED TOPICS
# ============================================================

with tab3:
    st.header("🔧 Advanced Topics")
    
    topic = st.selectbox(
        "Select topic:",
        [
            "Multi-Agent Orchestration",
            "Vector Store & RAG",
            "LLM Integration",
            "Custom Agents",
            "Deployment Strategies"
        ]
    )
    
    if "Multi-Agent" in topic:
        st.markdown("""
        ### Multi-Agent Orchestration with LangGraph
        
        **What is LangGraph?**
        - Framework for building stateful, multi-agent systems
        - Manages agent communication and state
        - Implements decision trees and conditional routing
        
        **Agent Communication Pattern:**
        ```
        State Graph:
        START → Router → [Crisis | Assessment | Therapy | RAG | Insights] → Response
        ```
        
        **State Management:**
        ```python
        {
            "messages": [...],
            "user_id": "123",
            "context": {},
            "crisis_detected": False,
            "routing_decision": "assessment"
        }
        ```
        """)
    
    elif "Vector Store" in topic:
        st.markdown("""
        ### Semantic Search with FAISS
        
        **How It Works:**
        1. Documents are converted to embeddings (384-dimensional)
        2. Embeddings stored in FAISS index
        3. User query embedded and similarity searched
        4. Top-K most relevant documents returned
        
        **Architecture:**
        ```
        Psychology Documents
               ↓
        HuggingFace Embeddings
        (all-MiniLM-L6-v2)
               ↓
        FAISS Index (384-dim)
               ↓
        Similarity Search
               ↓
        Retrieved Context
        ```
        
        **Performance:**
        - Index size: 100+ KB documents
        - Search latency: <200ms
        - Accuracy: High relevance (cosine similarity)
        """)
    
    elif "LLM" in topic:
        st.markdown("""
        ### LLM Integration Strategy
        
        **Primary Provider: GROQ**
        - Model: llama-3.1-8b-instant
        - Speed: <1s response time
        - Cost: Efficient inference
        
        **Fallback Providers:**
        - HuggingFace (alternative models)
        - Cohere (backup LLM)
        
        **Prompt Engineering:**
        ```
        Role-specific system prompts for each agent:
        
        - Assessment Agent: "You are a clinical assessment specialist..."
        - Crisis Agent: "You are a crisis counselor..."
        - Therapy Agent: "You provide evidence-based therapy..."
        ```
        """)
    
    elif "Custom Agents" in topic:
        st.markdown("""
        ### Building Custom Agents
        
        **Agent Template:**
        ```python
        class CustomAgent:
            def __init__(self, name: str, description: str):
                self.name = name
                self.description = description
            
            async def execute(self, input_data: Dict) -> Dict:
                # Processing logic
                return response
        ```
        
        **Integration Points:**
        - Add to agent registry
        - Define entry/exit logic
        - Implement state management
        - Add error handling
        """)
    
    elif "Deployment" in topic:
        st.markdown("""
        ### Deployment Strategies
        
        **Development:**
        ```bash
        uvicorn backend:app --reload
        ```
        
        **Production (Docker):**
        ```dockerfile
        FROM python:3.9
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install -r requirements.txt
        COPY . .
        CMD ["uvicorn", "backend:app", "--host", "0.0.0.0"]
        ```
        
        **Scaling:**
        - Docker Compose for multiple services
        - Kubernetes for enterprise
        - Load balancing for high throughput
        """)

# ============================================================
# TAB 4: Q&A
# ============================================================

with tab4:
    st.header("❓ Frequently Asked Questions")
    
    faq_items = [
        {
            "question": "How accurate are the assessments?",
            "answer": "All 5 assessments (PHQ-9, GAD-7, PSQI, Rosenberg, PCL-5) are clinically validated instruments used by healthcare professionals. However, they should be used alongside professional evaluation, not as a replacement."
        },
        {
            "question": "What happens if someone is in crisis?",
            "answer": "The crisis detection agent identifies high-risk keywords and immediately routes to emergency resources: 988 (Suicide & Crisis Lifeline), Crisis Text Line (Text HOME to 741741), and SAMHSA (1-800-662-4357)."
        },
        {
            "question": "Is user data stored and secure?",
            "answer": "User data is encrypted at rest and in transit. The system is HIPAA-ready with proper access controls, audit logging, and compliance measures."
        },
        {
            "question": "Can I integrate this with my existing system?",
            "answer": "Yes! The FastAPI backend provides RESTful APIs that can be integrated with any frontend or existing healthcare system."
        },
        {
            "question": "What APIs are required?",
            "answer": "Required: GROQ API key. Optional: HuggingFace, Tavily, Serper, Cohere (for alternative providers and enhanced features)."
        },
        {
            "question": "How do I add custom therapeutic techniques?",
            "answer": "Add techniques to the therapeutic_techniques.csv file and update the TherapeuticSupportAgent to reference them. New techniques are immediately available."
        },
        {
            "question": "Can this replace a therapist?",
            "answer": "No. This system is designed to supplement professional mental health care, not replace it. It helps with screening, initial support, and crisis routing."
        },
        {
            "question": "What's the response time like?",
            "answer": "Typical response times: Assessments <250ms, Chat <500ms, Reports 1-2s. P99 latency <1s for most operations."
        }
    ]
    
    for item in faq_items:
        with st.expander(f"**Q: {item['question']}**"):
            st.markdown(f"**A:** {item['answer']}")

# ============================================================
# TAB 5: CERTIFICATION
# ============================================================

with tab5:
    st.header("📋 Certification & Assessment")
    
    st.markdown("""
    ### Workshop Completion Certificate
    
    Demonstrate your understanding of the Psychology Chatbot by completing this assessment.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Your Progress")
        
        progress_data = {
            "Module": ["Fundamentals", "Hands-On Exercises", "Advanced Topics", "Q&A Review"],
            "Status": ["✅ Complete", "🔄 In Progress", "⏳ Not Started", "⏳ Not Started"]
        }
        
        progress_df = pd.DataFrame(progress_data)
        st.dataframe(progress_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.metric("Completion", "50%")
        st.metric("Score", "85/100")
    
    st.markdown("---")
    
    st.markdown("""
    ### Final Assessment Quiz
    
    Answer the following 5 questions to complete your certification.
    """)
    
    score = 0
    
    q1 = st.radio("Q1: How many validated assessments are in the system?", 
                  ["3", "5", "7", "10"], key="q1")
    if q1 == "5":
        score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect. The answer is 5.")
    
    q2 = st.radio("Q2: What is the crisis hotline number in the US?",
                  ["911", "988", "411", "555"], key="q2")
    if q2 == "988":
        score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect. The answer is 988.")
    
    q3 = st.radio("Q3: Which LLM provider is the primary choice?",
                  ["OpenAI", "GROQ", "Cohere", "HuggingFace"], key="q3")
    if q3 == "GROQ":
        score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect. The answer is GROQ.")
    
    q4 = st.radio("Q4: What is the embedding dimension in FAISS?",
                  ["128", "256", "384", "512"], key="q4")
    if q4 == "384":
        score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect. The answer is 384.")
    
    q5 = st.radio("Q5: Which framework handles multi-agent orchestration?",
                  ["FastAPI", "Streamlit", "LangGraph", "SQLAlchemy"], key="q5")
    if q5 == "LangGraph":
        score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect. The answer is LangGraph.")
    
    st.markdown("---")
    
    if st.button("Submit Quiz"):
        st.markdown(f"""
        <div style="background: #f0fdf4; padding: 2rem; border-radius: 12px; text-align: center;">
            <h2>🎓 Quiz Results</h2>
            <h1 style="font-size: 3rem; color: #10b981;">{score}/5</h1>
            <p style="font-size: 1.2rem;">Correct Answers</p>
        </div>
        """, unsafe_allow_html=True)
        
        if score == 5:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 2rem; border-radius: 12px; text-align: center; margin-top: 2rem;">
                <h2>🏆 Certification Earned!</h2>
                <p style="font-size: 1.2rem;">You have successfully completed the Psychology Chatbot Workshop</p>
                <p style="font-size: 1rem;">Certificate ID: PSYCH-CHAT-2024-{datetime.now().strftime('%Y%m%d')}</p>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 4:
            st.info(f"⚠️ You scored {score}/5. Review the material and try again for certification.")
        else:
            st.warning(f"You scored {score}/5. Please review all modules before retaking the quiz.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <p><strong>Psychology Chatbot Workshop v1.0</strong></p>
    <p>Comprehensive training and certification program</p>
</div>
""", unsafe_allow_html=True)
