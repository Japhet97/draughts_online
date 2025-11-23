from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Draughts Online Gaming Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./draughts.db"
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # PayChangu Payment Gateway
    PAYCHANGU_API_KEY: str = "test_key"
    PAYCHANGU_SECRET_KEY: str = "test_secret"
    PAYCHANGU_CALLBACK_URL: str = "http://localhost:8080/api/v1/payments/callback"
    PAYCHANGU_BASE_URL: str = "https://api.paychangu.com/v1"
    
    # Game Settings
    COMMISSION_RATE: float = 0.10  # 10% commission
    MIN_BET_AMOUNT: float = 1.00
    MAX_BET_AMOUNT: float = 10000.00
    
    # AI Difficulty Levels
    AI_DIFFICULTY_LEVELS: dict = {
        "easy": {"depth": 2, "rating": 800},
        "medium": {"depth": 4, "rating": 1200},
        "hard": {"depth": 6, "rating": 1600},
        "expert": {"depth": 8, "rating": 2000}
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
