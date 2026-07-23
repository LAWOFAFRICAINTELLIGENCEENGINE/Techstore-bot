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

# ==========================================================
# AI MODEL CONFIGURATION
# ==========================================================

# Brain 1 (xAI)
XAI_MODEL = "grok-beta"

# Brain 2 (Google Gemini)
GEMINI_MODEL = "gemini-1.5-pro"

# Brain 3 (Groq)
GROQ_MODEL = "llama-3.3-70b-versatile"


# ==========================================================
# AI PROVIDERS
# ==========================================================

AI_PROVIDERS = {
    "xai": {
        "enabled": True,
        "model": XAI_MODEL,
        "priority": 1
    },
    "gemini": {
        "enabled": True,
        "model": GEMINI_MODEL,
        "priority": 2
    },
    "groq": {
        "enabled": True,
        "model": GROQ_MODEL,
        "priority": 3
    }
}


# ==========================================================
# 3-BRAIN COLLABORATION SETTINGS
# ==========================================================

ENABLE_AI_COLLABORATION = True

ENABLE_INTELLIGENT_ROUTING = True

ENABLE_FALLBACK = True

ENABLE_STREAMING = True

ENABLE_RESPONSE_ENHANCER = True

ENABLE_PROJECT_ANALYZER = True

ENABLE_CODE_VALIDATOR = True

ENABLE_SELF_HEALING = True

ENABLE_DIAGNOSTICS = True


# ==========================================================
# ROUTING RULES
# ==========================================================

AI_ROUTING = {

    "research": "xai",

    "reasoning": "xai",

    "planning": "gemini",

    "documents": "gemini",

    "images": "gemini",

    "coding": "groq",

    "debugging": "groq",

    "projects": "groq",

    "default": "groq"

}


# ==========================================================
# FALLBACK ORDER
# ==========================================================

FALLBACK_ORDER = [

    "groq",

    "gemini",

    "xai"

]


# ==========================================================
# IMAGE UNDERSTANDING
# ==========================================================

ENABLE_IMAGE_ANALYSIS = True

SUPPORTED_IMAGE_TYPES = [

    ".png",

    ".jpg",

    ".jpeg",

    ".webp"

]


# ==========================================================
# DOCUMENT ANALYSIS
# ==========================================================

ENABLE_DOCUMENT_ANALYSIS = True

SUPPORTED_DOCUMENTS = [

    ".pdf",

    ".docx",

    ".xlsx",

    ".csv",

    ".txt"

]


# ==========================================================
# WEB SEARCH
# ==========================================================

ENABLE_WEB_SEARCH = True

WEB_SEARCH_PROVIDER = "Tavily"


# ==========================================================
# AI RESPONSE SETTINGS
# ==========================================================

DEFAULT_TEMPERATURE = 0.2

DEFAULT_MAX_TOKENS = 8000

ENABLE_MARKDOWN = True

ENABLE_CODE_BLOCKS = True

ENABLE_RESPONSE_CACHE = True


# ==========================================================
# END OF SECTION 3
# ==========================================================

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

# Default database engine
DATABASE_ENGINE = "sqlite"      # Options: sqlite, postgresql

# SQLite database file
SQLITE_DATABASE = DATABASE_FILE

# PostgreSQL Configuration
POSTGRES_HOST = get_secret("POSTGRES_HOST", "localhost")

POSTGRES_PORT = int(get_secret("POSTGRES_PORT", "5432"))

POSTGRES_DATABASE = get_secret("POSTGRES_DATABASE", "techstore")

POSTGRES_USER = get_secret("POSTGRES_USER", "postgres")

POSTGRES_PASSWORD = get_secret("POSTGRES_PASSWORD", "")

# Connection Pool
DATABASE_POOL_SIZE = 10

DATABASE_TIMEOUT = 30

ENABLE_DATABASE_POOLING = True

AUTO_CREATE_DATABASE = True


# ==========================================================
# DATABASE TABLES
# ==========================================================

DATABASE_TABLES = [

    "users",

    "roles",

    "customers",

    "orders",

    "inventory",

    "chat_history",

    "conversation_memory",

    "response_cache",

    "system_logs",

    "performance_logs",

    "api_usage",

    "plugins"

]


# ==========================================================
# DATABASE BACKUP
# ==========================================================

ENABLE_DATABASE_BACKUP = True

DATABASE_BACKUP_DIRECTORY = BACKUPS_DIR

DATABASE_BACKUP_INTERVAL_HOURS = 24

MAX_DATABASE_BACKUPS = 30


# ==========================================================
# DATABASE SECURITY
# ==========================================================

ENABLE_DATABASE_ENCRYPTION = False

ENABLE_FOREIGN_KEYS = True

ENABLE_WAL_MODE = True

ENABLE_DATABASE_INDEXING = True


# ==========================================================
# DATABASE MIGRATIONS
# ==========================================================

ENABLE_AUTO_MIGRATION = True

DATABASE_SCHEMA_VERSION = "1.0.0"


# ==========================================================
# END OF SECTION 4
# ==========================================================

# ==========================================================
# CACHE CONFIGURATION
# ==========================================================

ENABLE_CACHE = True

CACHE_TYPE = "sqlite"

CACHE_EXPIRY_MINUTES = 60

CACHE_MAX_SIZE = 10000

CACHE_CLEANUP_INTERVAL = 30

CACHE_COMPRESS = True

CACHE_ENCRYPTION = False


# ==========================================================
# CONVERSATION MEMORY
# ==========================================================

ENABLE_MEMORY = True

MEMORY_TYPE = "sqlite"

MEMORY_RETENTION_DAYS = 365

MAX_CONVERSATIONS = 10000

MAX_MESSAGES_PER_CONVERSATION = 500

ENABLE_LONG_TERM_MEMORY = True

ENABLE_MEMORY_SUMMARIZATION = True


# ==========================================================
# PERFORMANCE MONITOR
# ==========================================================

ENABLE_PERFORMANCE_MONITOR = True

TRACK_CPU_USAGE = True

TRACK_MEMORY_USAGE = True

TRACK_RESPONSE_TIME = True

TRACK_API_USAGE = True

TRACK_DATABASE_PERFORMANCE = True

TRACK_CACHE_PERFORMANCE = True


# ==========================================================
# RESPONSE SETTINGS
# ==========================================================

DEFAULT_RESPONSE_TIMEOUT = 120

STREAM_RESPONSE_DELAY = 0

ENABLE_RESPONSE_STREAMING = True

ENABLE_RESPONSE_STATISTICS = True

MAX_RESPONSE_LENGTH = 100000


# ==========================================================
# BACKGROUND TASKS
# ==========================================================

ENABLE_BACKGROUND_TASKS = True

BACKGROUND_WORKERS = 4

TASK_RETRY_COUNT = 3

TASK_TIMEOUT_SECONDS = 300


# ==========================================================
# ASYNCHRONOUS PROCESSING
# ==========================================================

ENABLE_ASYNC_AI = True

ENABLE_ASYNC_DATABASE = True

ENABLE_ASYNC_UPLOADS = True

ENABLE_ASYNC_ANALYTICS = True


# ==========================================================
# PERFORMANCE LIMITS
# ==========================================================

MAX_CONCURRENT_USERS = 1000

MAX_SIMULTANEOUS_AI_REQUESTS = 200

MAX_UPLOAD_SIZE_MB = 500

REQUEST_QUEUE_SIZE = 1000


# ==========================================================
# SYSTEM OPTIMIZATION
# ==========================================================

AUTO_CLEAR_OLD_CACHE = True

AUTO_OPTIMIZE_DATABASE = True

AUTO_ROTATE_LOGS = True

AUTO_CLEAN_TEMP_FILES = True

SELF_HEALING_INTERVAL_MINUTES = 10


# ==========================================================
# END OF SECTION 5
# ==========================================================

# ==========================================================
# FILE UPLOAD CONFIGURATION
# ==========================================================

ENABLE_FILE_UPLOADS = True

UPLOAD_DIRECTORY = UPLOADS_DIR

MAX_UPLOAD_SIZE_MB = 500

ALLOW_MULTIPLE_UPLOADS = True

ALLOWED_FILE_TYPES = [
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".csv",
    ".xlsx",
    ".xls",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".bmp",
    ".mp3",
    ".wav",
    ".ogg",
    ".m4a",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm"
]


# ==========================================================
# IMAGE CONFIGURATION
# ==========================================================

ENABLE_IMAGE_PROCESSING = True

ENABLE_IMAGE_ANALYSIS = True

ENABLE_IMAGE_PREVIEW = True

ENABLE_IMAGE_RESIZE = True

MAX_IMAGE_WIDTH = 4096

MAX_IMAGE_HEIGHT = 4096


# ==========================================================
# DOCUMENT CONFIGURATION
# ==========================================================

ENABLE_DOCUMENT_PARSER = True

ENABLE_PDF_ANALYSIS = True

ENABLE_WORD_ANALYSIS = True

ENABLE_EXCEL_ANALYSIS = True

ENABLE_CSV_ANALYSIS = True

ENABLE_TEXT_ANALYSIS = True


# ==========================================================
# AUDIO CONFIGURATION
# ==========================================================

ENABLE_AUDIO_UPLOAD = True

ENABLE_VOICE_INPUT = True

ENABLE_VOICE_OUTPUT = True

ENABLE_AUDIO_TRANSCRIPTION = True

ENABLE_SPEECH_SYNTHESIS = True

SUPPORTED_AUDIO_FORMATS = [

    ".mp3",

    ".wav",

    ".ogg",

    ".m4a"

]


# ==========================================================
# VIDEO CONFIGURATION
# ==========================================================

ENABLE_VIDEO_UPLOAD = True

ENABLE_VIDEO_PROCESSING = True

ENABLE_VIDEO_ANALYSIS = True

ENABLE_VIDEO_PREVIEW = True

ENABLE_WEBCAM = True

SUPPORTED_VIDEO_FORMATS = [

    ".mp4",

    ".avi",

    ".mov",

    ".mkv",

    ".webm"

]


# ==========================================================
# ADVANCED AI MEDIA FEATURES
# ==========================================================

ENABLE_BACKGROUND_REMOVAL = True

ENABLE_BACKGROUND_REPLACEMENT = True

ENABLE_FACE_SWAP = True

ENABLE_VOICE_CLONE = True

ENABLE_VIDEO_GENERATOR = True

ENABLE_IMAGE_GENERATOR = True


# ==========================================================
# MEDIA STORAGE
# ==========================================================

MEDIA_DIRECTORY = ASSETS_DIR / "media"

IMAGE_DIRECTORY = MEDIA_DIRECTORY / "images"

VIDEO_DIRECTORY = MEDIA_DIRECTORY / "videos"

AUDIO_DIRECTORY = MEDIA_DIRECTORY / "audio"

GENERATED_DIRECTORY = MEDIA_DIRECTORY / "generated"


MEDIA_DIRECTORIES = [

    MEDIA_DIRECTORY,

    IMAGE_DIRECTORY,

    VIDEO_DIRECTORY,

    AUDIO_DIRECTORY,

    GENERATED_DIRECTORY

]

for folder in MEDIA_DIRECTORIES:
    folder.mkdir(parents=True, exist_ok=True)


# ==========================================================
# END OF SECTION 6
# ==========================================================
