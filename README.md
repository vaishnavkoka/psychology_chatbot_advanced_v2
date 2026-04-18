# 🧠 Psychology Chatbot - Multi-Agent Mental Health Support

**Intelligent mental health support powered by multi-agent AI orchestration using LangGraph**

## 🎯 Quick Start

### Prerequisites
- Python 3.10+
- GROQ API Key (for LLM access)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY="your-groq-api-key"
```

### Running the Application

**Start Backend (Port 8000):**
```bash
cd /home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced
python3 -m uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

**Start Frontend (Port 8501):**
```bash
streamlit run frontend_premium.py --logger.level=warning
```

Access the application at: **http://localhost:8501**

---

## 🏗️ Architecture

### Multi-Agent System

The system uses **LangGraph orchestrator** to coordinate specialized agents:

| Agent | Purpose | Triggered By |
|-------|---------|--------------|
| **Query Router** | Analyzes user intent and selects appropriate agents | All inputs |
| **Crisis Detection** | 🚨 Priority - Detects high-risk keywords | Emotional distress keywords |
| **Therapy Support** | Provides coping strategies and emotional support | Mental health concerns |
| **Assessment Agent** | Conducts PHQ-9, GAD-7, PSQI evaluations | Assessment requests |
| **RAG Agent** | Retrieves psychology knowledge and resources | Knowledge queries |

### System Workflow

```
User Input → Query Routing → Crisis Detection?
  ├─ NO → Select therapy/assessment/rag agents
  └─ YES → Trigger emergency response
  
→ Agent Execution → Response Synthesis → LLM Generation → User Output
```

---

## 💻 Features

### Core Capabilities
✅ **Real-time Chat** - Contextual responses powered by Groq LLM (llama-3.3-70b-versatile)  
✅ **Crisis Detection** - Immediate emergency response with hotlines  
✅ **Psychological Assessments** - PHQ-9, GAD-7, PSQI, Rosenberg SES, PCL-5  
✅ **Spell Checking** - Automatic correction of typos (transparent to user)  
✅ **Scrollable Chat UI** - Messages stay in box, no page scrolling  
✅ **Sample Quick Buttons** - Pre-built inputs showing agent routing  

### Assessment Types
- **PHQ-9**: Depression Screening
- **GAD-7**: Anxiety Screening  
- **PSQI**: Sleep Quality
- **Rosenberg SES**: Self-Esteem
- **PCL-5**: PTSD Screening

---

## 📁 Project Structure

```
psychology_chatbot_advanced/
├── backend.py                          # FastAPI backend with orchestration
├── frontend_premium.py                 # Streamlit UI with chat & assessments
├── agents/
│   ├── langgraph_orchestrator_psychology.py   # Multi-agent coordinator
│   ├── assessment_agent.py             # Assessment execution
│   ├── therapeutic_support_agent.py    # Therapy strategies
│   └── rag_agent.py                    # Knowledge retrieval
├── safety/
│   └── crisis_detection.py             # Crisis keyword detection
├── config/
│   └── settings.py                     # API keys & configurations
├── assessment_routes.py                # Assessment API endpoints
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 🔌 API Endpoints

### Chat
**POST** `/chat`
```json
{
  "message": "I'm feeling depressed",
  "context": {}
}
```
Response: Contextual response with crisis detection

### Assessments
**GET** `/api/assessments/available` - List available assessments  
**POST** `/api/assessments/start` - Start assessment  
**POST** `/api/assessments/score` - Score assessment responses  

### Health Check
**GET** `/health` - Backend status

---

## 🧪 Testing

Run comprehensive test suites:

```bash
# Core functionality tests (61 tests)
python3 test_comprehensive.py

# Edge case tests (32 tests)
python3 test_edge_cases.py

# Quick integration test
python3 system_integration_test.py
```

**Test Status**: ✅ All tests passing (100% success rate)

---

## 🎮 Sample Inputs & Agent Routing

Click any sample button to see which agents are triggered:

| Input | Agents Triggered | Purpose |
|-------|------------------|---------|
| "I'm feeling depressed" | 🔗 Crisis Detection → Therapy Support | Emotional distress |
| "Help with anxiety" | 🔗 Query Router → Therapy Support → RAG | Anxiety management |
| "I can't sleep well" | 🔗 Query Router → RAG → Therapy Support | Sleep improvement |
| "Stress at work" | 🔗 Query Router → Therapy Support | Occupational stress |
| "I'm having suicidal thoughts" | 🚨 Crisis Detection (PRIORITY) | Emergency response |
| "Can I take PHQ-9?" | 🔗 Query Router → Assessment | Psychological screening |

---

## ⚙️ Configuration

### Environment Variables
```bash
GROQ_API_KEY=your-api-key          # Required for LLM
BACKEND_PORT=8000                  # Backend port (default)
```

### Settings (config/settings.py)
- LLM Model: `llama-3.3-70b-versatile`
- Temperature: 0.7 (contextual but stable)
- Timeout: 30 seconds
- Max Tokens: 2000

---

## 🔐 Safety Features

✅ **Crisis Detection** - Keywords: suicide, self-harm, hopeless, emergency  
✅ **Immediate Resources** - 988 Lifeline, Crisis Text Line  
✅ **Professional Recommendation** - Suggested professional contact  
✅ **Spell Checking** - Clean user messages automatically  

---

## 📊 Frontend Features

### Chat Interface
- **Scrollable Message Box** (550px height)
- **Sample Quick Buttons** with agent routing display
- **Real-time Responses** with typing indicator
- **Crisis Alerts** with emergency resources
- **Assessment Integration** with scoring

### Tabs & Sections
1. **Chat** - Main conversation interface
2. **Assessments** - Psychological assessment tools
3. **Resources** - Mental health resources & hotlines
4. **Dashboard** - User insights & progress tracking

---

## 🚀 Performance

- **Response Time**: < 3 seconds (Groq LLM)
- **Chat Box**: 550px scrollable, no page scroll
- **Input Method**: Enter key or Send button
- **Sample Inputs**: Auto-fill with st.rerun()

---

## ✨ Recent Updates

### v2.0 - Multi-Agent Orchestration
✅ LangGraph-based agent coordination  
✅ Crisis detection with priority routing  
✅ LLM-based contextual responses  
✅ Proper message rendering with chat components  
✅ Scrollable chat interface  
✅ Sample inputs with agent educational display  

---

## 📝 Development

### Adding New Agents
1. Create agent class in `agents/` directory
2. Integrate with `langgraph_orchestrator_psychology.py`
3. Add routing logic in `_determine_required_agents()`
4. Test with `test_comprehensive.py`

### Adding New Assessments
1. Define assessment in backend
2. Add scoring logic
3. Create UI in `render_assessment_interface()`
4. Add to sample inputs

---

## 🐛 Troubleshooting

### Backend won't start
- Check GROQ_API_KEY is set
- Verify port 8000 is free
- Check Python 3.10+ installed

### Frontend shows "Cannot connect to server"
- Ensure backend is running on port 8000
- Check `/health` endpoint

### Messages showing raw HTML
- Already fixed in v2.0
- Using st.chat_message() for rendering

### Session state errors
- Clear browser cache
- Close and reopen Streamlit

---

## 📞 Support Resources

- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **International Crisis Centers**: https://www.iasp.info/resources/Crisis_Centres/
- **Emergency Services**: 911

---

## 📄 License

This project is part of the RE4BDD research initiative.

---

**Last Updated**: April 15, 2026 | **Status**: ✅ Production Ready
