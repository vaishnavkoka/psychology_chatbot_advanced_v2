"""
Configuration for Multi-API Psychology Chatbot  
Integrates 5 different API providers for redundancy and optimal performance
"""

import os
from dotenv import load_dotenv

load_dotenv()

# === 5 API KEYS CONFIGURATION ===
class APIKeys:
    """All 5 API keys for maximum flexibility and reliability"""
    
    # 1. GROQ - Primary Fast LLM
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODELS = [
        "llama-3.1-8b-instant",      # Fast routing and quick responses
        "llama-3.1-70b-versatile",   # Complex psychological reasoning
        "mixtral-8x7b-32768"         # Long context for detailed analysis
    ]
    GROQ_PRIMARY = "llama-3.1-8b-instant"
    GROQ_ADVANCED = "llama-3.1-70b-versatile"
    
    # 2. HUGGINGFACE - Embedding and Alternative Models
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    HF_ALTERNATIVE_MODELS = [
        "mistralai/Mistral-7B-Instruct-v0.1",
        "meta-llama/Llama-2-7b-chat"
    ]
    
    # 3. TAVILY - Web Research and Mental Health Resources
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    TAVILY_MONTHLY_LIMIT = 1000
    TAVILY_FREE_TIER = True
    
    # 4. SERPER - Alternative Search (Google Search API)
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    SERPER_MONTHLY_LIMIT = 2500
    SERPER_FREE_TIER = True
    
    # 5. COHERE - Alternative LLM and Reranking
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    COHERE_PRIMARY_MODEL = "command-light"
    COHERE_EMBEDDING_MODEL = "embed-english-v3.0"

# === MODEL CONFIGURATION ===
class ModelConfig:
    # Primary & Fallback LLMs
    PRIMARY_LLM = "groq::llama-3.1-8b-instant"
    ADVANCED_LLM = "groq::llama-3.1-70b-versatile"
    LONG_CONTEXT_LLM = "groq::mixtral-8x7b-32768"
    
    FALLBACK_LLMS = [
        "cohere::command-light",
        "huggingface::mistralai/Mistral-7B-Instruct-v0.1"
    ]
    
    # Specialized Models
    CRISIS_DETECTION_MODEL = "groq::llama-3.1-70b-versatile"
    ASSESSMENT_SCORING_MODEL = "groq::llama-3.1-70b-versatile"
    THERAPY_SUPPORT_MODEL = "groq::llama-3.1-8b-instant"
    
    # Embedding Models
    PRIMARY_EMBEDDING = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # For compatibility
    BACKUP_EMBEDDINGS = [
        "sentence-transformers/all-mpnet-base-v2",
        "cohere::embed-english-v3.0"
    ]

# === VECTOR STORE CONFIGURATION ===
class VectorConfig:
    FAISS_INDEX_PATH = "data/vector_store"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 5
    EMBEDDING_DIMENSION = 384

# === PSYCHOLOGY-SPECIFIC CONFIGURATION ===
class PsychologyConfig:
    # Supported Assessments
    SUPPORTED_ASSESSMENTS = {
        "phq9": {"name": "PHQ-9 Depression Screen", "questions": 9, "max_score": 27},
        "gad7": {"name": "GAD-7 Anxiety Screen", "questions": 7, "max_score": 21},
        "psqi": {"name": "Pittsburgh Sleep Quality Index", "questions": 7, "max_score": 21},
        "rosenberg_ses": {"name": "Rosenberg Self-Esteem Scale", "questions": 10, "max_score": 40},
        "pcl5": {"name": "PTSD Checklist-5", "questions": 20, "max_score": 80}
    }
    
    # Crisis Keywords
    CRISIS_KEYWORDS = {
        "suicidal": ["suicide", "kill myself", "end it", "want to die"],
        "self_harm": ["cut", "harm", "hurt myself"],
        "severe": ["emergency", "danger", "hospital"]
    }
    
    # Therapeutic Techniques
    THERAPEUTIC_TECHNIQUES = [
        "cbt", "mindfulness", "dbt", "act", "emdr", "eft"
    ]
    
    # Session Management
    MAX_SESSION_LENGTH = 60  # minutes
    SESSION_TIMEOUT = 30  # minutes
    MAX_CONVERSATION_HISTORY = 50  # messages

# === DATABASE CONFIGURATION ===
class DatabaseConfig:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:////home/vaishnavkoka/RE4BDD/psychology_chatbot_advanced/psychology_chatbot.db"
    )

# === RATE LIMITING CONFIGURATION ===
class RateLimits:
    GROQ_DAILY_LIMIT = 25000
    GROQ_REQUESTS_PER_MINUTE = 30
    SERPER_MONTHLY_LIMIT = 2500
    TAVILY_MONTHLY_LIMIT = 1000
    HF_MONTHLY_LIMIT = 950
    COHERE_MONTHLY_LIMIT = 1000

# === FEATURE TOGGLES ===
class FeatureFlags:
    ENABLE_CRISIS_DETECTION = True
    ENABLE_ASSESSMENTS = True
    ENABLE_MULTI_AGENT_ORCHESTRATION = True
    ENABLE_REPORT_GENERATION = True
    ENABLE_VECTOR_SEARCH = True

# === REPORT CONFIGURATION ===
class ReportConfig:
    REPORT_OUTPUT_DIR = "generated_reports"
    SUPPORT_PDF = True
    SUPPORT_JSON = True
    SUPPORT_CSV = True
    MAX_REPORT_SIZE_MB = 10

# === SECURITY CONFIGURATION ===
class SecurityConfig:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "psychology-chatbot-secret")
    CORS_ORIGINS = ["http://localhost:8501", "http://localhost:8000"]

# === LOGGING CONFIGURATION ===
class LoggingConfig:
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "logs/psychology_chatbot.log"

# === THERAPY SETTINGS ===
class TherapySettings:
    EMPATHY_LEVEL = "high"
    CONFIDENTIALITY_REMINDER = True
    PRIVACY_NOTICE_INTERVAL = 3
    SESSION_LENGTH = 3600  # seconds
    FOLLOW_UP_INTERVAL = 86400  # 24 hours
    MAX_CONCURRENT_SESSIONS = 5
