# competency_routes.py

from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from dto.competency_dto import SubmitCompetencyRatingsDTO
from controllers.auth_controller import AuthController
from services.competency_service import CompetencyService
from utils.response_utils import success_response

router = APIRouter(prefix="/competencies", tags=["Competencies"])
auth_controller = AuthController()
comp_service = CompetencyService()


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    return auth_controller.get_token_data(authorization.split(" ")[1])


@router.get("", summary="List all active competencies")
def get_all(authorization: Optional[str] = Header(None)):
    """Returns all active company-wide competencies."""
    get_current_user(authorization)
    data = comp_service.get_all_competencies()
    return success_response(data=data)


@router.post("/ratings", summary="Submit competency ratings")
def submit_ratings(body: SubmitCompetencyRatingsDTO,
                   authorization: Optional[str] = Header(None)):
    """Submits competency ratings for a review."""
    user = get_current_user(authorization)
    result = comp_service.submit_ratings(
        review_id=body.review_id,
        rated_by=user["user_id"],
        ratings=body.ratings
    )
    return success_response(data=result, message="Competency ratings saved")


@router.get("/ratings/{review_id}", summary="Get competency ratings for a review")
def get_ratings(review_id: int, authorization: Optional[str] = Header(None)):
    """Returns all competency ratings for a specific review."""
    get_current_user(authorization)
    data = comp_service.get_ratings(review_id)
    return success_response(data=data)