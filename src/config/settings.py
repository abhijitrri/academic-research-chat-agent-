"""Settings and configuration management."""
from pydantic_settings import BaseSettings
from typing import Optional, Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider Configuration
    llm_provider: Literal["openai", "anthropic"] = "openai"

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"

    # Anthropic Configuration
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-opus-4-1"

    # Database
    database_url: str = "postgresql://research_user:research_pass@localhost:5432/research_agent_db"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Frontend
    frontend_url: str = "http://localhost:3000"

    # File Storage
    data_dir: str = "./data"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_active_api_key(self) -> str:
        """Get the active LLM API key based on provider."""
        if self.llm_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic")
            return self.anthropic_api_key
        return self.openai_api_key

    def get_active_model(self) -> str:
        """Get the active LLM model based on provider."""
        if self.llm_provider == "anthropic":
            return self.anthropic_model
        return self.openai_model


settings = Settings()
