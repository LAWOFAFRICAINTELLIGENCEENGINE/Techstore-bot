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
# Automatically create database schema
    self.initialize_schema()

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

    # Database Version
    self.create_migrations_table()

   # Default Settings
    self.initialize_default_settings()

    # Default Settings
    self.initialize_default_api_keys()


    logger.info("All TechStore database tables created successfully.")

# ======================================================
# INVENTORY TABLE
# ======================================================

def create_inventory_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS inventory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_name TEXT NOT NULL,

        sku TEXT UNIQUE,

        category TEXT,

        quantity INTEGER DEFAULT 0,

        price REAL DEFAULT 0,

        supplier TEXT,

        status TEXT DEFAULT 'In Stock',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP

    )
    """)


# ======================================================
# USERS TABLE
# ======================================================

def create_users_table(self):
    """
    Create the users table.
    """

    self.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password_hash TEXT NOT NULL,

        full_name TEXT,

        profile_image TEXT,

        phone TEXT,

        country TEXT,

        role TEXT DEFAULT 'user',

        is_active INTEGER DEFAULT 1,

        is_verified INTEGER DEFAULT 0,

        failed_login_attempts INTEGER DEFAULT 0,

        locked_until TIMESTAMP,

        last_login TIMESTAMP,

        password_changed_at TIMESTAMP,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP

    )
    """)

# ======================================================
# ROLES TABLE
# ======================================================

def create_roles_table(self):
    """
    Create roles table.
    """

    self.execute("""
    CREATE TABLE IF NOT EXISTS roles (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        role_name TEXT UNIQUE NOT NULL,

        description TEXT,

        permissions TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

# ======================================================
# CREATE DEFAULT ROLES
# ======================================================

def create_default_roles(self):
    """
    Insert default roles.
    """

    roles = [

        ("admin", "System Administrator", "all"),

        ("user", "Normal User", "standard"),

        ("moderator", "Moderator", "moderate")

    ]

    for role in roles:

        try:

            self.execute(

                """
                INSERT OR IGNORE INTO roles
                (role_name, description, permissions)

                VALUES (?, ?, ?)
                """,

                role

            )

        except Exception:

            pass

# ======================================================
# ORDERS TABLE
# ======================================================

def create_orders_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS orders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_id INTEGER,

        total REAL DEFAULT 0,

        status TEXT DEFAULT 'Pending',

        payment_status TEXT DEFAULT 'Unpaid',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(customer_id)
        REFERENCES customers(id)

    )
    """)


# ======================================================
# PRODUCTS TABLE
# ======================================================

def create_products_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS products (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_name TEXT NOT NULL,

        description TEXT,

        category TEXT,

        price REAL,

        stock INTEGER DEFAULT 0,

        barcode TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# SALES TABLE
# ======================================================

def create_sales_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS sales (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        order_id INTEGER,

        amount REAL,

        payment_method TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(order_id)
        REFERENCES orders(id)

    )
    """)


# ======================================================
# INVOICES TABLE
# ======================================================

def create_invoices_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS invoices (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_number TEXT UNIQUE,

        customer_id INTEGER,

        order_id INTEGER,

        amount REAL,

        status TEXT DEFAULT 'Pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(customer_id)
        REFERENCES customers(id),

        FOREIGN KEY(order_id)
        REFERENCES orders(id)

    )
    """)

# ======================================================
# PROJECTS TABLE
# ======================================================

def create_projects_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS projects (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_name TEXT NOT NULL,

        description TEXT,

        owner TEXT,

        status TEXT DEFAULT 'Active',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP

    )
    """)


# ======================================================
# PLUGINS TABLE
# ======================================================

def create_plugins_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS plugins (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        plugin_name TEXT UNIQUE NOT NULL,

        version TEXT,

        author TEXT,

        enabled INTEGER DEFAULT 1,

        installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# API USAGE TABLE
# ======================================================

def create_api_usage_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS api_usage (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        provider TEXT NOT NULL,

        model TEXT,

        endpoint TEXT,

        tokens_used INTEGER DEFAULT 0,

        request_time REAL DEFAULT 0,

        cost REAL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# DIAGNOSTICS TABLE
# ======================================================

def create_diagnostics_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS diagnostics (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        component TEXT,

        severity TEXT,

        message TEXT,

        resolved INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# SYSTEM LOGS TABLE
# ======================================================

def create_logs_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        level TEXT,

        module TEXT,

        message TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)
    
# ======================================================
# UPLOADED FILES TABLE
# ======================================================

def create_uploaded_files_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS uploaded_files (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT NOT NULL,

        file_type TEXT,

        file_size INTEGER,

        file_path TEXT,

        uploaded_by TEXT,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# IMAGES TABLE
# ======================================================

def create_images_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS images (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        path TEXT,

        width INTEGER,

        height INTEGER,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# VIDEOS TABLE
# ======================================================

def create_videos_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS videos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        path TEXT,

        duration REAL,

        resolution TEXT,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# VOICE TABLE
# ======================================================

def create_voice_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS voice (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        path TEXT,

        duration REAL,

        sample_rate INTEGER,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# DOCUMENTS TABLE
# ======================================================

def create_documents_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        document_type TEXT,

        path TEXT,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# HEALTH REPORTS TABLE
# ======================================================

def create_health_reports_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS health_reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        component TEXT,

        status TEXT,

        message TEXT,

        checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# PERFORMANCE REPORTS TABLE
# ======================================================

def create_performance_reports_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS performance_reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        cpu_usage REAL,

        memory_usage REAL,

        disk_usage REAL,

        response_time REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# ANALYTICS TABLE
# ======================================================

def create_analytics_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS analytics (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        metric TEXT,

        value REAL,

        category TEXT,

        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# BACKUPS TABLE
# ======================================================

def create_backups_table(self):

    self.execute("""
    CREATE TABLE IF NOT EXISTS backups (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        backup_name TEXT,

        backup_path TEXT,

        backup_size INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

# ======================================================
# DATABASE MIGRATIONS
# ======================================================

def create_migrations_table(self):
    """
    Store schema versions for future upgrades.
    """

    self.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        version TEXT UNIQUE NOT NULL,

        description TEXT,

        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


# ======================================================
# DATABASE INDEXES
# ======================================================

def create_indexes(self):
    """
    Create indexes for better performance.
    """

    indexes = [

        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",

        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",

        "CREATE INDEX IF NOT EXISTS idx_inventory_sku ON inventory(sku);",

        "CREATE INDEX IF NOT EXISTS idx_products_name ON products(product_name);",

        "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);",

        "CREATE INDEX IF NOT EXISTS idx_sales_order_id ON sales(order_id);",

        "CREATE INDEX IF NOT EXISTS idx_memory_session ON conversation_memory(session_id);",

        "CREATE INDEX IF NOT EXISTS idx_cache_hash ON response_cache(prompt_hash);"

    ]

    for sql in indexes:

        self.execute(sql)


# ======================================================
# ENABLE FOREIGN KEYS
# ======================================================

def enable_foreign_keys(self):
    """
    Enable SQLite foreign key enforcement.
    """

    if self.database_engine == "sqlite":

        self.execute("PRAGMA foreign_keys = ON;")


# ======================================================
# INITIALIZE DATABASE STRUCTURE
# ======================================================

def initialize_schema(self):
    """
    Create every database object.
    """

    self.enable_foreign_keys()

    self.create_tables()

    self.create_migrations_table()

    self.create_indexes()

    logger.info("Database schema initialized successfully.")

# ======================================================
# CREATE USER
# ======================================================

def create_user(
    self,
    username,
    email,
    password_hash,
    full_name=None,
    role="user",
):
    """
    Create a new user.
    """

    query = """
    INSERT INTO users
    (
        username,
        email,
        password_hash,
        full_name,
        role
    )
    VALUES (?, ?, ?, ?, ?)
    """

    return self.insert(
        query,
        (
            username,
            email,
            password_hash,
            full_name,
            role,
        ),
    )


# ======================================================
# GET USER BY ID
# ======================================================

def get_user_by_id(self, user_id):
    """
    Return a user by ID.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    )


# ======================================================
# GET USER BY USERNAME
# ======================================================

def get_user_by_username(self, username):
    """
    Return a user by username.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,),
    )


# ======================================================
# GET USER BY EMAIL
# ======================================================

def get_user_by_email(self, email):
    """
    Return a user by email.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,),
    )

# ======================================================
# CREATE ROLE
# ======================================================

def create_role(self, role_name, description="", permissions=""):
    """
    Create a new role.
    """

    query = """
    INSERT INTO roles
    (role_name, description, permissions)
    VALUES (?, ?, ?)
    """

    return self.insert(
        query,
        (
            role_name,
            description,
            permissions,
        ),
    )


# ======================================================
# GET ROLE BY ID
# ======================================================

def get_role_by_id(self, role_id):
    """
    Return one role by ID.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM roles
        WHERE id = ?
        """,
        (role_id,),
    )


# ======================================================
# GET ROLE BY NAME
# ======================================================

def get_role_by_name(self, role_name):
    """
    Return one role by name.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM roles
        WHERE role_name = ?
        """,
        (role_name,),
    )


# ======================================================
# GET ALL ROLES
# ======================================================

def get_all_roles(self):
    """
    Return all roles.
    """

    return self.fetch_all(
        """
        SELECT *
        FROM roles
        ORDER BY role_name
        """
    )


# ======================================================
# UPDATE ROLE
# ======================================================

def update_role(
    self,
    role_id,
    description,
    permissions,
):
    """
    Update role information.
    """

    return self.update(
        """
        UPDATE roles
        SET
            description = ?,
            permissions = ?
        WHERE id = ?
        """,
        (
            description,
            permissions,
            role_id,
        ),
    )


# ======================================================
# DELETE ROLE
# ======================================================

def delete_role(self, role_id):
    """
    Delete a role.
    """

    return self.delete(
        """
        DELETE FROM roles
        WHERE id = ?
        """,
        (role_id,),
    )


# ======================================================
# ROLE EXISTS
# ======================================================

def role_exists(self, role_name):
    """
    Check whether a role exists.
    """

    return self.get_role_by_name(role_name) is not None

# ======================================================
# CREATE SETTING
# ======================================================

def create_setting(self, setting_key, setting_value):
    """
    Create a new application setting.
    """

    return self.insert(
        """
        INSERT OR REPLACE INTO settings
        (setting_key, setting_value)
        VALUES (?, ?)
        """,
        (
            setting_key,
            setting_value,
        ),
    )


# ======================================================
# GET SETTING
# ======================================================

def get_setting(self, setting_key):
    """
    Return one setting.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM settings
        WHERE setting_key = ?
        """,
        (setting_key,),
    )


# ======================================================
# GET SETTING VALUE
# ======================================================

def get_setting_value(self, setting_key, default=None):
    """
    Return only the setting value.
    """

    row = self.get_setting(setting_key)

    if row is None:
        return default

    return row["setting_value"]


# ======================================================
# GET ALL SETTINGS
# ======================================================

def get_all_settings(self):
    """
    Return every application setting.
    """

    return self.fetch_all(
        """
        SELECT *
        FROM settings
        ORDER BY setting_key
        """
    )


# ======================================================
# UPDATE SETTING
# ======================================================

def update_setting(self, setting_key, setting_value):
    """
    Update one setting.
    """

    return self.update(
        """
        UPDATE settings
        SET setting_value = ?
        WHERE setting_key = ?
        """,
        (
            setting_value,
            setting_key,
        ),
    )


# ======================================================
# DELETE SETTING
# ======================================================

def delete_setting(self, setting_key):
    """
    Delete one setting.
    """

    return self.delete(
        """
        DELETE FROM settings
        WHERE setting_key = ?
        """,
        (setting_key,),
    )


# ======================================================
# SETTING EXISTS
# ======================================================

def setting_exists(self, setting_key):
    """
    Check whether a setting exists.
    """

    return self.get_setting(setting_key) is not None

# ======================================================
# INITIALIZE DEFAULT SETTINGS
# ======================================================

def initialize_default_settings(self):
    """
    Create default application settings.
    """

    defaults = {

        "theme": "dark",

        "language": "en",

        "default_ai": "auto",

        "streaming": "true",

        "voice_enabled": "true",

        "video_enabled": "true",

        "face_swap_enabled": "true",

        "voice_clone_enabled": "true",

        "background_removal": "true",

        "video_generation": "true",

        "plugins_enabled": "true",

        "cache_enabled": "true",

        "memory_enabled": "true",

        "health_monitor": "true",

        "performance_monitor": "true",

        "auto_update": "true",

        "backup_enabled": "true",

        "developer_mode": "false",

    }

    for key, value in defaults.items():

        if not self.setting_exists(key):

            self.create_setting(key, value)

# ======================================================
# CREATE API KEY
# ======================================================

def create_api_key(
    self,
    provider,
    api_key,
    description="",
    active=True,
):
    """
    Store an API key.
    """

    return self.insert(
        """
        INSERT OR REPLACE INTO api_keys
        (
            provider,
            api_key,
            description,
            active
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            provider,
            api_key,
            description,
            int(active),
        ),
    )


# ======================================================
# GET API KEY
# ======================================================

def get_api_key(self, provider):
    """
    Return one API key.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM api_keys
        WHERE provider = ?
        """,
        (provider,),
    )


# ======================================================
# GET API KEY VALUE
# ======================================================

def get_api_key_value(self, provider):
    """
    Return only the key.
    """

    row = self.get_api_key(provider)

    if row:

        return row["api_key"]

    return None


# ======================================================
# GET ALL API KEYS
# ======================================================

def get_all_api_keys(self):
    """
    Return all API keys.
    """

    return self.fetch_all(
        """
        SELECT *
        FROM api_keys
        ORDER BY provider
        """
    )


# ======================================================
# UPDATE API KEY
# ======================================================

def update_api_key(
    self,
    provider,
    api_key,
):
    """
    Update API key.
    """

    return self.update(
        """
        UPDATE api_keys
        SET api_key = ?
        WHERE provider = ?
        """,
        (
            api_key,
            provider,
        ),
    )


# ======================================================
# DELETE API KEY
# ======================================================

def delete_api_key(self, provider):
    """
    Delete one API key.
    """

    return self.delete(
        """
        DELETE FROM api_keys
        WHERE provider = ?
        """,
        (provider,),
    )


# ======================================================
# API KEY EXISTS
# ======================================================

def api_key_exists(self, provider):
    """
    Check whether an API key exists.
    """

    return self.get_api_key(provider) is not None

# ======================================================
# INITIALIZE DEFAULT API PROVIDERS
# ======================================================

def initialize_default_api_keys(self):
    """
    Register supported providers.
    """

    providers = [

        "xai",

        "gemini",

        "groq",

        "openai",

        "anthropic",

        "deepseek",

        "stability",

        "elevenlabs",

        "tavily",

        "video_generation",

        "face_swap",

        "voice_clone",

    ]

    for provider in providers:

        if not self.api_key_exists(provider):

            self.create_api_key(
                provider,
                "",
                "Not configured",
                False,
            )

# ======================================================
# CREATE MEMORY
# ======================================================

def create_memory(
    self,
    user_id,
    memory_type,
    title,
    content,
):
    """
    Save a memory.
    """

    return self.insert(
        """
        INSERT INTO conversation_memory
        (
            user_id,
            memory_type,
            title,
            content
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            memory_type,
            title,
            content,
        ),
    )


# ======================================================
# GET MEMORY
# ======================================================

def get_memory(self, memory_id):
    """
    Return one memory.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM conversation_memory
        WHERE id = ?
        """,
        (memory_id,),
    )


# ======================================================
# GET USER MEMORIES
# ======================================================

def get_user_memories(self, user_id):
    """
    Return all memories for one user.
    """

    return self.fetch_all(
        """
        SELECT *
        FROM conversation_memory
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )


# ======================================================
# SEARCH MEMORY
# ======================================================

def search_memory(self, keyword):
    """
    Search memories.
    """

    return self.fetch_all(
        """
        SELECT *
        FROM conversation_memory
        WHERE
            title LIKE ?
            OR content LIKE ?
        ORDER BY created_at DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
        ),
    )


# ======================================================
# UPDATE MEMORY
# ======================================================

def update_memory(
    self,
    memory_id,
    title,
    content,
):
    """
    Update a memory.
    """

    return self.update(
        """
        UPDATE conversation_memory
        SET
            title = ?,
            content = ?
        WHERE id = ?
        """,
        (
            title,
            content,
            memory_id,
        ),
    )


# ======================================================
# DELETE MEMORY
# ======================================================

def delete_memory(self, memory_id):
    """
    Delete one memory.
    """

    return self.delete(
        """
        DELETE FROM conversation_memory
        WHERE id = ?
        """,
        (memory_id,),
    )


# ======================================================
# DELETE USER MEMORIES
# ======================================================

def delete_user_memories(self, user_id):
    """
    Delete all memories for one user.
    """

    return self.delete(
        """
        DELETE FROM conversation_memory
        WHERE user_id = ?
        """,
        (user_id,),
    )


# ======================================================
# MEMORY EXISTS
# ======================================================

def memory_exists(self, memory_id):
    """
    Check whether a memory exists.
    """

    return self.get_memory(memory_id) is not None


# ======================================================
# MEMORY COUNT
# ======================================================

def memory_count(self, user_id):
    """
    Return total memories for a user.
    """

    row = self.fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM conversation_memory
        WHERE user_id = ?
        """,
        (user_id,),
    )

    return row["total"]

# ======================================================
# CREATE CACHE
# ======================================================

def create_cache(
    self,
    prompt_hash,
    prompt,
    response,
    model,
):
    """
    Save an AI response into cache.
    """

    return self.insert(
        """
        INSERT OR REPLACE INTO response_cache
        (
            prompt_hash,
            prompt,
            response,
            model
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            prompt_hash,
            prompt,
            response,
            model,
        ),
    )


# ======================================================
# GET CACHE
# ======================================================

def get_cache(self, prompt_hash):
    """
    Return cached response.
    """

    return self.fetch_one(
        """
        SELECT *
        FROM response_cache
        WHERE prompt_hash = ?
        """,
        (prompt_hash,),
    )


# ======================================================
# CACHE EXISTS
# ======================================================

def cache_exists(self, prompt_hash):
    """
    Check whether cache exists.
    """

    return self.get_cache(prompt_hash) is not None


# ======================================================
# UPDATE CACHE
# ======================================================

def update_cache(
    self,
    prompt_hash,
    response,
):
    """
    Update cached response.
    """

    return self.update(
        """
        UPDATE response_cache
        SET
            response = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE prompt_hash = ?
        """,
        (
            response,
            prompt_hash,
        ),
    )


# ======================================================
# DELETE CACHE
# ======================================================

def delete_cache(self, prompt_hash):
    """
    Delete one cached response.
    """

    return self.delete(
        """
        DELETE FROM response_cache
        WHERE prompt_hash = ?
        """,
        (prompt_hash,),
    )


# ======================================================
# CLEAR CACHE
# ======================================================

def clear_cache(self):
    """
    Remove every cached response.
    """

    return self.delete(
        """
        DELETE FROM response_cache
        """
    )


# ======================================================
# CACHE COUNT
# ======================================================

def cache_count(self):
    """
    Return number of cached responses.
    """

    row = self.fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM response_cache
        """
    )

    return row["total"]


# ======================================================
# GET RECENT CACHE
# ======================================================

def get_recent_cache(self, limit=20):
    """
    Return recent cached responses.
    """

    return self.fetch_all(
        """
        SELECT *
        FROM response_cache
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )


# ======================================================
# CACHE STATISTICS
# ======================================================

def cache_statistics(self):
    """
    Return cache statistics.
    """

    return {
        "entries": self.cache_count(),
    }
