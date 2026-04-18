"""
Assessment Routes - Psychological Assessment API Endpoints
Handles all assessment administration, scoring, and results
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assessments", tags=["assessments"])

# ============================================================
# PYDANTIC MODELS
# ============================================================

class AssessmentStartRequest(BaseModel):
    """Request to start an assessment"""
    assessment_type: str  # phq9, gad7, psqi, rosenberg_ses, pcl5
    user_id: Optional[str] = None
    notes: Optional[str] = None

class AssessmentResponse(BaseModel):
    """Assessment questions and metadata"""
    assessment_id: str
    assessment_type: str
    assessment_name: str
    total_questions: int
    questions: List[str]
    score_range: Dict[str, Any]
    instructions: str
    estimated_time_minutes: int

class AssessmentAnswerRequest(BaseModel):
    """Submit assessment responses"""
    assessment_id: str
    responses: List[int]  # 0-3 or 0-4 depending on scale
    user_id: Optional[str] = None
    notes: Optional[str] = None

class AssessmentResult(BaseModel):
    """Assessment scoring result"""
    assessment_id: str
    assessment_type: str
    assessment_name: str
    total_score: int
    max_score: int
    percentage: float
    interpretation: str
    severity_level: str
    recommendations: List[str]
    requires_professional_help: bool
    crisis_resources: Optional[Dict] = None
    completed_at: str

class HistoricalAssessment(BaseModel):
    """Historical assessment record"""
    assessment_id: str
    assessment_type: str
    score: int
    interpretation: str
    completed_at: str

# ============================================================
# ASSESSMENT DATABASE
# ============================================================

ASSESSMENTS_DB = {
    "phq9": {
        "name": "Patient Health Questionnaire-9 (PHQ-9)",
        "description": "Screening and severity measure for depression",
        "duration_minutes": 3,
        "questions": [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself or that you're a failure",
            "Trouble concentrating on things",
            "Moving or speaking so slowly that others have noticed, or being fidgety",
            "Thoughts that you would be better off dead, or hurting yourself"
        ],
        "scale": "0-3 (Not at all, Several days, More than half, Nearly every day)",
        "max_score": 27,
        "scoring": {
            (0, 4): {"level": "minimal", "recommendation": "No treatment needed"},
            (5, 9): {"level": "mild", "recommendation": "Monitor and self-care"},
            (10, 14): {"level": "moderate", "recommendation": "Consider therapy"},
            (15, 19): {"level": "moderately_severe", "recommendation": "Therapy recommended"},
            (20, 27): {"level": "severe", "recommendation": "Urgent professional help"}
        }
    },
    "gad7": {
        "name": "Generalized Anxiety Disorder-7 (GAD-7)",
        "description": "Screening and severity measure for anxiety",
        "duration_minutes": 2,
        "questions": [
            "Feeling nervous, anxious, or on edge",
            "Not being able to stop or control worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it's hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid as if something awful might happen"
        ],
        "scale": "0-3 (Not at all, Several days, More than half, Nearly every day)",
        "max_score": 21,
        "scoring": {
            (0, 4): {"level": "minimal", "recommendation": "No treatment needed"},
            (5, 9): {"level": "mild", "recommendation": "Monitor and self-care"},
            (10, 14): {"level": "moderate", "recommendation": "Consider therapy"},
            (15, 21): {"level": "severe", "recommendation": "Professional help recommended"}
        }
    },
    "psqi": {
        "name": "Pittsburgh Sleep Quality Index (PSQI)",
        "description": "Comprehensive assessment of sleep quality",
        "duration_minutes": 10,
        "questions": [
            "During the past month, when have you usually gone to bed?",
            "How long (in minutes) has it usually taken you to fall asleep?",
            "During the past month, when have you usually gotten up?",
            "How many hours of actual sleep did you get at night?",
            "Overall, how would you rate your sleep quality?",
            "How often have you had trouble sleeping because you cannot get to sleep?",
            "How often have you taken medicine to sleep?"
        ],
        "scale": "Variable (time/hours/frequency)",
        "max_score": 21,
        "scoring": {
            (0, 5): {"level": "good", "recommendation": "Good sleep quality"},
            (6, 10): {"level": "poor", "recommendation": "Poor sleep quality"},
            (11, 21): {"level": "very_poor", "recommendation": "Very poor - consider sleep specialist"}
        }
    },
    "rosenberg_ses": {
        "name": "Rosenberg Self-Esteem Scale",
        "description": "Measure of global self-esteem",
        "duration_minutes": 2,
        "questions": [
            "I feel that I'm a person of worth",
            "I feel that I have a number of good qualities",
            "All in all, I am inclined to feel that I am a failure",
            "I am able to do things as well as most other people",
            "I feel I do not have much to be proud of",
            "I take a positive attitude toward myself",
            "On the whole, I am satisfied with myself",
            "I wish I could have more respect for myself",
            "I certainly feel useless at times",
            "At times I think I am no good at all"
        ],
        "scale": "0-3 (Strongly disagree to Strongly agree)",
        "max_score": 40,
        "scoring": {
            (10, 15): {"level": "low", "recommendation": "Low self-esteem - consider therapy"},
            (16, 25): {"level": "moderate", "recommendation": "Moderate self-esteem"},
            (26, 40): {"level": "high", "recommendation": "High self-esteem"}
        }
    },
    "pcl5": {
        "name": "PTSD Checklist-5 (PCL-5)",
        "description": "Screening for PTSD symptoms",
        "duration_minutes": 5,
        "questions": [
            "Repeated unwanted memories of the experience",
            "Repeated disturbing dreams related to the experience",
            "Suddenly feeling or acting as if the experience were happening again",
            "Feeling very upset when reminded of the experience",
            "Having strong physical reactions when reminded of the experience",
            "Avoiding memories, thoughts, or feelings related to the experience",
            "Avoiding external reminders of the experience",
            "Difficulty remembering important parts of the experience",
            "Negative beliefs about yourself or the world",
            "Blaming yourself or someone else for the experience",
            "Negative feelings like fear, anger, guilt, or shame",
            "Decreased interest in activities",
            "Feeling detached or cut off from people",
            "Difficulty concentrating",
            "Irritability or aggressiveness",
            "Taking risky or destructive actions",
            "Being overly watchful or on guard",
            "Difficulty relaxing",
            "Being easily startled",
            "Having difficulty falling or staying asleep"
        ],
        "scale": "0-4 (Not at all, A little, Moderately, Quite a bit, Extremely)",
        "max_score": 80,
        "scoring": {
            (0, 10): {"level": "minimal", "recommendation": "Minimal PTSD symptoms"},
            (11, 20): {"level": "mild", "recommendation": "Mild PTSD symptoms"},
            (21, 33): {"level": "moderate", "recommendation": "Moderate PTSD - consider therapy"},
            (34, 46): {"level": "severe", "recommendation": "Severe PTSD - professional help recommended"},
            (47, 80): {"level": "very_severe", "recommendation": "Very severe - urgent professional intervention"}
        }
    }
}

# ============================================================
# ENDPOINTS
# ============================================================

@router.post("/start")
async def start_assessment(request: AssessmentStartRequest) -> AssessmentResponse:
    """Start a psychological assessment
    
    Args:
        request: Assessment type and user info
    
    Returns:
        Questions and scoring information
    """
    assessment_type = request.assessment_type.lower()
    
    if assessment_type not in ASSESSMENTS_DB:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown assessment type: {assessment_type}. Available: {list(ASSESSMENTS_DB.keys())}"
        )
    
    assessment_DB = ASSESSMENTS_DB[assessment_type]
    assessment_id = f"{assessment_type}_{datetime.now().timestamp()}"
    
    logger.info(f"✅ Started {assessment_type} for user {request.user_id}")
    
    return AssessmentResponse(
        assessment_id=assessment_id,
        assessment_type=assessment_type,
        assessment_name=assessment_DB["name"],
        total_questions=len(assessment_DB["questions"]),
        questions=assessment_DB["questions"],
        score_range={"min": 0, "max": assessment_DB["max_score"]},
        instructions=f"Rate each statement based on {assessment_DB['scale']}. This assessment takes approximately {assessment_DB['duration_minutes']} minutes.",
        estimated_time_minutes=assessment_DB["duration_minutes"]
    )

@router.post("/score")
async def score_assessment(request: AssessmentAnswerRequest) -> AssessmentResult:
    """Score assessment responses
    
    Args:
        request: Assessment ID and responses
    
    Returns:
        Scored result with interpretation
    """
    # Parse assessment type from ID
    assessment_type = request.assessment_id.split('_')[0].lower()
    
    if assessment_type not in ASSESSMENTS_DB:
        raise HTTPException(status_code=400, detail="Invalid assessment ID")
    
    assessment_db = ASSESSMENTS_DB[assessment_type]
    
    # Validate number of responses
    if len(request.responses) != len(assessment_db["questions"]):
        raise HTTPException(
            status_code=400,
            detail=f"Expected {len(assessment_db['questions'])} responses, got {len(request.responses)}"
        )
    
    # Calculate score
    total_score = sum(request.responses)
    max_score = assessment_db["max_score"]
    percentage = (total_score / max_score) * 100
    
    # Find interpretation
    interpretation_data = None
    for score_range, interpretation in assessment_db["scoring"].items():
        if score_range[0] <= total_score <= score_range[1]:
            interpretation_data = interpretation
            break
    
    if not interpretation_data:
        interpretation_data = {"level": "unknown", "recommendation": "Unable to interpret"}
    
    # Determine if professional help needed
    requires_help = total_score >= (max_score * 0.6)  # 60% threshold
    
    # Get crisis resources if needed
    crisis_resources = None
    if total_score >= (max_score * 0.75):  # 75% = high risk
        crisis_resources = {
            "crisis_line": "988",
            "text_line": "Text HOME to 741741",
            "immediate_help": "Go to nearest Emergency Room"
        }
    
    logger.info(f"✅ Scored {assessment_type}: {total_score}/{max_score} ({percentage:.1f}%)")
    
    return AssessmentResult(
        assessment_id=request.assessment_id,
        assessment_type=assessment_type,
        assessment_name=assessment_db["name"],
        total_score=total_score,
        max_score=max_score,
        percentage=percentage,
        interpretation=interpretation_data["recommendation"],
        severity_level=interpretation_data["level"],
        recommendations=[interpretation_data["recommendation"]],
        requires_professional_help=requires_help,
        crisis_resources=crisis_resources,
        completed_at=datetime.now().isoformat()
    )

@router.get("/available")
async def get_available_assessments() -> Dict[str, Any]:
    """Get list of available assessments"""
    assessments = {}
    for key, data in ASSESSMENTS_DB.items():
        assessments[key] = {
            "name": data["name"],
            "description": data["description"],
            "duration_minutes": data["duration_minutes"],
            "questions_count": len(data["questions"])
        }
    return assessments

@router.get("/{assessment_type}/info")
async def get_assessment_info(assessment_type: str) -> Dict[str, Any]:
    """Get detailed info about specific assessment"""
    assessment_type = assessment_type.lower()
    
    if assessment_type not in ASSESSMENTS_DB:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    data = ASSESSMENTS_DB[assessment_type]
    return {
        "type": assessment_type,
        "name": data["name"],
        "description": data["description"],
        "duration_minutes": data["duration_minutes"],
        "questions_count": len(data["questions"]),
        "scale": data["scale"],
        "max_score": data["max_score"]
    }

@router.get("/history/{user_id}")
async def get_assessment_history(user_id: str) -> Dict[str, Any]:
    """Get user's assessment history"""
    # TODO: Implement database query
    return {
        "user_id": user_id,
        "assessments": [],
        "total_completed": 0,
        "message": "Assessment history retrieval not yet implemented"
    }

# Health check
@router.get("/health")
async def assessment_health():
    """Health check for assessment service"""
    return {
        "status": "healthy",
        "available_assessments": list(ASSESSMENTS_DB.keys()),
        "count": len(ASSESSMENTS_DB)
    }
