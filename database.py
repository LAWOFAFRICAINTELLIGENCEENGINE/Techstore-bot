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

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None
    RealDictCursor = None

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

elif self.database_engine == "postgresql":
    self._initialize_postgresql()

else:
    raise ValueError(
        f"Unsupported database engine: {self.database_engine}"
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


# ======================================================
# RECONNECT DATABASE
# ======================================================

def reconnect(self):
    """
    Reconnect to the database.
    """

    logger.warning("Reconnecting database...")

    try:
        if self.connection:
            self.connection.close()
    except Exception:
        pass

    self.initialize()


# ======================================================
# EXECUTE QUERY
# ======================================================

def execute(self, query, parameters=None):
    """
    Execute INSERT, UPDATE or DELETE query.
    """

    if parameters is None:
        parameters = ()

    with self.lock:

        try:

            cursor = self.connection.cursor()

            cursor.execute(query, parameters)

            self.connection.commit()

            return cursor

        except Exception as e:

            logger.exception("Database execution failed.")

            self.connection.rollback()

            raise e


# ======================================================
# FETCH ONE
# ======================================================

def fetch_one(self, query, parameters=None):
    """
    Return one record.
    """

    cursor = self.execute(query, parameters)

    return cursor.fetchone()


# ======================================================
# FETCH ALL
# ======================================================

def fetch_all(self, query, parameters=None):
    """
    Return multiple records.
    """

    cursor = self.execute(query, parameters)

    return cursor.fetchall()


# ======================================================
# INSERT
# ======================================================

def insert(self, query, parameters=None):
    """
    Execute INSERT query.
    """

    cursor = self.execute(query, parameters)

    return cursor.lastrowid


# ======================================================
# UPDATE
# ======================================================

def update(self, query, parameters=None):
    """
    Execute UPDATE query.
    """

    cursor = self.execute(query, parameters)

    return cursor.rowcount


# ======================================================
# DELETE
# ======================================================

def delete(self, query, parameters=None):
    """
    Execute DELETE query.
    """

    cursor = self.execute(query, parameters)

    return cursor.rowcount


# ======================================================
# TRANSACTION
# ======================================================

@contextmanager
def transaction(self):
    """
    Execute multiple SQL operations safely.
    """

    with self.lock:

        try:

            yield self.connection

            self.connection.commit()

        except Exception:

            self.connection.rollback()

            raise


# ======================================================
# DATABASE HEALTH CHECK
# ======================================================

def ping(self):
    """
    Check database connection.
    """

    try:

        self.connection.execute("SELECT 1")

        return True

    except Exception:

        return False


# ======================================================
# DATABASE INFORMATION
# ======================================================

def database_information(self):
    """
    Return database information.
    """

    return {

        "engine": self.database_engine,

        "database": str(self.database_path),

        "connected": self.ping()

    }


# ======================================================
# CLOSE DATABASE
# ======================================================

def close(self):
    """
    Close database connection.
    """

    try:

        if self.connection:

            self.connection.close()

            logger.info("Database connection closed.")

    except Exception as e:

        logger.exception(e)

# ======================================================
# CREATE ALL DATABASE TABLES
# ======================================================

def create_tables(self):
    """
    Create every database table required by TechStore.
    """

    # ==========================
    # Authentication
    # ==========================

    self.create_users_table()
    self.create_roles_table()

    # ==========================
    # Configuration
    # ==========================

    self.create_settings_table()
    self.create_api_keys_table()

    # ==========================
    # AI
    # ==========================

    self.create_memory_table()
    self.create_cache_table()
    self.create_ai_sessions_table()

    # ==========================
    # Business
    # ==========================

    self.create_inventory_table()
    self.create_customers_table()
    self.create_orders_table()
    self.create_products_table()
    self.create_sales_table()
    self.create_invoices_table()

    # ==========================
    # Developer
    # ==========================

    self.create_projects_table()
    self.create_plugins_table()
    self.create_api_usage_table()
    self.create_diagnostics_table()
    self.create_logs_table()

    # ==========================
    # Media
    # ==========================

    self.create_uploaded_files_table()
    self.create_images_table()
    self.create_videos_table()
    self.create_voice_table()
    self.create_documents_table()

    # ==========================
    # Monitoring
    # ==========================

    self.create_health_reports_table()
    self.create_performance_reports_table()
    self.create_analytics_table()
    self.create_backups_table()

    logger.info("All TechStore database tables created successfully.")
