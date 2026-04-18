"""
Therapeutic Support Agent - Evidence-Based Mental Health Support
Provides therapeutic guidance, coping strategies, and evidence-based techniques
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import Tool
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TherapeuticSupportAgent:
    """
    Specialized agent for therapeutic support and coping strategies
    - Provides evidence-based therapeutic techniques
    - Suggests coping strategies
    - Offers emotional support
    - Guides self-help interventions
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.therapeutic_techniques = self._initialize_techniques()
        
        self.support_tool = Tool(
            name="provide_support",
            description="Provide therapeutic support and coping strategies",
            func=self.provide_support
        )
        
        self.coping_strategies_tool = Tool(
            name="suggest_coping_strategies",
            description="Suggest evidence-based coping strategies",
            func=self.suggest_coping_strategies
        )
    
    def _initialize_techniques(self) -> Dict[str, Any]:
        """Initialize therapeutic techniques database"""
        return {
            "cbt_techniques": {
                "name": "Cognitive Behavioral Therapy",
                "techniques": [
                    {
                        "name": "Thought Records",
                        "description": "Identify and challenge negative thoughts",
                        "steps": [
                            "Write the triggering event",
                            "Note your automatic thought",
                            "Identify the emotion felt",
                            "Challenge the thought with evidence",
                            "Develop an alternative thought"
                        ]
                    },
                    {
                        "name": "Behavioral Activation",
                        "description": "Increase engagement in positive activities",
                        "steps": [
                            "List activities that usually bring pleasure",
                            "Schedule specific activities",
                            "Track completion and mood",
                            "Gradually increase difficulty"
                        ]
                    }
                ]
            },
            "mindfulness_techniques": {
                "name": "Mindfulness & Meditation",
                "techniques": [
                    {
                        "name": "Body Scan Meditation",
                        "description": "Progressive awareness of body sensations",
                        "duration": "10-20 minutes",
                        "benefits": ["Reduces anxiety", "Increases body awareness", "Improves relaxation"]
                    },
                    {
                        "name": "Breathing Exercises",
                        "description": "Controlled breathing to calm nervous system",
                        "techniques": ["4-7-8 Breathing", "Box Breathing", "Diaphragmatic Breathing"]
                    }
                ]
            },
            "emotion_regulation": {
                "name": "Emotion Regulation Techniques",
                "techniques": [
                    {
                        "name": "TIPP Skills",
                        "description": "Quick emotion regulation",
                        "skills": [
                            "T - Temperature: Cold water on face",
                            "I - Intense Exercise: Quick physical activity",
                            "P - Paced Breathing: Slow breathing",
                            "P - Paired Muscle Relaxation: Tense and release muscles"
                        ]
                    }
                ]
            },
            "stress_management": {
                "name": "Stress Management Strategies",
                "strategies": [
                    "Progressive Muscle Relaxation",
                    "Guided Imagery",
                    "Journaling",
                    "Physical Exercise",
                    "Social Connection",
                    "Time Management",
                    "Problem Solving"
                ]
            }
        }
    
    def provide_support(self, concern: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Provide therapeutic support"""
        return {
            "concern": concern,
            "therapeutic_approaches": [
                "Cognitive Behavioral Therapy (CBT)",
                "mindfulness and meditation",
                "Emotion Regulation",
                "Stress Management"
            ],
            "key_message": "You are not alone. There are evidence-based strategies that can help.",
            "next_steps": [
                "Choose an appropriate technique",
                "Practice consistently",
                "Track your progress",
                "Seek professional help if needed"
            ]
        }
    
    def suggest_coping_strategies(self, issue: str) -> Dict[str, Any]:
        """Suggest coping strategies for specific issue"""
        strategies_map = {
            "anxiety": {
                "immediate": [
                    "Box Breathing (4-4-4-4 pattern)",
                    "5-4-3-2-1 Grounding Technique",
                    "Progressive Muscle Relaxation"
                ],
                "short_term": [
                    "Regular exercise (30 mins daily)",
                    "Mindfulness meditation",
                    "Limit caffeine intake"
                ],
                "long_term": [
                    "Cognitive Behavioral Therapy",
                    "Regular therapy sessions",
                    "Lifestyle modifications"
                ]
            },
            "depression": {
                "immediate": [
                    "Get outside for 10 minutes",
                    "Call a friend or family member",
                    "Engage in a small task"
                ],
                "short_term": [
                    "Behavioral Activation",
                    "Regular sleep schedule",
                    "Physical activity"
                ],
                "long_term": [
                    "Psychotherapy",
                    "Medication if recommended",
                    "Social support network"
                ]
            },
            "stress": {
                "immediate": [
                    "Take 5 deep breaths",
                    "Reduce caffeine",
                    "Take a short break"
                ],
                "short_term": [
                    "Time management",
                    "Relaxation techniques",
                    "Physical exercise"
                ],
                "long_term": [
                    "Work-life balance",
                    "Stress counseling",
                    "Lifestyle changes"
                ]
            }
        }
        
        issue_lower = issue.lower()
        for key in strategies_map:
            if key in issue_lower:
                return {
                    "issue": issue,
                    "strategies": strategies_map[key],
                    "effectiveness": "High when practiced consistently",
                    "timeline": "Results typically seen within 2-4 weeks"
                }
        
        return {
            "issue": issue,
            "strategies": {
                "immediate": ["Take a break", "Practice deep breathing"],
                "short_term": ["Structured routine", "Physical activity"],
                "long_term": ["Professional support", "Lifestyle optimization"]
            }
        }
    
    async def process(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process therapeutic support query"""
        prompt = f"""You are an empathetic therapeutic support specialist providing evidence-based guidance.
        
        User concern: {query}
        
        Provide supportive, practical advice based on evidence-based therapeutic approaches.
        Include coping strategies and self-help techniques where appropriate.
        Be warm and non-judgmental."""
        
        try:
            message = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return {
                "agent": "therapeutic_support",
                "response": message.content,
                "timestamp": datetime.now().isoformat(),
                "suggested_techniques": self.therapeutic_techniques
            }
        except Exception as e:
            logger.error(f"Therapeutic support agent error: {e}")
            return {"agent": "therapeutic_support", "error": str(e)}
