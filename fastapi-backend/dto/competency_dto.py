# competency_dto.py

from pydantic import BaseModel, Field
from typing import Optional, List


class CompetencyRatingItemDTO(BaseModel):
    """Single competency rating"""
    comp_id: int
    score: float = Field(..., ge=1.0, le=5.0)
    feedback_comment: Optional[str] = Field(None, max_length=300)


class SubmitCompetencyRatingsDTO(BaseModel):
    """Request body for POST /competency-ratings"""
    review_id: int
    ratings: List[CompetencyRatingItemDTO]

    class Config:
        json_schema_extra = {
            "example": {
                "review_id": 1,
                "ratings": [
                    {"comp_id": 1, "score": 4.0, "feedback_comment": "Good communication skills"},
                    {"comp_id": 2, "score": 3.5, "feedback_comment": "Solid technical foundation"}
                ]
            }
        }