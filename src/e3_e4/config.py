"""Configuration management using pydantic-settings."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = "CollibrIA"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = Field(default=True, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: Literal["console", "json"] = Field(
        default="console", description="Log output format"
    )

    # AWS settings (will be populated later)
    aws_region: str = Field(default="eu-west-3", description="AWS region")
    aws_access_key_id: str | None = Field(default=None, description="AWS access key")
    aws_secret_access_key: str | None = Field(default=None, description="AWS secret key")

    # Database settings (for local development)
    database_host: str = Field(default="localhost", description="MySQL host")
    database_port: int = Field(default=3306, description="MySQL port")
    database_name: str = Field(default="test_db", description="Database name")
    database_user: str = Field(default="root", description="Database user")
    database_password: str = Field(default="", description="Database password")

    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=True, description="Enable auto-reload")

    # Bedrock settings (will be populated later)
    bedrock_model_id: str = Field(
        default="mistral.mistral-large-2407-v1:0",
        description="Bedrock model ID",
    )
    bedrock_max_tokens: int = Field(default=2048, description="Max tokens for response")
    bedrock_temperature: float = Field(default=0.1, description="Model temperature")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v_upper

    @property
    def database_url(self) -> str:
        """Construct MySQL database URL."""
        return (
            f"mysql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience function for tests
def get_test_settings(**kwargs) -> Settings:
    """Get settings instance for testing with overrides."""
    return Settings(**kwargs)
