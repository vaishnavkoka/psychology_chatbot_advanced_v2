"""
Crisis Detection and Safety Module
Monitors user inputs for indications of crisis or harm
"""

import re
import json
import os
from typing import Dict, List, Tuple, Optional
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk assessment levels"""
    GREEN = "green"      # No risk
    YELLOW = "yellow"    # Low risk, needs monitoring
    ORANGE = "orange"    # Medium risk, intervention needed
    RED = "red"          # High risk, immediate help needed

class CrisisDetector:
    """Detects and manages crisis situations"""
    
    def __init__(self):
        self.trigger_phrases = self._load_triggers()
        self.crisis_keywords = self._load_crisis_keywords()
        self.emergency_resources = self._load_emergency_resources()
        self.crisis_log = []
        
    def _load_triggers(self) -> Dict[str, List[str]]:
        """Load crisis trigger phrases"""
        return {
            "suicidal": [
                "want to die", "kill myself", "end my life", "suicide", 
                "no point in living", "better off dead", "take my own life",
                "end it all", "don't want to live", "harm myself", "cut myself"
            ],
            "self_harm": [
                "cut myself", "hurt myself", "hit myself", "injure",
                "self-harm", "burn myself", "starve myself", "purge"
            ],
            "abuse": [
                "being abused", "domestic violence", "being hit", "assault",
                "rape", "being hurt by", "abuse"
            ],
            "severe_mental": [
                "hearing voices", "seeing things", "losing touch with reality",
                "hallucinating", "paranoid", "can't think straight",
                "nervous breakdown", "going crazy"
            ],
            "substance": [
                "overdose", "took too much", "poison", "toxic",
                "can't stop drinking", "withdraw from drugs"
            ]
        }
    
    def _load_crisis_keywords(self) -> Dict[str, List[str]]:
        """Load severity indicators"""
        return {
            "immediate": ["now", "right now", "immediately", "urgent", "emergency"],
            "intent": ["plan to", "going to", "will", "tomorrow", "soon"],
            "means": ["pills", "knife", "rope", "gun", "weapon", "method"],
            "isolation": ["alone", "no one", "nobody cares", "isolated", "alone"]
        }
    
    def _load_emergency_resources(self) -> Dict[str, Dict]:
        """Load emergency contact information"""
        return {
            "US": {
                "987_crisis": {
                    "name": "Suicide & Crisis Lifeline",
                    "number": "988",
                    "text": "Text 'HELLO' to 741741",
                    "url": "https://988lifeline.org",
                    "available": "24/7",
                    "description": "Free, confidential support for suicidal crisis and emotional distress"
                },
                "crisis_text": {
                    "name": "Crisis Text Line",
                    "number": "Text HOME to 741741",
                    "url": "https://www.crisistextline.org",
                    "available": "24/7",
                    "description": "Crisis support via text message"
                },
                "nami_helpline": {
                    "name": "NAMI Helpline",
                    "number": "1-800-950-NAMI (6264)",
                    "url": "https://www.nami.org/help",
                    "available": "M-F 10am-10pm ET",
                    "description": "Mental health resources and peer support"
                },
                "emergency": {
                    "name": "National Emergency",
                    "number": "911",
                    "description": "Call 911 for immediate life-threatening emergency"
                }
            },
            "INTERNATIONAL": {
                "findhelp": {
                    "url": "https://www.findahelpline.com",
                    "description": "International crisis helpline finder"
                }
            }
        }
    
    def detect_crisis(self, user_message: str, context: Optional[Dict] = None) -> Tuple[RiskLevel, Dict]:
        """
        Detect crisis indicators in user message
        Returns (risk_level, analysis_dict)
        """
        message_lower = user_message.lower()
        
        # Initialize analysis
        analysis = {
            "risk_level": RiskLevel.GREEN,
            "triggers_detected": [],
            "risk_factors": [],
            "confidence": 0.0,
            "recommendation": None,
            "resources": None,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check for triggers
        trigger_count = 0
        for category, phrases in self.trigger_phrases.items():
            for phrase in phrases:
                if self._phrase_in_text(message_lower, phrase):
                    trigger_count += 1
                    analysis["triggers_detected"].append({
                        "category": category,
                        "phrase": phrase
                    })
        
        # Check for severity modifiers
        severity_score = self._calculate_severity(message_lower, analysis)
        
        # Determine risk level
        analysis["confidence"] = min(trigger_count * 0.3 + severity_score * 0.7, 1.0)
        
        if analysis["confidence"] >= 0.8:
            analysis["risk_level"] = RiskLevel.RED
        elif analysis["confidence"] >= 0.6:
            analysis["risk_level"] = RiskLevel.ORANGE
        elif analysis["confidence"] >= 0.3:
            analysis["risk_level"] = RiskLevel.YELLOW
        else:
            analysis["risk_level"] = RiskLevel.GREEN
        
        # Get recommendation and resources
        analysis["recommendation"] = self._get_recommendation(analysis["risk_level"])
        analysis["resources"] = self._get_resources(analysis["risk_level"])
        
        # Log crisis incident
        if analysis["risk_level"] in [RiskLevel.RED, RiskLevel.ORANGE]:
            self._log_crisis(user_message, analysis)
        
        return analysis["risk_level"], analysis
    
    def _phrase_in_text(self, text: str, phrase: str) -> bool:
        """Check if phrase appears in text with word boundaries"""
        pattern = r'\b' + re.escape(phrase) + r'\b'
        return bool(re.search(pattern, text, re.IGNORECASE))
    
    def _calculate_severity(self, message: str, analysis: Dict) -> float:
        """Calculate severity score based on modifiers"""
        score = 0.0
        
        # Check for urgency indicators
        for word in self.crisis_keywords["immediate"]:
            if self._phrase_in_text(message, word):
                score += 0.3
        
        # Check for stated intent
        for word in self.crisis_keywords["intent"]:
            if self._phrase_in_text(message, word):
                score += 0.25
        
        # Check for means
        for word in self.crisis_keywords["means"]:
            if self._phrase_in_text(message, word):
                score += 0.3
        
        # Check for isolation
        for word in self.crisis_keywords["isolation"]:
            if self._phrase_in_text(message, word):
                score += 0.15
        
        # Check for repetition/emphasis
        if "!!!" in message or "!!!!" in message:
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_recommendation(self, risk_level: RiskLevel) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            RiskLevel.GREEN: "Continue support and monitoring. Regular check-ins recommended.",
            RiskLevel.YELLOW: "Increase monitoring frequency. Encourage professional support.",
            RiskLevel.ORANGE: "⚠️ HIGH PRIORITY: Recommend immediate professional help. Consider contacting emergency services if situation worsens.",
            RiskLevel.RED: "🚨 CRITICAL: This requires immediate professional intervention. Please contact emergency services or crisis hotline NOW."
        }
        return recommendations.get(risk_level, "")
    
    def _get_resources(self, risk_level: RiskLevel) -> Dict:
        """Get appropriate resources based on risk level"""
        if risk_level in [RiskLevel.RED, RiskLevel.ORANGE]:
            return self.emergency_resources
        
        return None
    
    def _log_crisis(self, message: str, analysis: Dict):
        """Log crisis incident for monitoring"""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "risk_level": analysis["risk_level"].value,
            "confidence": analysis["confidence"],
            "triggers_count": len(analysis["triggers_detected"]),
            "message_preview": message[:100] + "..." if len(message) > 100 else message
        }
        self.crisis_log.append(incident)
        logger.warning(f"Crisis detected: {incident}")
    
    def get_crisis_log(self) -> List[Dict]:
        """Get log of detected crises"""
        return self.crisis_log
    
    def generate_safety_prompt(self, risk_level: RiskLevel) -> str:
        """Generate appropriate safety message"""
        if risk_level == RiskLevel.RED:
            return """
🚨 **IMMEDIATE HELP AVAILABLE** 🚨

I'm very concerned about what you've shared. Please reach out for immediate support:

**Call 988** (Suicide & Crisis Lifeline) - Available 24/7
**Text "HELLO" to 741741** (Crisis Text Line)
**Call 911** for immediate emergency

If you're in immediate danger, please contact emergency services.

You don't have to face this alone. Help is available right now.
            """
        elif risk_level == RiskLevel.ORANGE:
            return """
⚠️ **PROFESSIONAL SUPPORT RECOMMENDED** ⚠️

What you're experiencing sounds serious and would benefit from professional support.

**Consider reaching out to:**
- A therapist or counselor
- Your primary care doctor
- A local mental health clinic
- Crisis support line (988 in the US)

I'm here to listen and support, but a trained professional can provide the specialized help you deserve.
            """
        elif risk_level == RiskLevel.YELLOW:
            return """
💙 **Mental Health Support Available**

I hear that you're struggling. Please know that support is available:

**Resources:**
- Talk to a mental health professional
- Reach out to trusted friends or family
- Explore therapy options
- Call 988 if you need to talk (24/7, free, confidential)

I'm here to help, and so are many others. You're not alone in this.
            """
        else:
            return "I'm here to listen and support you. Feel free to share more about what you're experiencing."


# Global crisis detector instance
crisis_detector = CrisisDetector()
