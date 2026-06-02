# goal_dto.py

from pydantic import BaseModel, Field
from typing import Optional


class CreateGoalDTO(BaseModel):
    """Request body for POST /goals"""
    cycle_id: int
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    weight: float = Field(..., gt=0, le=100, description="Weight percentage (1-100)")
    target: Optional[str] = Field(None, max_length=300)

    class Config:
        json_schema_extra = {
            "example": {
                "cycle_id": 1,
                "title": "Complete React Dashboard Project",
                "description": "Build and deliver the performance review dashboard module",
                "weight": 40.0,
                "target": "Deliver fully functional dashboard by March 31"
            }
        }


class UpdateGoalDTO(BaseModel):
    """Request body for PUT /goals/{id}"""
    title: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0, le=100)
    target: Optional[str] = None


class UpdateAchievementDTO(BaseModel):
    """Request body for PUT /goals/{id}/achievement"""
    achievement: str = Field(..., max_length=300, description="What was actually achieved")

    class Config:
        json_schema_extra = {
            "example": {
                "achievement": "Delivered dashboard 2 days ahead of schedule with all required features"
            }
        }


class GoalResponseDTO(BaseModel):
    """Response model for goal data"""
    goal_id: int
    user_id: int
    cycle_id: int
    title: str
    description: Optional[str]
    weight: float
    target: Optional[str]
    achievement: Optional[str]