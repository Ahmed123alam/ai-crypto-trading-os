"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server
    FASTAPI_HOST: str = "0.0.0.0"
    FASTAPI_PORT: int = 8000
    WORKERS: int = 4
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/crypto_trading"
    MONGODB_URL: str = "mongodb://localhost:27017/crypto_trading"
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Exchange APIs
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    BYBIT_API_KEY: str = ""
    BYBIT_API_SECRET: str = ""
    OKX_API_KEY: str = ""
    OKX_API_SECRET: str = ""
    
    # AI Models
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    CLAUDE_API_KEY: str = ""
    
    # Data Providers
    WHALE_ALERT_API_KEY: str = ""
    GLASSNODE_API_KEY: str = ""
    COINGECKO_API_KEY: str = ""
    
    # Trading
    MAX_DAILY_DRAWDOWN: float = 0.10
    MAX_POSITION_SIZE: float = 0.05
    LEVERAGE_LIMIT: int = 3
    RISK_PER_TRADE: float = 0.02
    
    # Feature Flags
    ENABLE_PAPER_TRADING: bool = True
    ENABLE_LIVE_TRADING: bool = False
    ENABLE_BACKTESTING: bool = True
    ENABLE_AI_AGENTS: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
