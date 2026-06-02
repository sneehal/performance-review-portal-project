# manager_routes.py

from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from dto.manager_dto import ManagerReviewDTO
from controllers.auth_controller import AuthController
from services.manager_service import ManagerService
from utils.response_utils import success_response
from utils.exceptions import UnauthorizedException

router = APIRouter(prefix="/manager", tags=["Manager"])
auth_controller = AuthController()
manager_service = ManagerService()


def get_manager_user(authorization: Optional[str] = Header(None)) -> dict:
    """Verifies user is logged in AND is a manager"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    user = auth_controller.get_token_data(authorization.split(" ")[1])
    if user.get("role") not in ("manager", "hr_admin"):
        raise HTTPException(status_code=403, detail="Manager access required")
    return user


@router.get("/pending-reviews", summary="Get team members pending manager review")
def get_pending(authorization: Optional[str] = Header(None)):
    """Returns all submitted self-assessments that need manager review."""
    user = get_manager_user(authorization)
    data = manager_service.get_pending_reviews(user["user_id"])
    return success_response(data=data)


@router.post("/review/{review_id}", summary="Submit manager rating and feedback")
def submit_review(review_id: int, body: ManagerReviewDTO,
                  authorization: Optional[str] = Header(None)):
    """Manager rates employee's goals and submits feedback."""
    user = get_manager_user(authorization)
    try:
        result = manager_service.submit_manager_review(
            review_id=review_id,
            manager_id=user["user_id"],
            feedback_text=body.feedback_text,
            overall_rating=body.overall_rating,
            recommendation=body.recommendation,
            ratings=body.ratings
        )
        return success_response(data=result, message="Manager review submitted")
    except UnauthorizedException as e:
        raise HTTPException(status_code=403, detail=str(e.message))


@router.get("/team-summary", summary="Get overall team rating summary")
def get_team_summary(authorization: Optional[str] = Header(None)):
    """Returns rating summary for all team members."""
    user = get_manager_user(authorization)
    data = manager_service.get_team_summary(user["user_id"])
    return success_response(data=data)


@router.get("/compare/{review_id}", summary="Get self vs manager rating comparison")
def get_comparison(review_id: int, authorization: Optional[str] = Header(None)):
    """Returns side-by-side comparison of self vs manager ratings per goal."""
    get_manager_user(authorization)
    data = manager_service.get_comparison(review_id)
    return success_response(data=data)