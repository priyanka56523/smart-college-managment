from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent

# Load from demo1/.env, backend/.env, or cwd
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv(BASE_DIR / ".env")
load_dotenv(".env")


class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "Global AI & AGI News Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Storage
    DATABASE_URL: str = Field(default=f"sqlite:///{BASE_DIR / 'ai_news_intelligence.db'}")
    
    # NewsAPI Integration
    NEWSAPI_API_KEY: str = Field(default="")
    NEWSAPI_BASE_URL: str = "https://newsapi.org/v2"
    
    # NVIDIA Hosted LLM API
    NVIDIA_API_KEY: str = Field(default="")
    NVIDIA_BASE_URL: str = Field(default="https://integrate.api.nvidia.com/v1")
    NVIDIA_MODEL: str = Field(default="meta/llama-3.1-70b-instruct")
    
    # Additional Source Adapters
    ARXIV_ENABLED: bool = True
    GITHUB_ENABLED: bool = True
    OFFICIAL_FEEDS_ENABLED: bool = True
    SEARCH_ENABLED: bool = True
    
    # Scheduler Settings
    SCHEDULER_ENABLED: bool = True
    SCHEDULER_INTERVAL_HOURS: int = 6
    
    # Safety and Ingestion limits
    MAX_ARTICLES_PER_RUN: int = 40
    REQUEST_TIMEOUT_SECONDS: int = 15
    MAX_RETRIES: int = 3
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
