"""
Psychology Chatbot Backend - FastAPI Server
Provides REST API for psychology support and assessments
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager
import asyncio
import logging
import sys
import os
from datetime import datetime
import json
from spellchecker import SpellChecker

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import agents and safety
try:
    from agents.psychology_agents import (
        AssessmentAgent, SupportAgent, InsightAgent, RecommendationAgent
    )
    from agents.langgraph_orchestrator_psychology import LangGraphPsychologyOrchestrator
    from agents.rag_agent import RAGAgent
    from agents.report_generation_agent import report_agent
    from config.settings import APIKeys, PsychologyConfig
    from safety.crisis_detection import crisis_detector, RiskLevel
    from assessment_routes import router as assessment_router
except ImportError as e:
    logger.error(f"Failed to import: {e}")
    APIKeys = None
    PsychologyConfig = None
    crisis_detector = None
    RiskLevel = None
    LangGraphPsychologyOrchestrator = None
    RAGAgent = None
    AssessmentAgent = None
    SupportAgent = None
    InsightAgent = None
    RecommendationAgent = None
    assessment_router = None
    report_agent = None

# Pydantic Models
class MessageRequest(BaseModel):
    message: str
    context: Optional[Dict] = None

class AssessmentRequest(BaseModel):
    assessment_id: str
    responses: List[int]

class SupportRequest(BaseModel):
    issue: str
    severity: Optional[int] = 3  # 1-5 scale

class AssessmentResponse(BaseModel):
    assessment: str
    total_score: int
    interpretation: str
    recommendations: List[str]
    ai_analysis: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    agent: str
    timestamp: str
    follow_up: Optional[str] = None
    resources: Optional[List[str]] = None

class CrisisAnalysis(BaseModel):
    risk_level: str
    confidence: float
    triggers_detected: List[Dict]
    recommendation: str
    resources: Optional[Dict] = None
    safety_message: str
    
class SafeChatResponse(BaseModel):
    message: str
    agent: str
    timestamp: str
    crisis_detected: bool
    risk_level: str
    safety_message: Optional[str] = None
    resources: Optional[Dict] = None
    follow_up: Optional[str] = None

# Global agents
assessment_agent: Any = None
support_agent: Any = None
insight_agent: Any = None
recommendation_agent: Any = None
orchestrator: Any = None
rag_agent: Any = None

# Initialize spell checker
try:
    spell_checker = SpellChecker()
    logger.info("✅ Spell checker initialized")
except Exception as e:
    logger.warning(f"⚠️ Spell checker not available: {e}")
    spell_checker = None

def check_and_correct_message(text: str) -> Dict[str, Any]:
    """Check and correct spelling in user message"""
    try:
        if not spell_checker or not text:
            return {"original": text, "corrected": text, "corrections": {}, "has_errors": False}
        
        # Find misspelled words
        misspelled = spell_checker.unknown(text.lower().split())
        
        if not misspelled:
            return {"original": text, "corrected": text, "corrections": {}, "has_errors": False}
        
        # Get corrections
        corrections = {}
        corrected_text = text
        
        for word in misspelled:
            candidates = spell_checker.candidates(word)
            if candidates:
                best_correction = spell_checker.correction(word)
                corrections[word] = best_correction
                # Replace in original text (case-insensitive)
                corrected_text = corrected_text.replace(word, best_correction, 1)
        
        return {
            "original": text,
            "corrected": corrected_text,
            "corrections": corrections,
            "has_errors": len(corrections) > 0
        }
    except Exception as e:
        logger.warning(f"Error in spell checking: {e}")
        return {"original": text, "corrected": text, "corrections": {}, "has_errors": False}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global assessment_agent, support_agent, insight_agent, recommendation_agent, orchestrator, rag_agent
    
    # Startup - with graceful fallbacks
    logger.info("🧠 Initializing Psychology Chatbot...")
    api_key = APIKeys.GROQ_API_KEY if APIKeys else os.getenv("GROQ_API_KEY", "dummy_key")
    
    # Try to initialize agents, but don't fail if they can't be created
    if AssessmentAgent:
        try:
            assessment_agent = AssessmentAgent(api_key=api_key)
            logger.info("✅ Assessment agent initialized")
        except Exception as e:
            logger.warning(f"⚠️ Assessment agent initialization failed: {e}")
    
    if SupportAgent:
        try:
            support_agent = SupportAgent(api_key=api_key)
            logger.info("✅ Support agent initialized")
        except Exception as e:
            logger.warning(f"⚠️ Support agent initialization failed: {e}")
    
    if InsightAgent:
        try:
            insight_agent = InsightAgent(api_key=api_key)
            logger.info("✅ Insight agent initialized")
        except Exception as e:
            logger.warning(f"⚠️ Insight agent initialization failed: {e}")
    
    if RecommendationAgent:
        try:
            recommendation_agent = RecommendationAgent(api_key=api_key)
            logger.info("✅ Recommendation agent initialized")
        except Exception as e:
            logger.warning(f"⚠️ Recommendation agent initialization failed: {e}")
    
    if LangGraphPsychologyOrchestrator:
        try:
            logger.info("🚀 Initializing LangGraph Orchestrator...")
            orchestrator = LangGraphPsychologyOrchestrator()
            logger.info("✅ LangGraph Orchestrator initialized")
        except Exception as e:
            logger.warning(f"⚠️ LangGraph Orchestrator initialization failed: {e}")
    
    if RAGAgent:
        try:
            logger.info("📚 Initializing RAG Agent...")
            rag_agent = RAGAgent(groq_api_key=api_key)
            logger.info("✅ RAG Agent initialized")
        except Exception as e:
            logger.warning(f"⚠️ RAG Agent initialization failed: {e}")
    
    logger.info("✅ Backend initialization complete")
    
    yield
    
    # Shutdown
    logger.info("Psychology Chatbot shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Psychology Chatbot API",
    description="Comprehensive psychology support and assessment platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include assessment router
if assessment_router:
    app.include_router(assessment_router)
    logger.info("✅ Assessment router included")
else:
    logger.warning("⚠️ Assessment router not available")

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Psychology Chatbot",
        "version": "1.0.0",
        "agents_ready": {
            "assessment": assessment_agent is not None,
            "support": support_agent is not None,
            "insight": insight_agent is not None,
            "recommendation": recommendation_agent is not None
        }
    }

# Assessment endpoints
@app.get("/assessments")
async def get_available_assessments():
    """Get list of available assessments"""
    try:
        if assessment_agent:
            assessments = assessment_agent.get_available_assessments()
        else:
            # Fallback assessment list
            assessments = [
                {"id": "phq9", "name": "PHQ-9: Depression Screening", "questions": 9},
                {"id": "gad7", "name": "GAD-7: Anxiety Screening", "questions": 7},
                {"id": "psqi", "name": "PSQI: Sleep Quality", "questions": 7},
                {"id": "rosenberg", "name": "Rosenberg Self-Esteem", "questions": 10},
                {"id": "pcl5", "name": "PCL-5: PTSD Symptoms", "questions": 20}
            ]
        
        return {
            "success": True,
            "assessments": assessments,
            "count": len(assessments)
        }
    except Exception as e:
        logger.error(f"Error getting assessments: {e}")
        return {
            "success": False,
            "error": str(e),
            "assessments": []
        }

@app.get("/assessment/{assessment_id}")
async def get_assessment_details(assessment_id: str):
    """Get detailed assessment information"""
    if not assessment_agent:
        raise HTTPException(status_code=503, detail="Assessment agent not available")
    
    try:
        details = assessment_agent.get_assessment_details(assessment_id)
        if "error" in details:
            raise HTTPException(status_code=404, detail=details["error"])
        return {"success": True, "assessment": details}
    except Exception as e:
        logger.error(f"Error getting assessment details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assessment/conduct", response_model=AssessmentResponse)
async def conduct_assessment(request: AssessmentRequest):
    """Conduct assessment"""
    if not assessment_agent:
        raise HTTPException(status_code=503, detail="Assessment agent not available")
    
    try:
        result = assessment_agent.conduct_assessment(request.assessment_id, request.responses)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Get AI analysis
        ai_analysis = assessment_agent.analyze_score_with_ai(
            request.assessment_id,
            result["total_score"]
        )
        
        return AssessmentResponse(
            assessment=result["assessment"],
            total_score=result["total_score"],
            interpretation=result["interpretation"],
            recommendations=result["recommendations"],
            ai_analysis=ai_analysis
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error conducting assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Frontend-compatible assessment endpoints
class AssessmentStartRequest(BaseModel):
    assessment_type: str
    user_id: str = "guest"

class AssessmentScoreRequest(BaseModel):
    assessment_id: str
    responses: List[int]

@app.post("/api/assessments/start")
async def start_assessment_endpoint(request: AssessmentStartRequest):
    """Start a new assessment session"""
    try:
        # Validate assessment type
        valid_types = ["phq9", "gad7", "psqi", "rosenberg_ses", "pcl5", "rosenberg"]
        assessment_type = request.assessment_type.lower().strip()
        
        if assessment_type not in valid_types:
            return {
                "success": False,
                "error": f"Invalid assessment type: {request.assessment_type}. Valid types: {', '.join(valid_types)}",
                "assessment_id": None,
                "assessment_name": None,
                "questions": None
            }
        
        # Create assessment session
        import uuid
        assessment_id = str(uuid.uuid4())
        
        # Assessment details mapping
        assessment_details = {
            "phq9": {
                "name": "PHQ-9: Depression Screening",
                "questions": 9,
                "description": "Patient Health Questionnaire - screens for depression severity",
                "scale": "0-27 (0-4: None, 5-9: Mild, 10-14: Moderate, 15-19: Moderately Severe, 20-27: Severe)"
            },
            "gad7": {
                "name": "GAD-7: Anxiety Screening",
                "questions": 7,
                "description": "Generalized Anxiety Disorder - screens for anxiety severity",
                "scale": "0-21 (0-4: None, 5-9: Mild, 10-14: Moderate, 15-21: Severe)"
            },
            "psqi": {
                "name": "PSQI: Sleep Quality",
                "questions": 7,
                "description": "Pittsburgh Sleep Quality Index",
                "scale": "0-21 (Higher = worse sleep quality)"
            },
            "rosenberg": {
                "name": "Rosenberg Self-Esteem Scale",
                "questions": 10,
                "description": "Rosenberg Self-Esteem Scale - measures global self-worth",
                "scale": "10-40 (10-15: Low, 16-34: Average, 35-40: High)"
            },
            "rosenberg_ses": {
                "name": "Rosenberg Self-Esteem Scale",
                "questions": 10,
                "description": "Rosenberg Self-Esteem Scale - measures global self-worth",
                "scale": "10-40 (10-15: Low, 16-34: Average, 35-40: High)"
            },
            "pcl5": {
                "name": "PCL-5: PTSD Screening",
                "questions": 20,
                "description": "PTSD Checklist for DSM-5 - screens for PTSD symptoms",
                "scale": "0-80 (0-10: None, 11-20: Mild, 21-35: Moderate, 36-51: Severe, 52+: Extremely Severe)"
            }
        }
        
        details = assessment_details.get(assessment_type, {})
        
        logger.info(f"✅ Assessment session started: {assessment_id} - {assessment_type}")
        
        return {
            "success": True,
            "assessment_id": assessment_id,
            "assessment_name": details.get("name", assessment_type),
            "description": details.get("description", ""),
            "questions": details.get("questions", 0),
            "scale": details.get("scale", ""),
            "user_id": request.user_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting assessment: {e}")
        return {
            "success": False,
            "error": f"Failed to start assessment: {str(e)}",
            "assessment_id": None,
            "assessment_name": None,
            "questions": None
        }

@app.post("/api/assessments/score")
async def score_assessment_endpoint(request: AssessmentScoreRequest):
    """Score assessment responses"""
    try:
        # Validate inputs
        if not request.assessment_id or not isinstance(request.assessment_id, str):
            return {
                "success": False,
                "error": "Invalid assessment ID",
                "total_score": None,
                "severity_level": None,
                "interpretation": None,
                "max_score": None
            }
        
        if not request.responses or not isinstance(request.responses, list):
            return {
                "success": False,
                "error": "Invalid responses format",
                "total_score": None,
                "severity_level": None,
                "interpretation": None,
                "max_score": None
            }
        
        # Validate all responses are integers
        try:
            responses = [int(r) for r in request.responses]
        except (ValueError, TypeError):
            return {
                "success": False,
                "error": "All responses must be numbers",
                "total_score": None,
                "severity_level": None,
                "interpretation": None,
                "max_score": None
            }
        
        # Calculate score
        total_score = sum(responses)
        question_count = len(responses)
        
        # Determine severity based on typical assessment scales
        severity_mapping = {
            "none": (0, 4),
            "mild": (5, 9),
            "moderate": (10, 14),
            "moderately_severe": (15, 19),
            "severe": (20, float('inf'))
        }
        
        severity_level = "unknown"
        max_score = question_count * 4  # Typical 0-4 scale
        
        for level, (min_score, max_s) in severity_mapping.items():
            if min_score <= total_score <= max_s:
                severity_level = level
                break
        
        # Generate interpretation
        interpretations = {
            "none": "Your responses indicate minimal symptoms. Continue healthy practices.",
            "mild": "Your responses indicate mild symptoms. Consider lifestyle adjustments and self-care.",
            "moderate": "Your responses indicate moderate symptoms. Speaking with a professional is recommended.",
            "moderately_severe": "Your responses indicate moderately severe symptoms. Professional support is strongly recommended.",
            "severe": "Your responses indicate severe symptoms. Please reach out to a mental health professional or crisis service."
        }
        
        interpretation = interpretations.get(severity_level, "Please consult with a healthcare provider for interpretation.")
        
        logger.info(f"✅ Assessment scored: {total_score}/{max_score} - {severity_level}")
        
        return {
            "success": True,
            "assessment_id": request.assessment_id,
            "total_score": total_score,
            "max_score": max_score,
            "severity_level": severity_level,
            "interpretation": interpretation,
            "timestamp": datetime.now().isoformat(),
            "recommendations": [
                "Speak with a mental health professional",
                "Practice self-care and stress management",
                "Maintain regular sleep and exercise",
                "Connect with supportive friends and family"
            ] if severity_level in ["moderate", "moderately_severe", "severe"] else []
        }
        
    except Exception as e:
        logger.error(f"Error scoring assessment: {e}")
        return {
            "success": False,
            "error": f"Failed to score assessment: {str(e)}",
            "total_score": None,
            "severity_level": None,
            "interpretation": None,
            "max_score": None
        }

# Support endpoints
@app.post("/support", response_model=ChatResponse)
async def get_support(request: SupportRequest):
    """Get emotional support"""
    if not support_agent:
        raise HTTPException(status_code=503, detail="Support agent not available")
    
    try:
        response = support_agent.provide_support(request.issue)
        
        # Get recommended exercises
        exercise = support_agent.recommend_exercise(request.severity)
        
        return ChatResponse(
            message=response,
            agent="SupportAgent",
            timestamp=datetime.now().isoformat(),
            follow_up=f"Try this exercise: {exercise.get('name', 'Breathing Exercise')}",
            resources=["Crisis Hotline: 988", "Psychology Today Therapist Finder"]
        )
    except Exception as e:
        logger.error(f"Error providing support: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/spell-check")
async def spell_check_endpoint(request: MessageRequest):
    """Check and correct spelling in user message"""
    try:
        if not request.message:
            return {
                "original": "",
                "corrected": "",
                "corrections": {},
                "has_errors": False,
                "timestamp": datetime.now().isoformat()
            }
        
        result = check_and_correct_message(request.message)
        result["timestamp"] = datetime.now().isoformat()
        return result
        
    except Exception as e:
        logger.error(f"Spell check error: {e}")
        return {
            "original": request.message,
            "corrected": request.message,
            "corrections": {},
            "has_errors": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/chat", response_model=SafeChatResponse)
async def chat_endpoint(request: MessageRequest):
    """General chat endpoint with LangGraph orchestrator"""
    try:
        user_message = request.message.strip() if request.message else ""
        
        if not user_message:
            return SafeChatResponse(
                message="Please write something so I can help you.",
                agent="Assistant",
                timestamp=datetime.now().isoformat(),
                crisis_detected=False,
                risk_level="no_risk"
            )
        
        # Check spelling and automatically correct if needed
        spell_check_result = check_and_correct_message(user_message)
        corrected_message = spell_check_result.get("corrected", user_message)
        
        # Log if corrections were made
        if spell_check_result.get("corrections"):
            logger.info(f"📝 Spelling corrections: {spell_check_result['corrections']}")
        
        # Check if orchestrator available
        if orchestrator:
            logger.info(f"📨 Processing message through orchestrator: {corrected_message[:50]}...")
            result = await orchestrator.process_user_input(
                user_id="default",
                user_message=corrected_message,  # Use corrected message
                conversation_history=request.context or []
            )
        else:
            # Fallback response when orchestrator not available
            logger.info(f"📨 Using fallback response for: {corrected_message[:50]}...")
            result = {
                "response": "I'm here to listen and help. Can you tell me more about what you're experiencing?",
                "agent_used": "Fallback",
                "crisis_detected": False,
                "risk_level": "no_risk",
                "agents_involved": [],
                "synthesis_metadata": {}
            }
        
        # Extract results from orchestrator
        response_text = result.get("response", "I'm here to help. What's on your mind?")
        agent_used = result.get("agent_used", "Orchestrator")
        crisis_detected = result.get("crisis_detected", False)
        risk_level = result.get("risk_level", "no_risk")
        agents_involved = result.get("agents_involved", [])
        synthesis_metadata = result.get("synthesis_metadata", {})
        
        # Get resources if crisis detected
        resources = []
        if crisis_detected:
            if rag_agent:
                resources = rag_agent.retrieve_relevant_knowledge(
                    query="crisis hotline resources emergency help",
                    k=5
                )
        
        # Safety message for elevated risk
        safety_message = None
        if risk_level in ["orange_risk", "red_risk", "critical_risk"]:
            safety_message = f"I notice you might be going through something challenging. "
            safety_message += "Please reach out to: 988 Suicide & Crisis Lifeline (call or text 988)"
        
        logger.info(f"✅ Orchestrator responded: {agent_used} (crisis: {crisis_detected})")
        
        return SafeChatResponse(
            message=response_text,
            agent=agent_used,
            timestamp=datetime.now().isoformat(),
            crisis_detected=crisis_detected,
            risk_level=risk_level,
            safety_message=safety_message,
            resources=resources if resources else None,
            metadata={
                "agents_involved": agents_involved,
                "synthesis": synthesis_metadata
            }
        )
    except Exception as e:
        logger.error(f"Error in orchestrator chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Recommendation endpoints
@app.get("/recommendations/{issue}")
async def get_recommendations(issue: str):
    """Get recommendations for issue"""
    if not recommendation_agent:
        raise HTTPException(status_code=503, detail="Recommendation agent not available")
    
    try:
        technique = recommendation_agent.recommend_cbt_technique(issue)
        return {
            "success": True,
            "issue": issue,
            "technique": technique
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mental health info endpoints
@app.get("/topics")
async def get_topics():
    """Get available mental health topics"""
    try:
        with open("data/psychology_db/mental_health_topics.json", "r") as f:
            data = json.load(f)
            topics = [{
                "id": t["id"],
                "topic": t["topic"],
                "preview": f"{len(t['symptoms'])} symptoms covered"
            } for t in data.get("mental_health_topics", [])]
            return {"success": True, "topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/topic/{topic_name}")
async def get_topic_details(topic_name: str):
    """Get detailed information about a topic"""
    if not insight_agent:
        raise HTTPException(status_code=503, detail="Insight agent not available")
    
    try:
        topic_info = insight_agent.get_topic_info(topic_name)
        if not topic_info:
            raise HTTPException(status_code=404, detail=f"Topic '{topic_name}' not found")
        
        return {"success": True, "topic": topic_info}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mindfulness endpoints
@app.get("/exercises")
async def get_exercises():
    """Get available mindfulness exercises"""
    try:
        with open("data/psychology_db/mindfulness_exercises.json", "r") as f:
            data = json.load(f)
            exercises = [{
                "id": e["id"],
                "name": e["name"],
                "duration": e["duration"],
                "difficulty": e["difficulty"]
            } for e in data.get("mindfulness_exercises", [])]
            return {
                "success": True,
                "exercises": exercises,
                "count": len(exercises)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exercise/{exercise_id}")
async def get_exercise_details(exercise_id: str):
    """Get mindfulness exercise details"""
    try:
        with open("data/psychology_db/mindfulness_exercises.json", "r") as f:
            data = json.load(f)
            exercise = next(
                (e for e in data.get("mindfulness_exercises", []) if e["id"] == exercise_id),
                None
            )
            if not exercise:
                raise HTTPException(status_code=404, detail="Exercise not found")
            
            return {"success": True, "exercise": exercise}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Crisis Detection endpoints
@app.post("/safety/detect-crisis", response_model=CrisisAnalysis)
async def detect_crisis(request: MessageRequest):
    """Analyze message for crisis indicators"""
    if not crisis_detector:
        raise HTTPException(status_code=503, detail="Crisis detector not available")
    
    try:
        risk_level, analysis = crisis_detector.detect_crisis(request.message, request.context)
        safety_message = crisis_detector.generate_safety_prompt(risk_level)
        
        return CrisisAnalysis(
            risk_level=risk_level.value,
            confidence=analysis["confidence"],
            triggers_detected=analysis["triggers_detected"],
            recommendation=analysis["recommendation"],
            resources=analysis["resources"],
            safety_message=safety_message
        )
    except Exception as e:
        logger.error(f"Error in crisis detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/safety/emergency-resources")
async def get_emergency_resources():
    """Get comprehensive emergency resources"""
    if not crisis_detector:
        raise HTTPException(status_code=503, detail="Crisis detector not available")
    
    return {
        "emergency": True,
        "resources": crisis_detector.emergency_resources,
        "message": "If you're in immediate danger, call 911 or your local emergency number"
    }

@app.get("/safety/crisis-log")
async def get_crisis_log():
    """Get log of detected crises (for monitoring purposes)"""
    if not crisis_detector:
        raise HTTPException(status_code=503, detail="Crisis detector not available")
    
    return {
        "crisis_count": len(crisis_detector.crisis_log),
        "recent_incidents": crisis_detector.crisis_log[-10:] if crisis_detector.crisis_log else []
    }

# Emergency resources
@app.get("/emergency")
async def get_emergency_resources_legacy():
    """Get emergency mental health resources (legacy endpoint)"""
    return {
        "emergency": True,
        "resources": [
            {
                "name": "National Suicide Prevention Lifeline",
                "number": "988",
                "url": "https://suicidepreventionlifeline.org"
            },
            {
                "name": "Crisis Text Line",
                "text": "Text HOME to 741741",
                "url": "https://www.crisistextline.org"
            },
            {
                "name": "International Association for Suicide Prevention",
                "url": "https://www.iasp.info/resources/Crisis_Centres"
            }
        ]
    }

# ============================================================================
# NEW: Orchestrator Status & Monitoring Endpoints
# ============================================================================

@app.get("/orchestrator/status")
async def get_orchestrator_status():
    """Get status of LangGraph orchestrator and its agents"""
    if not orchestrator:
        return {
            "status": "unavailable",
            "message": "Orchestrator not initialized",
            "agents": []
        }
    
    try:
        return {
            "status": "ready",
            "orchestrator_type": "LangGraph",
            "agents": [
                {"name": "QueryRouter", "status": "active", "purpose": "Route user queries to appropriate agent"},
                {"name": "AssessmentAgent", "status": "active", "purpose": "Psychological assessment & analysis"},
                {"name": "CrisisResponse", "status": "active", "purpose": "Crisis detection & immediate support"},
                {"name": "TherapySupport", "status": "active", "purpose": "Therapeutic guidance & coping strategies"},
                {"name": "ResourceFinder", "status": "active", "purpose": "Find relevant mental health resources"},
                {"name": "RAGAgent", "status": "active", "purpose": "Evidence-based knowledge retrieval"}
            ],
            "rag_agent_available": rag_agent is not None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting orchestrator status: {e}")
        return {
            "status": "error",
            "message": str(e),
            "agents": []
        }

# ============================================================================
# NEW: Knowledge Base & RAG Endpoints
# ============================================================================

@app.post("/knowledge/search")
async def search_knowledge_base(request: MessageRequest):
    """Search knowledge base for relevant information"""
    if not rag_agent:
        raise HTTPException(status_code=503, detail="RAG agent not available")
    
    try:
        # Search vector store with fallback to general query
        query = request.message or "mental health support"
        logger.info(f"🔍 Searching knowledge base for: {query}")
        
        results = rag_agent.retrieve_relevant_knowledge(query=query, k=5)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results) if results else 0,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/topics")
async def get_knowledge_topics():
    """Get list of available knowledge base topics"""
    if not rag_agent:
        raise HTTPException(status_code=503, detail="RAG agent not available")
    
    try:
        topics = [
            "Depression & Mood Disorders",
            "Anxiety & Panic Disorders",
            "PTSD & Trauma",
            "Sleep & Insomnia",
            "Stress Management",
            "Cognitive Behavioral Therapy (CBT)",
            "Dialectical Behavior Therapy (DBT)",
            "Mindfulness & Meditation",
            "Exercise & Physical Health",
            "Nutrition & Mental Health",
            "Breathing Exercises",
            "Grounding Techniques",
            "Crisis Resources",
            "Therapeutic Techniques",
            "Mental Health Conditions"
        ]
        
        return {
            "success": True,
            "topics": topics,
            "count": len(topics),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting knowledge topics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/info/{topic}")
async def get_evidence_based_info(topic: str):
    """Get comprehensive evidence-based information on a specific topic"""
    if not rag_agent:
        raise HTTPException(status_code=503, detail="RAG agent not available")
    
    try:
        logger.info(f"📖 Retrieving evidence-based information on: {topic}")
        
        # Create a detailed query
        query = f"Comprehensive guide to {topic} evidence-based treatment therapy techniques"
        
        # Retrieve relevant knowledge
        knowledge = rag_agent.retrieve_relevant_knowledge(query=query, k=10)
        
        # Generate response with context
        response = rag_agent.generate_response_with_knowledge(
            user_query=f"Tell me about {topic}",
            retrieved_knowledge=knowledge
        )
        
        return {
            "success": True,
            "topic": topic,
            "information": response,
            "sources": knowledge if knowledge else [],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting evidence-based info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/sources")
async def get_knowledge_sources():
    """Get information about available knowledge sources"""
    if not rag_agent:
        raise HTTPException(status_code=503, detail="RAG agent not available")
    
    try:
        sources = [
            {
                "name": "Mental Health Conditions Database",
                "type": "CSV",
                "entries": "10+ conditions",
                "coverage": "Depression, Anxiety, PTSD, OCD, ADHD, Bipolar, Eating Disorders, etc."
            },
            {
                "name": "Therapeutic Techniques Database",
                "type": "CSV",
                "entries": "20+ techniques",
                "coverage": "CBT, DBT, IPT, ACT, MBSR, Exercise, Sleep, Nutrition, etc."
            },
            {
                "name": "Crisis Resources Database",
                "type": "CSV",
                "entries": "25+ resources",
                "coverage": "Emergency hotlines, Crisis text lines, LGBTQ+ support, etc."
            },
            {
                "name": "Understanding Depression Guide",
                "type": "Text",
                "length": "3000+ words",
                "coverage": "Symptoms, causes, treatments, recovery strategies"
            },
            {
                "name": "Managing Anxiety Guide",
                "type": "Text",
                "length": "3000+ words",
                "coverage": "Types, triggers, treatments, coping techniques"
            }
        ]
        
        return {
            "success": True,
            "sources": sources,
            "total_sources": len(sources),
            "total_entries": "50+",
            "total_content": "6000+ words of knowledge"
        }
    except Exception as e:
        logger.error(f"Error getting knowledge sources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
