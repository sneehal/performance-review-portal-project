# goal_model.py
# Represents a single row from the GOALS table in Oracle DB
# Used internally between DAO, Service, and Controller layers

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class GoalModel:
    """
    Maps directly to the GOALS table columns.

    GOALS Table:
    goal_id, user_id, cycle_id, title, description,
    weight, target, achievement, created_at
    """
    goal_id: int
    user_id: int
    cycle_id: int
    title: str
    weight: float

    # Optional fields
    description: Optional[str] = None
    target: Optional[str] = None
    achievement: Optional[str] = None
    created_at: Optional[datetime] = None

    def is_achieved(self) -> bool:
        """
        Returns True if employee has entered an achievement.
        Used to check if goal is ready for self-assessment.
        """
        return self.achievement is not None and len(self.achievement.strip()) > 0

    def to_dict(self) -> dict:
        """Converts model to dictionary for API responses"""
        return {
            "goal_id": self.goal_id,
            "user_id": self.user_id,
            "cycle_id": self.cycle_id,
            "title": self.title,
            "description": self.description,
            "weight": self.weight,
            "target": self.target,
            "achievement": self.achievement,
            "created_at": str(self.created_at) if self.created_at else None,
            "is_achieved": self.is_achieved()
        }