# competency_model.py
# Represents rows from COMPETENCIES and COMPETENCY_RATINGS tables

from dataclasses import dataclass
from typing import Optional


@dataclass
class CompetencyModel:
    """
    Maps to a single row in the COMPETENCIES table.
    These are company-wide skills defined by HR.

    COMPETENCIES Table:
    comp_id, name, description, is_active
    """
    comp_id: int
    name: str
    is_active: int   # 1 = active, 0 = disabled

    description: Optional[str] = None

    def is_enabled(self) -> bool:
        """Returns True if this competency is currently active"""
        return self.is_active == 1

    def to_dict(self) -> dict:
        return {
            "comp_id": self.comp_id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active
        }


@dataclass
class CompetencyRatingModel:
    """
    Maps to a single row in the COMPETENCY_RATINGS table.
    Both employees and managers submit these ratings separately.

    COMPETENCY_RATINGS Table:
    cr_id, review_id, comp_id, score, rated_by, comment
    """
    cr_id: int
    review_id: int
    comp_id: int
    score: float
    rated_by: int

    feedback_comment: Optional[str] = None
    competency_name: Optional[str] = None   # Joined from COMPETENCIES

    def to_dict(self) -> dict:
        return {
            "cr_id": self.cr_id,
            "review_id": self.review_id,
            "comp_id": self.comp_id,
            "competency_name": self.competency_name,
            "score": self.score,
            "rated_by": self.rated_by,
            "feedback_comment": self.feedback_comment
        }