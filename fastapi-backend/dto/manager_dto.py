# manager_dto.py

from pydantic import BaseModel, Field
from typing import Optional, List


class GoalManagerRatingDTO(BaseModel):
    """Manager's rating for a single goal"""
    goal_id: int
    score: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = Field(None, max_length=500)


class ManagerReviewDTO(BaseModel):
    """Request body for POST /manager/review/{review_id}"""
    feedback_text: str = Field(..., min_length=10, description="Detailed written feedback")
    overall_rating: float = Field(..., ge=1.0, le=5.0)
    recommendation: Optional[str] = Field(
        None,
        description="Promote, Excellent, Meets Expectations, Needs Improvement, PIP"
    )
    ratings: List[GoalManagerRatingDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "feedback_text": "Alice consistently delivered quality work and showed strong initiative.",
                "overall_rating": 4.0,
                "recommendation": "Promote",
                "ratings": [
                    {"goal_id": 1, "score": 4.5, "comment": "Excellent delivery"},
                    {"goal_id": 2, "score": 3.5, "comment": "Good work, needs improvement in testing"}
                ]
            }
        }