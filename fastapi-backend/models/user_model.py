# user_model.py
# Simple Python classes representing database rows
# These are NOT Pydantic models - just plain Python classes
# Used internally in services and DAOs

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class UserModel:
    """
    Represents a row from the USERS table.
    Dataclass auto-generates __init__, __repr__ etc.
    """
    user_id: int
    name: str
    email: str
    password_hash: str
    role: str
    department: Optional[str]
    manager_id: Optional[int]
    is_active: int
    created_at: Optional[datetime]