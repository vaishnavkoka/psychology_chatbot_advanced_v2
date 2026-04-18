"""
Psychology Insights Agent - Mental Health Analysis and Insights
Analyzes patterns, provides insights, and generates personalized recommendations
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class InsightsAgent:
    """
    Specialized agent for generating insights and analysis
    - Analyzes mental health patterns
    - Identifies trends over time
    - Generates personalized recommendations
    - Provides psychoeducation
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.psychoeducation_topics = self._initialize_psychoeducation()
        
        self.insights_tool = Tool(
            name="generate_insights",
            description="Generate insights from mental health data",
            func=self.generate_insights
        )
        
        self.trend_analysis_tool = Tool(
            name="analyze_trends",
            description="Analyze patterns and trends in mental health",
            func=self.analyze_trends
        )
    
    def _initialize_psychoeducation(self) -> Dict[str, Any]:
        """Initialize psychoeducation topics"""
        return {
            "depression": {
                "definition": "Persistent depressed mood affecting daily functioning",
                "symptoms": [
                    "Persistent sad mood",
                    "Loss of interest/pleasure",
                    "Changes in sleep/appetite",
                    "Fatigue",
                    "Guilt or worthlessness",
                    "Difficulty concentrating",
                    "Suicidal thoughts"
                ],
                "causes": ["Genetics", "Life events", "Brain chemistry", "Medical conditions"],
                "treatments": ["Therapy", "Medication", "Lifestyle changes", "Support groups"]
            },
            "anxiety": {
                "definition": "Excessive worry and fear affecting daily life",
                "symptoms": [
                    "Excessive worry",
                    "Restlessness",
                    "Irritability",
                    "Difficulty sleeping",
                    "Panic symptoms",
                    "Avoidance behaviors"
                ],
                "causes": ["Stress", "Genetics", "Medical conditions", "Substance use"],
                "treatments": ["CBT", "Meditation", "Exercise", "Medication"]
            },
            "stress": {
                "definition": "Response to demanding situations",
                "signs": [
                    "Overwhelming feeling",
                    "Sleep disturbance",
                    "Difficulty concentrating",
                    "Irritability",
                    "Physical symptoms"
                ],
                "management": [
                    "Time management",
                    "Exercise",
                    "Relaxation techniques",
                    "Social support",
                    "Professional help"
                ]
            }
        }
    
    def generate_insights(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights from session data"""
        insights = []
        recommendations = []
        
        # Analyze session patterns
        if "mood_scores" in session_data:
            avg_mood = sum(session_data["mood_scores"]) / len(session_data["mood_scores"])
            if avg_mood < 3:
                insights.append("Consistently low mood detected - consider professional support")
                recommendations.append("Schedule therapy session")
            elif avg_mood < 5:
                insights.append("Moderate mood variability - practice coping strategies")
                recommendations.append("Daily mindfulness practice")
        
        # Analyze common concerns
        if "concerns" in session_data:
            concern_count = len(session_data["concerns"])
            if concern_count > 5:
                insights.append("Multiple concerns identified - prioritize addressing key issues")
                recommendations.append("Practice problem-solving technique")
        
        # Analyze engagement
        if "session_frequency" in session_data:
            if session_data["session_frequency"] < 1:
                insights.append("Low engagement - consider more frequent check-ins")
                recommendations.append("Set reminder for daily mental health check-in")
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "analysis_date": datetime.now().isoformat(),
            "next_review": "7 days"
        }
    
    def analyze_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trends in mental health over time"""
        if not historical_data:
            return {"error": "No historical data available"}
        
        trends = {
            "mood_trend": "stable",
            "concern_evolution": [],
            "improvement_areas": [],
            "areas_of_concern": [],
            "overall_trajectory": "stable"
        }
        
        # Calculate mood trend
        if len(historical_data) > 1:
            recent_mood = historical_data[-1].get("mood_score", 5)
            older_mood = historical_data[0].get("mood_score", 5)
            if recent_mood > older_mood:
                trends["mood_trend"] = "improving"
                trends["overall_trajectory"] = "positive"
            elif recent_mood < older_mood:
                trends["mood_trend"] = "declining"
                trends["overall_trajectory"] = "needs attention"
        
        return trends
    
    async def process(self, query: str, session_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Process insights query"""
        prompt = f"""You are a mental health insights specialist.
        
        User question: {query}
        
        Provide personalized insights based on mental health principles and psychoeducation.
        Be specific, practical, and empowering."""
        
        try:
            message = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            # Generate insights if history available
            insights = {}
            if session_history:
                insights = self.generate_insights({"concerns": session_history})
            
            return {
                "agent": "insights",
                "response": message.content,
                "insights": insights,
                "psychoeducation": self.psychoeducation_topics,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Insights agent error: {e}")
            return {"agent": "insights", "error": str(e)}
