# review_cycle_routes.py

from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from dto.review_cycle_dto import CreateCycleDTO, UpdateCycleDTO
from controllers.auth_controller import AuthController
from services.review_cycle_service import ReviewCycleService
from utils.response_utils import success_response
from utils.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/review-cycles", tags=["Review Cycles"])
auth_controller = AuthController()
cycle_service = ReviewCycleService()


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Helper to extract and validate JWT from Authorization header"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    return auth_controller.get_token_data(authorization.split(" ")[1])


@router.get("", summary="Get all review cycles")
def get_all_cycles(authorization: Optional[str] = Header(None)):
    """Returns all review cycles. Accessible by all roles."""
    get_current_user(authorization)  # Just verify they are logged in
    data = cycle_service.get_all_cycles()
    return success_response(data=data)


@router.post("", summary="Create a new review cycle (HR Admin only)")
def create_cycle(body: CreateCycleDTO, authorization: Optional[str] = Header(None)):
    """Creates a new review cycle. Only HR Admin can do this."""
    user = get_current_user(authorization)
    
    # Role check: Only hr_admin can create cycles
    if user.get("role") != "hr_admin":
        raise HTTPException(status_code=403, detail="Only HR Admin can create review cycles")

    try:
        result = cycle_service.create_cycle(
            name=body.name,
            start_date=body.start_date,
            end_date=body.end_date,
            self_due_date=body.self_due_date,
            manager_due_date=body.manager_due_date,
            created_by=user["user_id"]
        )
        return success_response(data=result, message="Review cycle created")
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e.message))


@router.put("/{cycle_id}", summary="Update a review cycle (HR Admin only)")
def update_cycle(cycle_id: int, body: UpdateCycleDTO,
                 authorization: Optional[str] = Header(None)):
    """Updates cycle dates or status."""
    user = get_current_user(authorization)
    if user.get("role") != "hr_admin":
        raise HTTPException(status_code=403, detail="Only HR Admin can update cycles")

    try:
        result = cycle_service.update_cycle(
            cycle_id=cycle_id,
            updates=body.model_dump(exclude_none=True)
        )
        return success_response(data=result, message="Cycle updated")
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.message))
    except ValidationException as e:
        raise HTTPException(status_code=400, detail=str(e.message))


@router.get("/{cycle_id}/progress", summary="Get cycle completion progress (HR Admin)")
def get_progress(cycle_id: int, authorization: Optional[str] = Header(None)):
    """Returns completion percentage for a review cycle."""
    user = get_current_user(authorization)
    if user.get("role") != "hr_admin":
        raise HTTPException(status_code=403, detail="Only HR Admin can view progress")

    try:
        data = cycle_service.get_progress(cycle_id)
        return success_response(data=data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.message))