"""
SQLite database models and session management for chat history
"""

from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

from config import settings

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    personality = Column(String, default="default")
    metadata = Column(Text, default="{}")  # JSON field for extra data

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    role = Column(String)  # 'user', 'assistant', 'system'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(Text, default="{}")  # JSON field for tokens, model, etc.

# Create engine and session
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Database utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_message(db, session_id: str, role: str, content: str, metadata: dict = None):
    """Save a chat message to the database"""
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        metadata=json.dumps(metadata or {})
    )
    db.add(message)
    db.commit()
    return message

def get_session_history(db, session_id: str, limit: int = None):
    """Get chat history for a session"""
    query = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at)
    
    if limit:
        # Get last N messages
        messages = query.all()
        return messages[-limit:] if len(messages) > limit else messages
    
    return query.all()

def create_session(db, session_id: str, personality: str = "default"):
    """Create a new chat session"""
    session = ChatSession(
        id=session_id,
        personality=personality
    )
    db.add(session)
    db.commit()
    return session