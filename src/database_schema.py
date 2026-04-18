"""
Database Schema for Psychology Chatbot
Defines SQLAlchemy models for persistent data storage
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

# Database configuration
DB_PATH = os.getenv("DB_PATH", "sqlite:///psychology_chatbot.db")
Base = declarative_base()
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================================
# DATABASE MODELS
# ============================================================

class User(Base):
    """User profile and preferences"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = relationship("Assessment", back_populates="user")
    sessions = relationship("ConversationSession", back_populates="user")
    crisis_events = relationship("CrisisEvent", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id})>"


class Assessment(Base):
    """Assessment administration records"""
    __tablename__ = "assessments"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    assessment_type = Column(String, index=True)  # phq9, gad7, psqi, rosenberg_ses, pcl5
    total_score = Column(Integer)
    max_score = Column(Integer)
    percentage = Column(Float)
    interpretation = Column(String)
    severity_level = Column(String)  # minimal, mild, moderate, severe, very_severe
    recommendations = Column(JSON)  # List of recommendations
    requires_professional_help = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    
    def __repr__(self):
        return f"<Assessment(type={self.assessment_type}, score={self.total_score})>"


class ConversationSession(Base):
    """Chat session history"""
    __tablename__ = "conversation_sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    topic = Column(String, nullable=True)  # anxiety, depression, stress, assessment, etc.
    summary = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    message_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ConversationSession(id={self.id}, topic={self.topic})>"


class Message(Base):
    """Individual messages in conversation"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("conversation_sessions.id"), index=True)
    role = Column(String)  # user or assistant
    content = Column(Text)
    agent_type = Column(String, nullable=True)  # assessment, support, insights, crisis, rag, router
    sentiment = Column(String, nullable=True)  # positive, neutral, negative
    crisis_detected = Column(Boolean, default=False)
    risk_level = Column(String, nullable=True)  # LOW, MODERATE, HIGH, CRITICAL
    message_metadata = Column(JSON, nullable=True)  # Any additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(role={self.role}, session_id={self.session_id})>"


class CrisisEvent(Base):
    """Crisis detection and response events"""
    __tablename__ = "crisis_events"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    risk_level = Column(String)  # LOW, MODERATE, HIGH, CRITICAL
    confidence = Column(Float)  # 0.0 to 1.0
    triggers_detected = Column(JSON)  # List of crisis keywords/phrases
    initial_response = Column(Text)
    resources_provided = Column(JSON)  # Emergency resources info
    escalated = Column(Boolean, default=False)
    escalation_method = Column(String, nullable=True)  # call, text, email, etc.
    resolution_notes = Column(Text, nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="crisis_events")
    
    def __repr__(self):
        return f"<CrisisEvent(risk_level={self.risk_level}, user_id={self.user_id})>"


class VectorStoreMetadata(Base):
    """Metadata about indexed documents in vector store"""
    __tablename__ = "vector_store_metadata"
    
    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, unique=True, index=True)
    source_file = Column(String)  # CSV, TXT file name
    content_type = Column(String)  # assessment_q, resource, guide, technique
    content_preview = Column(Text)
    embedding_model = Column(String)  # all-MiniLM-L6-v2
    indexed_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<VectorStoreMetadata(doc_id={self.document_id})>"


# ============================================================
# DATABASE UTILITIES
# ============================================================

def init_db():
    """Initialize database with all tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema initialized")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
