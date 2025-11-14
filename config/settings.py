import os
from typing import Dict, List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration"""
    
    # Application
    APP_NAME: str = "Enterprise Risk Assessment Platform"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://user:pass@localhost/erp")
    
    # LLM Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "8192"))
    
    # Agent Configuration
    AGENT_TIMEOUT: int = int(os.getenv("AGENT_TIMEOUT", "600"))
    AGENT_RETRY_ATTEMPTS: int = int(os.getenv("AGENT_RETRY_ATTEMPTS", "3"))
    AGENT_RETRY_DELAY: int = int(os.getenv("AGENT_RETRY_DELAY", "5"))
    
    # API Configuration
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", "100"))
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    API_RETRY_ATTEMPTS: int = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
    
    # Data Retention
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # API Keys
    FRED_KEY: str = os.getenv("FRED_KEY", "")
    ALPHA_VANTAGE_KEY: str = os.getenv("ALPHA_VANTAGE_KEY", "")
    FINNHUB_KEY: str = os.getenv("FINNHUB_KEY", "")
    HIBP_KEY: str = os.getenv("HIBP_KEY", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()