# goal_routes.py

from fastapi import APIRouter, Header, HTTPException
from typing import Optional
from dto.goal_dto import CreateGoalDTO, UpdateGoalDTO, UpdateAchievementDTO
from controllers.auth_controller import AuthController
from controllers.goal_controller import GoalController
from utils.response_utils import success_response

router = APIRouter(prefix="/goals", tags=["Goals"])
auth_controller = AuthController()
goal_controller = GoalController()


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    return auth_controller.get_token_data(authorization.split(" ")[1])


@router.get("/my", summary="Get my goals")
def get_my_goals(cycle_id: Optional[int] = None,
                 authorization: Optional[str] = Header(None)):
    """
    Returns current user's goals.
    Optionally filter by cycle_id query parameter.
    Example: GET /goals/my?cycle_id=1
    """
    user = get_current_user(authorization)
    data = goal_controller.get_my_goals(user["user_id"], cycle_id)
    return success_response(data=data)


@router.post("", summary="Create a new goal")
def create_goal(body: CreateGoalDTO, authorization: Optional[str] = Header(None)):
    """Creates a new goal for the logged-in employee."""
    user = get_current_user(authorization)
    result = goal_controller.create_goal(
        user_id=user["user_id"],
        cycle_id=body.cycle_id,
        title=body.title,
        description=body.description,
        weight=body.weight,
        target=body.target
    )
    return success_response(data=result, message="Goal created")


@router.put("/{goal_id}", summary="Update a goal")
def update_goal(goal_id: int, body: UpdateGoalDTO,
                authorization: Optional[str] = Header(None)):
    """Updates an existing goal. Users can only edit their own goals."""
    user = get_current_user(authorization)
    result = goal_controller.update_goal(
        goal_id=goal_id,
        user_id=user["user_id"],
        updates=body.model_dump(exclude_none=True)
    )
    return success_response(data=result, message="Goal updated")


@router.put("/{goal_id}/achievement", summary="Record goal achievement")
def update_achievement(goal_id: int, body: UpdateAchievementDTO,
                       authorization: Optional[str] = Header(None)):
    """Records what the employee actually achieved for a goal."""
    user = get_current_user(authorization)
    result = goal_controller.record_achievement(
        goal_id=goal_id,
        user_id=user["user_id"],
        achievement=body.achievement
    )
    return success_response(data=result, message="Achievement recorded")