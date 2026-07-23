"""
=========================================================
TechStore Universal Super-System v3
settings.py
=========================================================

Purpose:
    Central configuration for the entire application.

Author:
    Declan

Architecture:
    TechStore Universal Super-System v3

This file manages:

• Application Information
• Global Constants
• Folder Paths
• Environment Configuration
• AI Configuration
• Database Configuration
• Security Configuration
• Performance Configuration
• Upload Configuration
• Feature Flags
• Logging
"""

# ==========================================================
# IMPORTS
# ==========================================================

from pathlib import Path
import os
from datetime import timedelta

try:
    import streamlit as st
except ImportError:
    st = None


# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

APP_NAME = "TechStore Universal Super-System"

APP_VERSION = "3.0.0"

APP_BUILD = "Build 001"

AUTHOR = "Declan"

COMPANY = "TechStore AI"

COPYRIGHT = "© 2026 TechStore AI"

DEBUG_MODE = True


# ==========================================================
# ROOT DIRECTORY
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent


# ==========================================================
# PROJECT FOLDERS
# ==========================================================

ASSETS_DIR = ROOT_DIR / "assets"

UPLOADS_DIR = ROOT_DIR / "uploads"

PROJECTS_DIR = ROOT_DIR / "projects"

BACKUPS_DIR = ROOT_DIR / "backups"

PLUGINS_DIR = ROOT_DIR / "plugins"

DATABASE_DIR = ROOT_DIR / "database"

LOGS_DIR = ROOT_DIR / "logs"

CACHE_DIR = ROOT_DIR / "cache"


# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================

REQUIRED_DIRECTORIES = [

    ASSETS_DIR,
    UPLOADS_DIR,
    PROJECTS_DIR,
    BACKUPS_DIR,
    PLUGINS_DIR,
    DATABASE_DIR,
    LOGS_DIR,
    CACHE_DIR,

]

for folder in REQUIRED_DIRECTORIES:
    folder.mkdir(parents=True, exist_ok=True)


# ==========================================================
# DATABASE FILE
# ==========================================================

DATABASE_FILE = DATABASE_DIR / "techstore.db"


# ==========================================================
# CACHE FILES
# ==========================================================

CACHE_DATABASE = CACHE_DIR / "cache.db"

MEMORY_DATABASE = CACHE_DIR / "memory.db"


# ==========================================================
# LOG FILES
# ==========================================================

SYSTEM_LOG = LOGS_DIR / "system.log"

ERROR_LOG = LOGS_DIR / "errors.log"

PERFORMANCE_LOG = LOGS_DIR / "performance.log"


# ==========================================================
# SESSION SETTINGS
# ==========================================================

SESSION_TIMEOUT = timedelta(hours=2)

MAX_CHAT_HISTORY = 500

MAX_MEMORY_RECORDS = 5000


# ==========================================================
# END OF SECTION 1
# ==========================================================

# ==========================================================
# ENVIRONMENT & SECRETS
# ==========================================================

# Environment Name
ENVIRONMENT = os.getenv("APP_ENV", "development")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET_KEY")

ENABLE_STREAMLIT_SECRETS = st is not None

# ==========================================================
# API KEY LOADER
# ==========================================================

def get_secret(key: str, default: str = "") -> str:
    """
    Load configuration securely.

    Priority:
    1. Streamlit Secrets
    2. Environment Variables
    3. Default Value
    """

    if ENABLE_STREAMLIT_SECRETS:
        try:
            return st.secrets[key]
        except Exception:
            pass

    return os.getenv(key, default)


# ==========================================================
# AI PROVIDER API KEYS
# ==========================================================

XAI_API_KEY = get_secret("XAI_API_KEY")

GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

GROQ_API_KEY = get_secret("GROQ_API_KEY")

OPENAI_API_KEY = get_secret("OPENAI_API_KEY")

CLAUDE_API_KEY = get_secret("CLAUDE_API_KEY")

DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")

MISTRAL_API_KEY = get_secret("MISTRAL_API_KEY")

ELEVENLABS_API_KEY = get_secret("ELEVENLABS_API_KEY")

TAVILY_API_KEY = get_secret("TAVILY_API_KEY")

FACE_SWAP_API_KEY = get_secret("FACE_SWAP_API_KEY")

VOICE_CLONE_API_KEY = get_secret("VOICE_CLONE_API_KEY")

VIDEO_GENERATOR_API_KEY = get_secret("VIDEO_GENERATOR_API_KEY")


# ==========================================================
# SECURITY CONFIGURATION
# ==========================================================

PASSWORD_HASH_ALGORITHM = "bcrypt"

MAX_LOGIN_ATTEMPTS = 5

ACCOUNT_LOCKOUT_MINUTES = 30

SESSION_COOKIE_NAME = "techstore_session"

SESSION_SECURE = True

SESSION_HTTPONLY = True

SESSION_SAMESITE = "Lax"

ENABLE_CSRF_PROTECTION = True


# ==========================================================
# RATE LIMITING
# ==========================================================

RATE_LIMIT_ENABLED = True

MAX_REQUESTS_PER_MINUTE = 60

MAX_AI_REQUESTS_PER_HOUR = 500

MAX_FILE_UPLOADS_PER_HOUR = 100


# ==========================================================
# USER SESSION
# ==========================================================

AUTO_LOGOUT_MINUTES = 120

REMEMBER_LOGIN_DAYS = 30

DEFAULT_USER_ROLE = "user"


# ==========================================================
# END OF SECTION 2
# ==========================================================
