"""
Crisis Detection Agent - Mental Health Crisis Assessment
Specializes in identifying mental health crises and routing to appropriate resources
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from typing import Dict, List, Optional, Any
import json
import logging
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class RiskLevel(str, Enum):
    """Risk level classification"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class CrisisDetectionAgent:
    """
    Specialized agent for crisis detection and intervention
    - Identifies crisis indicators
    - Assesses risk level
    - Routes to emergency services
    - Provides immediate support
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.crisis_keywords = self._initialize_crisis_keywords()
        
        self.crisis_detection_tool = Tool(
            name="detect_crisis",
            description="Detect potential mental health crisis",
            func=self.detect_crisis
        )
        
        self.risk_assessment_tool = Tool(
            name="assess_risk",
            description="Assess risk level and provide resources",
            func=self.assess_risk
        )
    
    def _initialize_crisis_keywords(self) -> Dict[str, List[str]]:
        """Initialize crisis indicator keywords and phrases"""
        return {
            "suicidal_ideation": [
                "kill myself", "end it all", "don't want to live",
                "better off dead", "suicide", "harm myself", "slit wrist",
                "jump off", "overdose", "no reason to live"
            ],
            "self_harm": [
                "cutting myself", "harm myself", "hurt myself",
                "self injury", "self mutilation", "burning myself"
            ],
            "severe_depression": [
                "completely hopeless", "total despair", "can't go on",
                "trapped", "suffocating", "paralyzed", "numb"
            ],
            "severe_anxiety": [
                "panic attack", "can't breathe", "heart attack",
                "losing control", "going crazy", "breakdown"
            ],
            "acute_psychosis": [
                "hearing voices", "seeing things", "people watching",
                "mind control", "alien thoughts", "hallucinations"
            ],
            "substance_abuse": [
                "overdose", "high dose", "mixing drugs",
                "alcohol poisoning", "abusing medication"
            ]
        }
    
    def _get_emergency_resources(self) -> Dict[str, Any]:
        """Get emergency resources and hotlines"""
        return {
            "immediate_action": [
                "If in immediate danger: Call Emergency Services (911 in US)",
                "Go to nearest Emergency Room",
                "Call Crisis Text Line: Text HOME to 741741",
                "Contact National Suicide Prevention Lifeline: 988"
            ],
            "crisis_hotlines": {
                "National Suicide Prevention Lifeline": "1-800-273-8255",
                "Crisis Text Line": "Text HOME to 741741",
                "SAMHSA National Helpline": "1-800-662-4357",
                "Veterans Crisis Line": "1-800-273-8255 then press 1",
                "Substance Abuse Hotline": "1-800-448-4663"
            },
            "online_resources": {
                "IMAlive": "https://www.imalive.org/",
                "Crisis Now": "https://crisischat.org/",
                "7 Cups": "https://www.7cups.com/"
            }
        }
    
    def detect_crisis(self, text: str) -> Dict[str, Any]:
        """Detect crisis indicators in text"""
        text_lower = text.lower()
        detected_indicators = []
        
        for indicator_type, keywords in self.crisis_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_indicators.append(indicator_type)
                    break
        
        return {
            "crisis_detected": len(detected_indicators) > 0,
            "indicators": detected_indicators,
            "indicator_count": len(detected_indicators)
        }
    
    def assess_risk(self, crisis_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level based on detected indicators"""
        indicators = crisis_analysis.get("indicators", [])
        
        # Determine risk level
        if "suicidal_ideation" in indicators:
            risk_level = RiskLevel.CRITICAL
            confidence = 0.95
        elif "severe_depression" in indicators or "acute_psychosis" in indicators:
            risk_level = RiskLevel.HIGH
            confidence = 0.85
        elif "self_harm" in indicators or "substance_abuse" in indicators:
            risk_level = RiskLevel.HIGH
            confidence = 0.80
        elif "severe_anxiety" in indicators:
            risk_level = RiskLevel.MODERATE
            confidence = 0.75
        else:
            risk_level = RiskLevel.LOW
            confidence = 0.5
        
        return {
            "risk_level": risk_level.value,
            "confidence": confidence,
            "indicators_detected": indicators,
            "urgent_action_required": risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL],
            "resources": self._get_emergency_resources(),
            "recommendation": self._get_recommendation(risk_level)
        }
    
    def _get_recommendation(self, risk_level: RiskLevel) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            RiskLevel.CRITICAL: "URGENT: Immediate professional intervention required. Call emergency services or go to ER.",
            RiskLevel.HIGH: "Please reach out to a mental health professional or crisis line immediately.",
            RiskLevel.MODERATE: "Consider contacting a mental health professional soon. Crisis resources available 24/7.",
            RiskLevel.LOW: "Continue monitoring. Reach out to support network or professional if needed."
        }
        return recommendations.get(risk_level, "")
    
    async def process(self, query: str) -> Dict[str, Any]:
        """Process crisis-related query"""
        # First, detect crisis indicators
        crisis_analysis = self.detect_crisis(query)
        
        if crisis_analysis["crisis_detected"]:
            # Assess risk
            risk_assessment = self.assess_risk(crisis_analysis)
            return {
                "agent": "crisis_detection",
                "crisis_detected": True,
                "analysis": risk_assessment,
                "timestamp": datetime.now().isoformat()
            }
        
        # If no crisis detected, process normally
        prompt = f"""You are a mental health crisis counselor.
        User concern: {query}
        
        Provide supportive response and guidance."""
        
        try:
            message = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return {
                "agent": "crisis_detection",
                "crisis_detected": False,
                "response": message.content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Crisis detection agent error: {e}")
            return {"agent": "crisis_detection", "error": str(e)}
