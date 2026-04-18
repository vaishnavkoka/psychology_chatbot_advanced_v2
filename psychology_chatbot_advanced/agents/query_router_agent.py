"""
Query Router Agent - Intent Detection and Agent Routing
Routes user queries to appropriate agents based on intent
"""

from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from typing import Dict, List, Optional, Any
import json
import logging
import re

logger = logging.getLogger(__name__)

class QueryRouterAgent:
    """
    LangChain-based Query Router for psychology chatbot
    Routes queries to appropriate agents based on intent detection
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.intent_patterns = self._initialize_intent_patterns()
        
        self.routing_tool = Tool(
            name="route_query",
            description="Route user query to appropriate agents",
            func=self.route_query
        )
    
    def _initialize_intent_patterns(self) -> Dict[str, List[str]]:
        """Initialize pattern matching for intent detection"""
        return {
            "assessment": [
                "assessment", "test", "evaluate", "screen",
                "phq", "gad", "psqi", "depression scale",
                "anxiety scale", "self-esteem", "take assessment",
                "psychological test", "mental health test"
            ],
            "crisis": [
                "crisis", "emergency", "suicide", "self harm",
                "overdose", "danger", "immediate help",
                "urgent", "emergency help", "in danger"
            ],
            "support": [
                "help", "support", "cope", "strategy",
                "technique", "advice", "guidance",
                "deal with", "manage", "overcome",
                "problem solving", "coping mechanism"
            ],
            "insights": [
                "analyze", "pattern", "trend", "insight",
                "understand", "explain", "why", "reason",
                "psychoeducation", "learn about", "information"
            ],
            "rag": [
                "tell me", "explain", "what is", "define",
                "resource", "information", "knowledge",
                "how to", "tips", "facts about"
            ]
        }
    
    def _quick_intent_detection(self, query: str) -> Optional[str]:
        """Quick pattern-based intent detection"""
        query_lower = query.lower()
        
        for intent, keywords in self.intent_patterns.items():
            for keyword in keywords:
                if keyword in query_lower:
                    return intent
        
        return None
    
    async def _llm_intent_detection(self, query: str) -> Dict[str, Any]:
        """Use LLM for more nuanced intent detection"""
        prompt = f"""Analyze this user query and determine their primary intent.
        
        User query: {query}
        
        Possible intents:
        1. assessment - User wants to take a psychological assessment
        2. crisis - User is in crisis or needs urgent help
        3. support - User needs therapeutic support or coping strategies
        4. insights - User wants analysis or psychoeducation
        5. rag - User asking for general information or resources
        
        Respond with JSON:
        {{
            "primary_intent": "one of above",
            "confidence": 0.0-1.0,
            "secondary_intents": ["list of possible secondary intents"],
            "agents_needed": ["list of agents to activate"],
            "reasoning": "brief explanation"
        }}"""
        
        try:
            message = await self.llm.ainvoke([HumanMessage(content=prompt)])
            result = json.loads(message.content)
            return result
        except Exception as e:
            logger.error(f"LLM intent detection error: {e}")
            return {
                "primary_intent": "support",
                "confidence": 0.5,
                "secondary_intents": [],
                "agents_needed": ["therapeutic_support"],
                "error": str(e)
            }
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """Route query to appropriate agents"""
        # Quick pattern detection
        quick_intent = self._quick_intent_detection(query)
        
        # Map intent to agents
        intent_to_agents = {
            "assessment": ["crisis_detection", "assessment"],
            "crisis": ["crisis_detection", "therapeutic_support"],
            "support": ["therapeutic_support", "insights"],
            "insights": ["insights", "rag"],
            "rag": ["rag", "insights"]
        }
        
        agents = intent_to_agents.get(quick_intent, ["therapeutic_support", "rag"])
        
        return {
            "query": query,
            "detected_intent": quick_intent,
            "recommended_agents": agents,
            "requires_crisis_check": "crisis" in agents,
            "parallel_execution": len(agents) > 1
        }
    
    async def process(self, query: str) -> Dict[str, Any]:
        """Process routing query"""
        # Perform quick routing
        quick_route = self.route_query(query)
        
        # Get LLM-based detailed intent if needed
        llm_intent = await self._llm_intent_detection(query)
        
        return {
            "agent": "query_router",
            "original_query": query,
            "quick_route": quick_route,
            "llm_analysis": llm_intent,
            "final_agents": llm_intent.get("agents_needed", quick_route["recommended_agents"])
        }
