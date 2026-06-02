# review_model.py
# Represents rows from REVIEWS and RATINGS tables

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class RatingModel:
    """
    Maps to a single row in the RATINGS table.
    One rating per goal per review.
    """
    rating_id: int
    review_id: int
    goal_id: int
    score: float
    rated_by: int

    # Optional fields
    comment: Optional[str] = None
    goal_title: Optional[str] = None  # Joined from GOALS table

    def to_dict(self) -> dict:
        return {
            "rating_id": self.rating_id,
            "review_id": self.review_id,
            "goal_id": self.goal_id,
            "goal_title": self.goal_title,
            "score": self.score,
            "comment": self.comment,
            "rated_by": self.rated_by
        }


@dataclass
class ReviewModel:
    """
    Maps to a single row in the REVIEWS table.
    Can be a SELF review or MANAGER review.

    REVIEWS Table:
    review_id, user_id, cycle_id, type, status,
    overall_comment, submitted_at, created_at
    """
    review_id: int
    user_id: int
    cycle_id: int
    type: str       # SELF or MANAGER
    status: str     # Draft, Submitted, Completed

    # Optional fields
    overall_comment: Optional[str] = None
    submitted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    # Ratings are loaded separately and attached here
    ratings: List[RatingModel] = field(default_factory=list)

    def is_submitted(self) -> bool:
        """Returns True if employee has submitted the review"""
        return self.status in ("Submitted", "Completed")

    def is_draft(self) -> bool:
        """Returns True if review is still in draft mode"""
        return self.status == "Draft"

    def to_dict(self) -> dict:
        return {
            "review_id": self.review_id,
            "user_id": self.user_id,
            "cycle_id": self.cycle_id,
            "type": self.type,
            "status": self.status,
            "overall_comment": self.overall_comment,
            "submitted_at": str(self.submitted_at) if self.submitted_at else None,
            "created_at": str(self.created_at) if self.created_at else None,
            "ratings": [r.to_dict() for r in self.ratings]
        }


@dataclass
class FeedbackModel:
    """
    Maps to a single row in the FEEDBACK table.
    Created by the manager after reviewing an employee.
    """
    feedback_id: int
    review_id: int
    reviewer_id: int
    feedback_text: str
    overall_rating: float

    # Optional fields
    recommendation: Optional[str] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "feedback_id": self.feedback_id,
            "review_id": self.review_id,
            "reviewer_id": self.reviewer_id,
            "feedback_text": self.feedback_text,
            "overall_rating": self.overall_rating,
            "recommendation": self.recommendation,
            "created_at": str(self.created_at) if self.created_at else None
        }