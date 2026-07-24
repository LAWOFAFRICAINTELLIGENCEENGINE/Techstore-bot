"""
=========================================================
TechStore-bot Super-System
Authentication Manager
=========================================================
"""

# =====================================================
# IMPORTS
# =====================================================

import secrets
import hashlib
import logging
import threading
from datetime import datetime, timedelta

from database import db

from settings import (
    SESSION_TIMEOUT,
    PASSWORD_MIN_LENGTH,
)

# =====================================================
# LOGGER
# =====================================================

logger = logging.getLogger("TechStore.Authentication")

# =====================================================
# AUTHENTICATION MANAGER
# =====================================================

class AuthenticationManager:
    """
    Central authentication manager.
    """

    def __init__(self):

        self.lock = threading.RLock()

        self.active_sessions = {}

        self.initialize()

# =====================================================
# INITIALIZE
# =====================================================

    def initialize(self):
        """
        Initialize authentication system.
        """

        logger.info("Initializing authentication system...")

# =====================================================
# SESSION TOKEN
# =====================================================

    def generate_session_token(self):
        """
        Generate a secure session token.
        """

        return secrets.token_hex(32)

# =====================================================
# PASSWORD HASH
# =====================================================

    def hash_password(self, password):
        """
        Return SHA-256 password hash.
        """

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

# =====================================================
# PASSWORD VERIFY
# =====================================================

    def verify_password(
        self,
        password,
        hashed_password,
    ):
        """
        Verify password.
        """

        return (
            self.hash_password(password)
            == hashed_password
        )

# =====================================================
# AUTHENTICATION HEALTH
# =====================================================

    def health(self):
        """
        Return authentication status.
        """

        return {

            "active_sessions": len(
                self.active_sessions
            ),

            "status": "healthy",

        }

# =====================================================
# GLOBAL AUTH INSTANCE
# =====================================================

auth = AuthenticationManager()


# =====================================================
# USERNAME VALIDATION
# =====================================================

def validate_username(self, username):
    """
    Validate username.
    """

    if not username:
        return False, "Username is required."

    username = username.strip()

    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if len(username) > 32:
        return False, "Username cannot exceed 32 characters."

    return True, ""


# =====================================================
# EMAIL VALIDATION
# =====================================================

def validate_email(self, email):
    """
    Validate email address.
    """

    if not email:
        return False, "Email is required."

    email = email.strip().lower()

    if "@" not in email or "." not in email:
        return False, "Invalid email address."

    return True, ""


# =====================================================
# PASSWORD VALIDATION
# =====================================================

def validate_password(self, password):
    """
    Validate password.
    """

    if not password:
        return False, "Password is required."

    if len(password) < PASSWORD_MIN_LENGTH:
        return (
            False,
            f"Password must be at least {PASSWORD_MIN_LENGTH} characters."
        )

    return True, ""


# =====================================================
# REGISTER USER
# =====================================================

def register_user(
    self,
    username,
    email,
    password,
):
    """
    Register a new user.
    """

    valid, message = self.validate_username(username)

    if not valid:
        return False, message

    valid, message = self.validate_email(email)

    if not valid:
        return False, message

    valid, message = self.validate_password(password)

    if not valid:
        return False, message

    if db.get_user_by_username(username):
        return False, "Username already exists."

    if db.get_user_by_email(email):
        return False, "Email already exists."

    password_hash = self.hash_password(password)

    db.create_user(
        username=username,
        email=email,
        password_hash=password_hash,
    )

    logger.info(
        f"User registered: {username}"
    )

    return True, "Registration successful."

# =====================================================
# LOGIN USER
# =====================================================

def login(self, username, password):
    """
    Authenticate a user and create a session.
    """

    user = db.get_user_by_username(username)

    if not user:
        return False, "Invalid username or password."

    password_hash = self.hash_password(password)

    if password_hash != user["password_hash"]:
        logger.warning(f"Failed login attempt: {username}")
        return False, "Invalid username or password."

    session_token = secrets.token_hex(32)

    expires_at = datetime.utcnow() + timedelta(
        seconds=SESSION_TIMEOUT
    )

    db.create_session(
        user_id=user["id"],
        session_token=session_token,
        expires_at=expires_at,
    )

    db.update_last_login(user["id"])

    logger.info(f"User logged in: {username}")

    return True, {
        "session_token": session_token,
        "user": user,
    }


# =====================================================
# VERIFY SESSION
# =====================================================

def verify_session(self, session_token):
    """
    Verify an active session.
    """

    session = db.get_session(session_token)

    if not session:
        return None

    if session["expires_at"] < datetime.utcnow():
        db.delete_session(session_token)
        return None

    return session


# =====================================================
# LOGOUT USER
# =====================================================

def logout(self, session_token):
    """
    Logout user.
    """

    db.delete_session(session_token)

    logger.info("Session terminated.")

    return True


# =====================================================
# CLEANUP EXPIRED SESSIONS
# =====================================================

def cleanup_sessions(self):
    """
    Remove expired sessions.
    """

    db.delete_expired_sessions()

    logger.info("Expired sessions removed.")

