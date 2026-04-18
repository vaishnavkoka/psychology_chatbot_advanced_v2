"""
LangGraph-based Psychology Agent Orchestrator
Manages multi-agent coordination for comprehensive mental health support
"""

import json
import logging
from typing import Dict, List, Optional, Any, TypedDict, Annotated
from datetime import datetime
import time
import asyncio

# LangGraph imports
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

# Import all agents
from agents.assessment_agent import AssessmentAgent
from agents.crisis_detection_agent import CrisisDetectionAgent, RiskLevel
from agents.therapeutic_support_agent import TherapeuticSupportAgent
from agents.insights_agent import InsightsAgent
from agents.query_router_agent import QueryRouterAgent
from agents.rag_agent import RAGAgent

# LLM imports
from langchain_groq import ChatGroq
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PsychologyAgentWorkflowState(TypedDict):
    """State definition for psychology agent orchestration workflow"""
    
    # Input and context
    messages: List[BaseMessage]
    original_query: str
    user_id: str
    conversation_history: List[Dict[str, str]]
    
    # Query analysis
    query_intent: str
    query_complexity: str  # simple, moderate, complex
    required_agents: List[str]
    agent_priorities: Dict[str, float]
    
    # Crisis detection
    crisis_detected: bool
    risk_level: str
    crisis_indicators: List[str]
    
    # Agent execution state
    active_agents: List[str]
    agent_results: Dict[str, Any]
    agent_errors: Dict[str, str]
    execution_metadata: Dict[str, Any]
    
    # Assessment tracking
    assessment_in_progress: Optional[str]
    assessment_responses: Dict[str, List[Any]]
    assessment_results: Optional[Dict[str, Any]]
    
    # Final output
    synthesized_result: Optional[Dict[str, Any]]
    final_response: str
    recommended_actions: List[str]
    confidence_score: float


class AssessmentResponse:
    """Structure for assessment responses"""
    def __init__(self, assessment_type: str, score: int, interpretation: str, recommendations: List[str]):
        self.assessment_type = assessment_type
        self.score = score
        self.interpretation = interpretation
        self.recommendations = recommendations


class LangGraphPsychologyOrchestrator:
    """
    Advanced LangGraph-based orchestrator for Psychology Chatbot

    Coordinates multiple specialized agents to provide comprehensive mental health support
    including assessments, crisis response, therapy support, and resource connection.
    """
    
    def __init__(self):
        logger.info("Initializing LangGraph Psychology Orchestrator...")
        
        # Initialize LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=os.getenv('GROQ_API_KEY')
        )
        
        # Initialize specialized agents
        self._initialize_agents()
        
        # Build and compile LangGraph workflow
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
        logger.info("✅ LangGraph Psychology Orchestrator initialized with 6 specialized agents!")

    def _initialize_agents(self):
        """Initialize all specialized psychology agents"""
        self.agents = {
            'query_router': self._create_query_router(),
            'assessment': self._create_assessment_agent(),
            'crisis_response': self._create_crisis_response_agent(),
            'therapy_support': self._create_therapy_support_agent(),
            'resource_finder': self._create_resource_finder_agent(),
            'rag': self._create_rag_agent()
        }
        logger.info("✅ All 6 psychology agents initialized")

    def _create_query_router(self):
        """Create query router agent for intent detection"""
        return {
            'name': 'QueryRouter',
            'description': 'Analyzes user query to detect intent and mental health needs',
            'model': self.llm
        }

    def _create_assessment_agent(self):
        """Create assessment agent"""
        return {
            'name': 'AssessmentAgent',
            'description': 'Conducts psychological assessments (PHQ-9, GAD-7, etc.)',
            'model': self.llm
        }

    def _create_crisis_response_agent(self):
        """Create crisis response agent"""
        return {
            'name': 'CrisisResponse',
            'description': 'Handles crisis situations with immediate support and resources',
            'model': self.llm
        }

    def _create_therapy_support_agent(self):
        """Create therapy support agent"""
        return {
            'name': 'TherapySupport',
            'description': 'Provides emotional support and coping strategies',
            'model': self.llm
        }

    def _create_resource_finder_agent(self):
        """Create resource finder agent"""
        return {
            'name': 'ResourceFinder',
            'description': 'Finds and connects users with mental health resources',
            'model': self.llm
        }

    def _create_rag_agent(self):
        """Create RAG agent for knowledge retrieval"""
        return {
            'name': 'RAG',
            'description': 'Retrieves relevant psychology knowledge and best practices',
            'model': self.llm
        }

    def _build_workflow(self) -> StateGraph:
        """Build the comprehensive LangGraph workflow for psychology agent orchestration"""
        
        workflow = StateGraph(PsychologyAgentWorkflowState)
        
        # === WORKFLOW NODES ===
        
        # 1. Initial Analysis Phase
        workflow.add_node("analyze_query", self._analyze_query_intent)
        workflow.add_node("detect_crisis", self._detect_crisis)
        workflow.add_node("determine_agents", self._determine_required_agents)
        
        # 2. Crisis Response Phase (highest priority)
        workflow.add_node("handle_crisis", self._handle_crisis)
        
        # 3. Assessment Phase
        workflow.add_node("conduct_assessment", self._conduct_assessment)
        
        # 4. Support Phase
        workflow.add_node("provide_therapy_support", self._provide_therapy_support)
        
        # 5. Resource Phase
        workflow.add_node("find_resources", self._find_resources)
        
        # 6. Knowledge Retrieval Phase
        workflow.add_node("retrieve_knowledge", self._retrieve_knowledge)
        
        # 7. Synthesis Phase
        workflow.add_node("synthesize_results", self._synthesize_results)
        workflow.add_node("generate_final_response", self._generate_final_response)
        
        # === WORKFLOW EDGES ===
        
        # Entry point
        workflow.set_entry_point("analyze_query")
        
        # Initial analysis flow
        workflow.add_edge("analyze_query", "detect_crisis")
        workflow.add_edge("detect_crisis", "determine_agents")
        
        # Crisis routing (highest priority)
        workflow.add_conditional_edges(
            "determine_agents",
            self._route_based_on_crisis,
            {
                "crisis_response": "handle_crisis",
                "normal_flow": "conduct_assessment"
            }
        )
        
        # Crisis flow leads directly to synthesis
        workflow.add_edge("handle_crisis", "synthesize_results")
        
        # Assessment flow
        workflow.add_conditional_edges(
            "conduct_assessment",
            self._route_after_assessment,
            {
                "to_support": "provide_therapy_support",
                "to_resources": "find_resources",
                "to_synthesis": "synthesize_results"
            }
        )
        
        # Support and resource flows
        workflow.add_edge("provide_therapy_support", "retrieve_knowledge")
        workflow.add_edge("find_resources", "retrieve_knowledge")
        workflow.add_edge("retrieve_knowledge", "synthesize_results")
        
        # Final synthesis and response generation
        workflow.add_edge("synthesize_results", "generate_final_response")
        workflow.add_edge("generate_final_response", END)
        
        return workflow

    # === WORKFLOW NODES ===

    async def _analyze_query_intent(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Analyze user query to understand intent and mental health needs"""
        logger.info("🔍 Analyzing query intent...")
        
        try:
            query = state["original_query"]
            
            analysis_prompt = f"""
            Analyze this mental health query to understand user intent and needs:
            
            Query: "{query}"
            
            Provide analysis as JSON:
            {{
                "primary_intent": "assessment|support|crisis|resources|information|general_chat",
                "secondary_intents": ["intent1", "intent2"],
                "complexity": "simple|moderate|complex",
                "mental_health_focus": ["anxiety", "depression", "stress", "trauma", "other"],
                "urgency": "low|medium|high|critical",
                "requires_assessment": true|false,
                "requires_professional_help": true|false
            }}
            
            Intent Definitions:
            - assessment: User wants to take a psychological assessment
            - support: User needs emotional support or coping strategies
            - crisis: User is in immediate crisis or danger
            - resources: User needs mental health resources or referrals
            - information: User wants information about mental health
            - general_chat: General conversation or non-specific needs
            """
            
            response = self.llm.invoke([HumanMessage(content=analysis_prompt)])
            
            # Parse response
            try:
                analysis = json.loads(response.content)
            except json.JSONDecodeError:
                logger.warning("JSON parsing failed, using fallback analysis")
                analysis = {
                    "primary_intent": "general_chat",
                    "secondary_intents": [],
                    "complexity": "simple",
                    "mental_health_focus": [],
                    "urgency": "low",
                    "requires_assessment": False,
                    "requires_professional_help": False
                }
            
            # Update state
            state["query_intent"] = analysis.get("primary_intent", "general_chat")
            state["query_complexity"] = analysis.get("complexity", "simple")
            state["execution_metadata"] = {
                "analysis": analysis,
                "analyzed_at": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Query Analysis: Intent={analysis['primary_intent']}, Urgency={analysis.get('urgency', 'low')}")
            
        except Exception as e:
            logger.error(f"❌ Query analysis failed: {e}")
            state["query_intent"] = "general_chat"
            state["query_complexity"] = "simple"
            state["execution_metadata"] = {"analysis_error": str(e)}
        
        return state

    async def _detect_crisis(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Detect if user is in crisis based on query content"""
        logger.info("🚨 Performing crisis detection...")
        
        query = state["original_query"].lower()
        
        # Crisis indicators
        crisis_keywords = {
            "suicidal": ["suicide", "kill myself", "end it", "want to die", "no point living", "better off dead"],
            "self_harm": ["cut myself", "harm myself", "hurt myself", "self injury"],
            "severe_distress": ["can't breathe", "panic", "spiraling", "breakdown"],
            "abuse": ["being abused", "domestic violence", "assault", "attacked"],
            "overdose": ["overdose", "poison", "pills"]
        }
        
        detected_indicators = []
        for category, keywords in crisis_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    detected_indicators.append(keyword)
                    break
        
        # Determine risk level
        if len(detected_indicators) > 0:
            state["crisis_detected"] = True
            state["risk_level"] = "HIGH_RISK" if "suicidal" in [k for indicators in crisis_keywords.values() for k in indicators if any(k in query for item in detected_indicators for ik in query)] else "MODERATE_RISK"
        else:
            state["crisis_detected"] = False
            state["risk_level"] = "NO_RISK"
        
        state["crisis_indicators"] = detected_indicators
        
        if state["crisis_detected"]:
            logger.warning(f"⚠️ CRISIS DETECTED: Risk Level = {state['risk_level']}, Indicators: {detected_indicators}")
        else:
            logger.info("✅ No crisis indicators detected")
        
        return state

    async def _determine_required_agents(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Determine which agents are required based on query analysis"""
        logger.info("🎯 Determining required agents...")
        
        query = state["original_query"].lower()
        intent = state["query_intent"]
        crisis_detected = state["crisis_detected"]
        
        required_agents = []
        priorities = {}
        
        # === AGENT SELECTION LOGIC ===
        
        # 1. Crisis Response Agent (ALWAYS first if crisis detected)
        if crisis_detected:
            required_agents.append("crisis_response")
            priorities["crisis_response"] = 1.0  # Highest priority
            logger.info("🚨 Crisis Response Agent selected (CRITICAL)")
        
        # 2. Assessment Agent
        if intent == "assessment" or any(kw in query for kw in ["assessment", "test", "quiz", "evaluate", "screen"]):
            required_agents.append("assessment")
            priorities["assessment"] = 0.9
            logger.info("📋 Assessment Agent selected")
        
        # 3. Therapy Support Agent
        if intent in ["support", "help", "general_chat"] or any(kw in query for kw in ["help", "support", "struggling", "advice", "coping"]):
            required_agents.append("therapy_support")
            priorities["therapy_support"] = 0.8
            logger.info("💬 Therapy Support Agent selected")
        
        # 4. Resource Finder Agent
        if intent == "resources" or any(kw in query for kw in ["resources", "therapist", "counselor", "hospital", "clinic", "help"]):
            required_agents.append("resource_finder")
            priorities["resource_finder"] = 0.8
            logger.info("🔗 Resource Finder Agent selected")
        
        # 5. RAG Agent (for knowledge retrieval)
        if intent in ["information", "general_chat"] or any(kw in query for kw in ["what is", "how to", "tell me about", "explain"]):
            required_agents.append("rag")
            priorities["rag"] = 0.7
            logger.info("📚 RAG Agent selected")
        
        # Default to therapy support if no agents selected
        if not required_agents:
            required_agents = ["therapy_support"]
            priorities["therapy_support"] = 0.7
            logger.info("📋 Default: Therapy Support Agent selected")
        
        # Update state
        state["required_agents"] = required_agents
        state["agent_priorities"] = priorities
        state["active_agents"] = []
        state["agent_results"] = {}
        state["agent_errors"] = {}
        
        logger.info(f"✅ Selected {len(required_agents)} agents: {required_agents}")
        
        return state

    def _route_based_on_crisis(self, state: PsychologyAgentWorkflowState) -> str:
        """Route to crisis handling if crisis detected"""
        if state["crisis_detected"]:
            logger.info("🚨 Routing to CRISIS RESPONSE (highest priority)")
            return "crisis_response"
        else:
            logger.info("✅ Routing to normal assessment flow")
            return "normal_flow"

    async def _handle_crisis(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Handle crisis situation with immediate response"""
        logger.warn("🚨 CRISIS HANDLER ACTIVATED")
        
        crisis_response = {
            "crisis_detected": True,
            "immediate_action": "PROVIDE EMERGENCY RESOURCES",
            "resources": [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/",
                "Local Emergency Services: 911"
            ],
            "supportive_message": "I'm really concerned about your safety, and I want you to know that help is available right now. Please reach out to one of these emergency services immediately."
        }
        
        state["agent_results"]["crisis_response"] = crisis_response
        state["recommended_actions"] = ["IMMEDIATE: Contact emergency services", "IMMEDIATE: Reach out to crisis helpline"]
        
        return state

    async def _conduct_assessment(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Conduct psychological assessment if needed"""
        logger.info("📋 Conducting psychological assessment...")
        
        # Placeholder for assessment execution
        state["assessment_in_progress"] = "PHQ-9"
        state["agent_results"]["assessment"] = {
            "assessment_type": "PHQ-9",
            "status": "ready",
            "message": "I'd like to help you understand your mood better. Let's do a quick assessment."
        }
        
        return state

    async def _provide_therapy_support(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Provide therapeutic support"""
        logger.info("💬 Providing therapeutic support...")
        
        # Placeholder for therapy support
        state["agent_results"]["therapy_support"] = {
            "support_type": "general",
            "strategies": ["breathing_exercise", "grounding_technique", "cognitive_reframing"],
            "focus": "Building resilience and coping skills"
        }
        
        return state

    async def _find_resources(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Find mental health resources"""
        logger.info("🔗 Finding mental health resources...")
        
        state["agent_results"]["resource_finder"] = {
            "resource_types": ["therapists", "support_groups", "crisis_lines", "apps"],
            "status": "resources located"
        }
        
        return state

    async def _retrieve_knowledge(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Retrieve relevant psychology knowledge"""
        logger.info("📚 Retrieving psychology knowledge...")
        
        state["agent_results"]["rag"] = {
            "knowledge_base": "psychology_knowledge_base",
            "status": "knowledge retrieved"
        }
        
        return state

    def _route_after_assessment(self, state: PsychologyAgentWorkflowState) -> str:
        """Route after assessment based on results"""
        # Simple routing logic - can be enhanced
        return "to_support"

    async def _synthesize_results(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Synthesize results from all agents"""
        logger.info("🔄 Synthesizing agent results...")
        
        # Combine all agent results
        synthesized = {
            "agents_executed": list(state["agent_results"].keys()),
            "results": state["agent_results"],
            "crisis_handled": state["crisis_detected"],
            "recommended_next_steps": state.get("recommended_actions", [])
        }
        
        state["synthesized_result"] = synthesized
        
        return state

    async def _generate_final_response(self, state: PsychologyAgentWorkflowState) -> PsychologyAgentWorkflowState:
        """Generate final response to user using LLM"""
        logger.info("📝 Generating final response using LLM...")
        
        # Build comprehensive response using LLM for contextual answers
        response_parts = []
        
        # Build context from agent results
        agent_context = []
        if state["crisis_detected"]:
            crisis_info = state["agent_results"].get("crisis_response", {})
            supportive_msg = crisis_info.get("supportive_message", "I'm here to help.")
            response_parts.append(supportive_msg)
            resources = crisis_info.get("resources", [])
            if resources:
                response_parts.append("\n\nEMERGENCY RESOURCES:\n" + "\n".join(resources))
        else:
            # Build agent context for LLM
            if "therapy_support" in state["agent_results"]:
                agent_context.append("User is seeking emotional support and coping strategies")
            
            if "assessment" in state["agent_results"]:
                agent_context.append("User may benefit from a psychological assessment")
            
            if "resource_finder" in state["agent_results"]:
                agent_context.append("Professional resources are available for recommendations")
            
            # Use LLM to generate contextual response if we have agent results
            if agent_context or state["agent_results"]:
                try:
                    context_str = ". ".join(agent_context) if agent_context else ""
                    
                    # Create prompt for LLM
                    system_prompt = """You are a compassionate mental health support assistant. 
Generate a warm, empathetic response to the user's message. The response should:
1. Validate their feelings
2. Offer specific support or suggestions based on their needs
3. Be conversational and natural, not robotic
4. Suggest appropriate next steps if needed
Keep the response concise (2-3 sentences maximum)."""
                    
                    user_context = f"User said: {state['original_query']}"
                    if context_str:
                        user_context += f"\nContext: {context_str}"
                    
                    messages = [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=user_context)
                    ]
                    
                    response = self.llm.invoke(messages)
                    final_response = response.content.strip()
                    
                    logger.info(f"✅ LLM generated response: {final_response[:80]}...")
                    response_parts.append(final_response)
                except Exception as e:
                    logger.error(f"❌ LLM generation failed: {e}")
                    # Fallback to template if LLM fails
                    response_parts.append("I'm here to listen and support you. Can you tell me more about what you're experiencing?")
        
        # Combine all response parts
        final_response = "\n".join(response_parts) if response_parts else "Thank you for sharing with me. How can I help you today?"
        
        state["final_response"] = final_response
        state["confidence_score"] = 0.85
        
        return state

    async def process_user_input(self, user_id: str, user_message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Process user input through the entire orchestration workflow"""
        
        logger.info(f"🤖 Processing input from user {user_id}: '{user_message}'")
        
        if conversation_history is None:
            conversation_history = []
        
        # Create initial state
        messages = [HumanMessage(content=user_message)]
        
        initial_state = PsychologyAgentWorkflowState(
            messages=messages,
            original_query=user_message,
            user_id=user_id,
            conversation_history=conversation_history,
            query_intent="",
            query_complexity="",
            required_agents=[],
            agent_priorities={},
            crisis_detected=False,
            risk_level="NO_RISK",
            crisis_indicators=[],
            active_agents=[],
            agent_results={},
            agent_errors={},
            execution_metadata={},
            assessment_in_progress=None,
            assessment_responses={},
            assessment_results=None,
            synthesized_result=None,
            final_response="",
            recommended_actions=[],
            confidence_score=0.0
        )
        
        # Execute workflow
        result = await self.app.ainvoke(initial_state)
        
        logger.info("✅ Workflow completed successfully")
        
        return {
            "user_id": user_id,
            "user_message": user_message,
            "response": result["final_response"],
            "crisis_detected": result["crisis_detected"],
            "risk_level": result["risk_level"],
            "agents_used": result["required_agents"],
            "recommended_actions": result["recommended_actions"],
            "confidence_score": result["confidence_score"],
            "metadata": result["execution_metadata"]
        }
