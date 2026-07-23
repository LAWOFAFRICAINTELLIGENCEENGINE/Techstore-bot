"""
=========================================================
TechStore Universal Super-System v3
database.py
=========================================================

Central database manager.

Responsibilities:
- SQLite support
- PostgreSQL support (future)
- Connection management
- Automatic initialization
- Health monitoring
- Backup support
"""

# ==========================================================
# IMPORTS
# ==========================================================

import sqlite3
import threading
import logging
from pathlib import Path
from contextlib import contextmanager

from settings import (
    DATABASE_ENGINE,
    SQLITE_DATABASE,
    ENABLE_FOREIGN_KEYS,
    ENABLE_WAL_MODE,
)

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger("TechStore.Database")


# ==========================================================
# DATABASE MANAGER
# ==========================================================

class DatabaseManager:
    """
    Central database manager used by every module.
    """

    def __init__(self):

        self.database_engine = DATABASE_ENGINE

        self.database_path = Path(SQLITE_DATABASE)

        self.connection = None

        self.lock = threading.RLock()

        self.initialize()


    # ======================================================
    # INITIALIZATION
    # ======================================================

    def initialize(self):

        if self.database_engine == "sqlite":
            self._initialize_sqlite()

        else:
            raise NotImplementedError(
                "PostgreSQL initialization will be added in Section 3."
            )


    # ======================================================
    # SQLITE INITIALIZATION
    # ======================================================

    def _initialize_sqlite(self):

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        cursor = self.connection.cursor()

        if ENABLE_FOREIGN_KEYS:
            cursor.execute("PRAGMA foreign_keys = ON;")

        if ENABLE_WAL_MODE:
            cursor.execute("PRAGMA journal_mode = WAL;")

        cursor.execute("PRAGMA synchronous = NORMAL;")

        self.connection.commit()

        logger.info("SQLite database initialized successfully.")


    # ======================================================
    # CONNECTION
    # ======================================================

    @contextmanager
    def get_connection(self):

        with self.lock:
            try:
                yield self.connection
            finally:
                pass


# ==========================================================
# GLOBAL DATABASE INSTANCE
# ==========================================================

db = DatabaseManager()


# ==========================================================
# END OF SECTION 1
# ==========================================================

# ======================================================
# CONNECTION HEALTH
# ======================================================

def reconnect(self):
    """
    Reconnect to the database if the connection is lost.
    """

    try:
        if self.connection:
            self.connection.close()
    except Exception:
        pass

    self._initialize_sqlite()


# ======================================================
# QUERY EXECUTION
# ======================================================

def execute(self, query, parameters=None):

    if parameters is None:
        parameters = ()

    with self.lock:

        try:

            cursor = self.connection.cursor()

            cursor.execute(query, parameters)

            self.connection.commit()

            return cursor

        except Exception as e:

            logger.exception("Database execute error")

            self.connection.rollback()

            raise e


# ======================================================
# FETCH ONE
# ======================================================

def fetch_one(self, query, parameters=None):

    cursor = self.execute(query, parameters)

    return cursor.fetchone()


# ======================================================
# FETCH ALL
# ======================================================

def fetch_all(self, query, parameters=None):

    cursor = self.execute(query, parameters)

    return cursor.fetchall()


# ======================================================
# TRANSACTION
# ======================================================

@contextmanager
def transaction(self):

    with self.lock:

        try:

            yield self.connection

            self.connection.commit()

        except Exception:

            self.connection.rollback()

            raise


# ======================================================
# DATABASE HEALTH
# ======================================================

def ping(self):

    try:

        self.connection.execute("SELECT 1")

        return True

    except Exception:

        return False


# ======================================================
# CLOSE DATABASE
# ======================================================

def close(self):

    if self.connection:

        self.connection.close()

        logger.info("Database connection closed.")
