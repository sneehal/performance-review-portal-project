# admin_routes.py

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import PlainTextResponse
from typing import Optional
from controllers.auth_controller import AuthController
from services.admin_service import AdminService
from utils.response_utils import success_response

router = APIRouter(prefix="/admin", tags=["Admin Reports"])
auth_controller = AuthController()
admin_service = AdminService()


def get_hr_user(authorization: Optional[str] = Header(None)) -> dict:
    """Verifies the user is HR Admin"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    user = auth_controller.get_token_data(authorization.split(" ")[1])
    if user.get("role") != "hr_admin":
        raise HTTPException(status_code=403, detail="HR Admin access required")
    return user


@router.get("/reports/ratings-summary", summary="Department-wise average ratings")
def ratings_summary(authorization: Optional[str] = Header(None)):
    """Returns average ratings grouped by department."""
    get_hr_user(authorization)
    data = admin_service.get_ratings_summary()
    return success_response(data=data)


@router.get("/reports/completion", summary="Cycle completion stats")
def completion_stats(authorization: Optional[str] = Header(None)):
    """Returns submission completion percentage per review cycle."""
    get_hr_user(authorization)
    data = admin_service.get_completion_stats()
    return success_response(data=data)


@router.get("/reports/export", summary="Export full review data as CSV")
def export_csv(authorization: Optional[str] = Header(None)):
    """
    Downloads full review data as CSV.
    Used by HR for payroll and promotion decisions.
    """
    get_hr_user(authorization)
    csv_content = admin_service.export_to_csv()
    # Return as downloadable CSV file
    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=review_export.csv"}
    )