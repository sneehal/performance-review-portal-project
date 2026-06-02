# admin_dto.py
# Request and Response DTOs for Admin/HR endpoints

from pydantic import BaseModel
from typing import Optional


class RatingsSummaryResponseDTO(BaseModel):
    """
    Response model for GET /admin/reports/ratings-summary
    One record per department.
    """
    department: Optional[str]
    total_employees: int
    avg_rating: Optional[float]
    promote_count: int
    pip_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "department": "Engineering",
                "total_employees": 10,
                "avg_rating": 3.85,
                "promote_count": 3,
                "pip_count": 1
            }
        }


class CompletionStatsResponseDTO(BaseModel):
    """
    Response model for GET /admin/reports/completion
    One record per review cycle.
    """
    cycle_id: int
    cycle_name: str
    status: str
    total_employees: int
    submitted_count: int
    completion_pct: float

    class Config:
        json_schema_extra = {
            "example": {
                "cycle_id": 1,
                "cycle_name": "Q1 2025 Appraisal",
                "status": "Active",
                "total_employees": 20,
                "submitted_count": 15,
                "completion_pct": 75.0
            }
        }


class ExportRowDTO(BaseModel):
    """
    Single row in the export CSV.
    One row per employee per cycle.
    """
    user_id: int
    employee_name: str
    department: Optional[str]
    email: str
    cycle_name: Optional[str]
    review_status: Optional[str]
    overall_rating: Optional[float]
    recommendation: Optional[str]
    feedback_text: Optional[str]