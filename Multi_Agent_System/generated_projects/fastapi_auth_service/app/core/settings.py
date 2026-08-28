import os
from pathlib import Path
from typing import Literal

from pydantic import BaseSettings, Field, EmailStr, validator
from dotenv import load_dotenv

# Load environment variables from a .env file located at the project root.
BASE_DIR = Path(__file__).resolve().parents[2]
dotenv_path = BASE_DIR / ".env"
if dotenv_path.is_file():
    load_dotenv(dotenv_path)


class Settings(BaseSettings):
    # Database
    DB_URL: str = Field(..., env="DB_URL", description="SQLAlchemy async database URL")

    # JWT configuration
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY", description="Secret key for signing JWTs")
    JWT_ALGORITHM: Literal["HS256", "HS384", "HS512"] = Field(
        "HS256", env="JWT_ALGORITHM", description="Algorithm used for JWT encoding"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        15, env="ACCESS_TOKEN_EXPIRE_MINUTES", description="Access token TTL in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        7, env="REFRESH_TOKEN_EXPIRE_DAYS", description="Refresh token TTL in days"
    )

    # Email (SMTP) configuration
    EMAIL_HOST: str = Field(..., env="EMAIL_HOST", description="SMTP server host")
    EMAIL_PORT: int = Field(..., env="EMAIL_PORT", description="SMTP server port")
    EMAIL_USER: str = Field(..., env="EMAIL_USER", description="SMTP authentication user")
    EMAIL_PASSWORD: str = Field(..., env="EMAIL_PASSWORD", description="SMTP authentication password")
    EMAIL_FROM: EmailStr = Field(..., env="EMAIL_FROM", description="Default sender address")
    EMAIL_USE_TLS: bool = Field(True, env="EMAIL_USE_TLS", description="Use STARTTLS")
    EMAIL_USE_SSL: bool = Field(False, env="EMAIL_USE_SSL", description="Use SSL/TLS directly")

    # Rate limiting (SlowAPI format, e.g., "5/minute")
    RATE_LIMIT: str = Field("5/minute", env="RATE_LIMIT", description="Global rate limit for auth endpoints")

    # Misc
    PROJECT_NAME: str = Field("FastAPI Authentication Service", env="PROJECT_NAME")
    DEBUG: bool = Field(False, env="DEBUG")
    LOG_LEVEL: str = Field("info", env="LOG_LEVEL")

    @validator("JWT_ALGORITHM")
    def validate_algorithm(cls, v: str) -> str:
        allowed = {"HS256", "HS384", "HS512"}
        if v not in allowed:
            raise ValueError(f"JWT_ALGORITHM must be one of {allowed}")
        return v

    class Config:
        env_file = str(dotenv_path)
        env_file_encoding = "utf-8"
        case_sensitive = True


# Export a singleton instance that can be imported throughout the project.
settings = Settings()