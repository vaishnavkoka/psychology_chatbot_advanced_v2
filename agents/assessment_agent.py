"""
Assessment Agent - Psychological Assessment Administration
Specializes in delivering and scoring validated mental health assessments
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AssessmentAgent:
    """
    Specialized agent for psychological assessments
    - Administers validated assessments (PHQ-9 for depression, GAD-7 for anxiety, etc.)
    - Scores responses accurately
    - Provides initial interpretation
    - Routes to support if needed
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.assessments_db = self._initialize_assessments()
        
        self.assessment_tool = Tool(
            name="administer_assessment",
            description="Administer a psychological assessment",
            func=self.administer_assessment
        )
        
        self.score_assessment_tool = Tool(
            name="score_assessment",
            description="Score assessment responses",
            func=self.score_assessment
        )
    
    def _initialize_assessments(self) -> Dict[str, Any]:
        """Initialize assessment database"""
        return {
            "phq9": {
                "name": "PHQ-9 Depression Scale",
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
                "scoring": {
                    (0, 4): "Minimal depression",
                    (5, 9): "Mild depression",
                    (10, 14): "Moderate depression",
                    (15, 19): "Moderately severe depression",
                    (20, 27): "Severe depression"
                }
            },
            "gad7": {
                "name": "GAD-7 Anxiety Scale",
                "questions": [
                    "Feeling nervous, anxious, or on edge",
                    "Not being able to stop or control worrying",
                    "Worrying too much about different things",
                    "Trouble relaxing",
                    "Being so restless that it's hard to sit still",
                    "Becoming easily annoyed or irritable",
                    "Feeling afraid as if something awful might happen"
                ],
                "scoring": {
                    (0, 4): "Minimal anxiety",
                    (5, 9): "Mild anxiety",
                    (10, 14): "Moderate anxiety",
                    (15, 21): "Severe anxiety"
                }
            },
            "psqi": {
                "name": "PSQI Sleep Quality Scale",
                "questions": [
                    "Bedtime",
                    "Sleep latency (how long to fall asleep)",
                    "Sleep duration",
                    "Habitual sleep efficiency",
                    "Sleep disturbances frequency",
                    "Use of sleeping medications",
                    "Daytime dysfunction"
                ],
                "scoring": {
                    (0, 5): "Good sleep quality",
                    (6, 10): "Poor sleep quality",
                    (11, 21): "Very poor sleep quality"
                }
            },
            "rosenberg_ses": {
                "name": "Rosenberg Self-Esteem Scale",
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
                "scoring": {
                    (10, 15): "Low self-esteem",
                    (16, 25): "Moderate self-esteem",
                    (26, 40): "High self-esteem"
                }
            }
        }
    
    def administer_assessment(self, assessment_type: str) -> Dict[str, Any]:
        """Administer an assessment"""
        if assessment_type not in self.assessments_db:
            return {"error": f"Assessment {assessment_type} not found"}
        
        assessment = self.assessments_db[assessment_type]
        return {
            "assessment_id": assessment_type,
            "name": assessment["name"],
            "questions": assessment["questions"],
            "total_questions": len(assessment["questions"]),
            "instructions": f"Please rate each statement on a scale of 0-3 or as appropriate for {assessment['name']}"
        }
    
    def score_assessment(self, assessment_type: str, responses: List[int]) -> Dict[str, Any]:
        """Score assessment responses"""
        if assessment_type not in self.assessments_db:
            return {"error": f"Assessment {assessment_type} not found"}
        
        assessment = self.assessments_db[assessment_type]
        total_score = sum(responses)
        
        # Find interpretation
        interpretation = "Unable to interpret"
        for score_range, interpretation_text in assessment["scoring"].items():
            if score_range[0] <= total_score <= score_range[1]:
                interpretation = interpretation_text
                break
        
        return {
            "assessment_id": assessment_type,
            "name": assessment["name"],
            "total_score": total_score,
            "interpretation": interpretation,
            "timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_recommendations(assessment_type, total_score)
        }
    
    def _generate_recommendations(self, assessment_type: str, score: int) -> List[str]:
        """Generate recommendations based on score"""
        recommendations = {
            "phq9": {
                "severe": [
                    "Please seek immediate professional help",
                    "Contact a mental health professional",
                    "Consider psychotherapy or medication",
                    "Crisis hotline available 24/7"
                ],
                "moderate": [
                    "Consider consulting a mental health professional",
                    "Practice stress management techniques",
                    "Maintain regular sleep and exercise"
                ],
                "mild": [
                    "Monitor your mood regularly",
                    "Practice self-care and mindfulness",
                    "Maintain social connections"
                ]
            }
        }
        
        if assessment_type in recommendations:
            for severity, recs in recommendations[assessment_type].items():
                if severity in assessment_type:
                    return recs
        
        return ["Continue monitoring your mental health", "Practice self-care regularly"]
    
    async def process(self, query: str) -> Dict[str, Any]:
        """Process assessment-related query"""
        prompt = f"""You are a psychological assessment specialist. 
        User query: {query}
        
        Provide appropriate assessment administration guidance or scoring."""
        
        try:
            message = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return {
                "agent": "assessment",
                "response": message.content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Assessment agent error: {e}")
            return {"agent": "assessment", "error": str(e)}
