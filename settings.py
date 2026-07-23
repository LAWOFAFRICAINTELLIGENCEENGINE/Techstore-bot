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
