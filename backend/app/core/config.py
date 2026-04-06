from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url:     str = "postgresql+asyncpg://user:pass@localhost/retail_insights"
    redis_url:        str = "redis://localhost:6379"
    secret_key:       str = "change-me-in-production"
    allowed_origins:  List[str] = ["http://localhost:3000", "http://localhost:5173", "https://retail-insights-th4a.vercel.app"]
    anthropic_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
