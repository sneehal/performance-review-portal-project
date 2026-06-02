# db_utils.py
# Helper utilities for Oracle database operations
# Fixes CLOB, DATE, NUMBER type conversion issues

from datetime import datetime, date


def read_lob(value) -> str:
    """
    Reads an Oracle CLOB/LOB object and returns plain string.

    Problem:
        Oracle CLOB columns return a ThinLobImpl object.
        FastAPI cannot serialize this to JSON.

    Fix:
        Call .read() on LOB objects to get the actual string.

    Args:
        value: Could be LOB object, string, or None

    Returns:
        Plain string or None

    Usage:
        description = read_lob(row[4])  # row[4] is a CLOB column
    """
    if value is None:
        return None

    # If it is already a plain string, return as is
    if isinstance(value, str):
        return value

    # If it is an Oracle LOB object, read it
    try:
        return value.read()
    except Exception:
        # Last resort: convert to string
        return str(value)


def safe_int(value) -> int:
    """Safely converts Oracle NUMBER to Python int"""
    if value is None:
        return None
    return int(value)


def safe_float(value) -> float:
    """Safely converts Oracle NUMBER to Python float"""
    if value is None:
        return None
    return float(value)


def safe_str(value) -> str:
    """Safely converts any Oracle value to string"""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    # Handle LOB objects
    try:
        return value.read()
    except Exception:
        return str(value)


def safe_date(value) -> str:
    """
    Converts Oracle DATE/TIMESTAMP to string.
    Oracle DATE returns Python datetime object.
    """
    if value is None:
        return None
    if isinstance(value, (datetime, date)):
        return str(value)
    return str(value)