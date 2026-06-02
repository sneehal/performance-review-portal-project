# review_cycle_dto.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateCycleDTO(BaseModel):
    """Request body for POST /review-cycles"""
    name: str = Field(..., min_length=3, max_length=100)
    start_date: date
    end_date: date
    self_due_date: date
    manager_due_date: date

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Q2 2025 Appraisal",
                "start_date": "2025-04-01",
                "end_date": "2025-06-30",
                "self_due_date": "2025-06-15",
                "manager_due_date": "2025-06-25"
            }
        }


class UpdateCycleDTO(BaseModel):
    """Request body for PUT /review-cycles/{id}"""
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    self_due_date: Optional[date] = None
    manager_due_date: Optional[date] = None
    status: Optional[str] = None  # Draft, Active, Closed


class CycleResponseDTO(BaseModel):
    """Response model for review cycle data"""
    cycle_id: int
    name: str
    start_date: date
    end_date: date
    self_due_date: date
    manager_due_date: date
    status: str
    created_by: int