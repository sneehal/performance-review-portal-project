# review_dto.py

from pydantic import BaseModel, Field
from typing import Optional, List


class GoalRatingDTO(BaseModel):
    """Single goal rating inside a self-assessment"""
    goal_id: int
    score: float = Field(..., ge=1.0, le=5.0, description="Score from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500)


class SelfAssessmentDTO(BaseModel):
    """Request body for POST /reviews/self-assessment"""
    cycle_id: int
    overall_comment: Optional[str] = None
    ratings: List[GoalRatingDTO] = Field(..., min_length=1, description="List of goal ratings")

    class Config:
        json_schema_extra = {
            "example": {
                "cycle_id": 1,
                "overall_comment": "I had a productive quarter and delivered all my goals.",
                "ratings": [
                    {"goal_id": 1, "score": 4.0, "comment": "Delivered ahead of schedule"},
                    {"goal_id": 2, "score": 3.5, "comment": "Met targets with some challenges"}
                ]
            }
        }


class ReviewResponseDTO(BaseModel):
    """Response model for review data"""
    review_id: int
    user_id: int
    cycle_id: int
    type: str
    status: str
    overall_comment: Optional[str]
    submitted_at: Optional[str]