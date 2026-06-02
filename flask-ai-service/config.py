import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER = os.getenv("DB_USER", "SYSTEM")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "hr")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "1521")
    DB_SERVICE = os.getenv("DB_SERVICE", "XE")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

config = Config()