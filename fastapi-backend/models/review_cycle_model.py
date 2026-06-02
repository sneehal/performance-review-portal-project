# review_cycle_model.py

from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class ReviewCycleModel:
    """Represents a row from the REVIEW_CYCLES table"""
    cycle_id: int
    name: str
    start_date: date
    end_date: date
    self_due_date: date
    manager_due_date: date
    status: str
    created_by: int
    created_at: Optional[datetime] = None