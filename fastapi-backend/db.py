# db.py
# Oracle DB connection using oracledb
# Works with Python 3.13 without Oracle Client (thin mode)

import oracledb
from config import settings

# Global pool variable
_pool = None


def init_db():
    """
    Initializes Oracle connection pool on app startup.

    oracledb has two modes:
    1. THIN MODE (default) — No Oracle Client needed, works out of the box
    2. THICK MODE — Requires Oracle Client, more features

    We use THIN MODE for simplicity and Docker compatibility.
    """
    global _pool

    # DO NOT call oracledb.init_oracle_client() in thin mode
    # Thin mode works automatically without Oracle Client installed

    try:
        _pool = oracledb.create_pool(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            dsn=f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_SERVICE}",
            min=2,
            max=10,
            increment=1
        )
        print(f"✅ Oracle DB pool created | Host: {settings.DB_HOST}:{settings.DB_PORT}")
        print(f"   Service: {settings.DB_SERVICE} | User: {settings.DB_USER}")

    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"❌ Oracle DB connection failed!")
        print(f"   Error: {error_obj.message}")
        print(f"   Check your .env file DB settings")
        # Don't raise — let the app start, but DB calls will fail
        # This makes it easier to debug connection issues
        _pool = None


def get_connection():
    """
    Gets a connection from the pool.

    IMPORTANT: Always use in try/finally:

        conn = get_connection()
        try:
            # do database work
        finally:
            release_connection(conn)
    """
    global _pool

    # Create pool if not initialized (lazy initialization)
    if _pool is None:
        init_db()

    if _pool is None:
        raise ConnectionError(
            "Database connection pool is not available. "
            "Check Oracle DB settings in .env file."
        )

    return _pool.acquire()


def release_connection(conn):
    """
    Returns connection back to the pool.
    Must always be called after using a connection.
    """
    global _pool
    if _pool and conn:
        try:
            _pool.release(conn)
        except Exception:
            pass  # Connection may already be released


def close_pool():
    """Closes entire connection pool on shutdown"""
    global _pool
    if _pool:
        try:
            _pool.close()
            print("🔴 Oracle DB pool closed")
        except Exception:
            pass
        _pool = None