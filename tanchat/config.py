"""
Configuration for Tangnet Chat System
Easily swap between local Pi and future 3080 GPU server
"""

from enum import Enum
from pydantic_settings import BaseSettings

class ModelServer(str, Enum):
    LOCAL_PI = "local_pi"
    REMOTE_3080 = "remote_3080"
    OLLAMA = "ollama"
    VLLM = "vllm"

class Settings(BaseSettings):
    # Current active server
    active_server: ModelServer = ModelServer.LOCAL_PI
    
    # Server configurations
    local_pi_url: str = "http://192.168.1.31:8080"
    remote_3080_url: str = "http://192.168.1.32:8001"  # Future 3080 server
    ollama_url: str = "http://localhost:11434"
    vllm_url: str = "http://localhost:8000"
    
    # Model configurations
    local_pi_model: str = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    remote_3080_model: str = "mistral-7b-instruct"  # Future upgrade
    
    # API settings
    api_timeout: int = 120
    max_tokens: int = 2048
    temperature: float = 0.7
    
    # Database
    database_url: str = "sqlite:///./tanchat.db"
    
    # Chat settings
    context_window: int = 4096
    max_history_messages: int = 20
    
    class Config:
        env_file = ".env"

settings = Settings()