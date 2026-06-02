# config.py
# All environment configuration in one place
# Uses python-dotenv to load from .env file

import os
from dotenv import load_dotenv

# Load .env file into environment variables
# This must be called before accessing os.getenv()
load_dotenv()


class Settings:
    """
    Central configuration class.

    All settings come from environment variables.
    This means we can change settings without changing code.
    Different values for development, staging, production.

    Never hardcode secrets like passwords or API keys in code!
    """

    # ─── Oracle Database ───────────────────────────────────────
    DB_USER: str = os.getenv("DB_USER", "system")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "oracle")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "1521")
    DB_SERVICE: str = os.getenv("DB_SERVICE", "XE")

    # ─── JWT Authentication ────────────────────────────────────
    # IMPORTANT: Change SECRET_KEY in production to a long random string
    # Generate one with: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-to-a-long-random-secret-key-in-production"
    )
    ALGORITHM: str = "HS256"  # HMAC SHA-256 — standard and secure

    # Token expires after 24 hours (1440 minutes)
    # Employee stays logged in for 24 hours without needing to re-login
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
    )

    # ─── App Settings ──────────────────────────────────────────
    APP_NAME: str = "Performance Review Portal"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))


# Create a single instance
# Import this everywhere: from config import settings
settings = Settings()