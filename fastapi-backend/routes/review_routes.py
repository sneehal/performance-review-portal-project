# review_routes.py

from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from dto.review_dto import SelfAssessmentDTO
from controllers.auth_controller import AuthController
from services.review_service import ReviewService
from utils.response_utils import success_response
from utils.exceptions import ConflictException, ValidationException, NotFoundException

router = APIRouter(prefix="/reviews", tags=["Reviews"])
auth_controller = AuthController()
review_service = ReviewService()


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    return auth_controller.get_token_data(authorization.split(" ")[1])

def get_employee_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")

    user = auth_controller.get_token_data(authorization.split(" ")[1])

    if user.get("role") != "employee":
        raise HTTPException(
            status_code=403,
            detail="Only employees can access this endpoint"
        )

    return user

@router.get("/my/{cycle_id}", summary="Get my review for a cycle")
def get_my_review(cycle_id: int, authorization: Optional[str] = Header(None)):
    """Gets the employee's self-assessment review for a specific cycle."""
    user = get_current_user(authorization)
    try:
        data = review_service.get_my_review(user["user_id"], cycle_id)
        return success_response(data=data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.message))


@router.post("/self-assessment", summary="Submit self-assessment")
def submit_self_assessment(
    body: SelfAssessmentDTO,
    authorization: Optional[str] = Header(None)
):
    user = get_employee_user(authorization)

    try:
        result = review_service.submit_self_assessment(
            user_id=user["user_id"],
            cycle_id=body.cycle_id,
            overall_comment=body.overall_comment,
            ratings=body.ratings
        )
        return success_response(data=result, message="Self-assessment saved as Draft")

    except ConflictException as e:
        raise HTTPException(status_code=409, detail=str(e.message))

    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e.message))


@router.put("/{review_id}/submit", summary="Submit review Draft to Submitted")
def submit_review(
    review_id: int,
    authorization: Optional[str] = Header(None)
):
    user = get_employee_user(authorization)

    try:
        result = review_service.submit_review(review_id, user["user_id"])
        return success_response(data=result, message="Review submitted successfully")

    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e.message))
