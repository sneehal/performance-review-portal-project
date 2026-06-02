# goal_controller.py

from fastapi import HTTPException, status
from services.goal_service import GoalService
from utils.exceptions import ValidationException, NotFoundException, UnauthorizedException

goal_service = GoalService()


class GoalController:

    def get_my_goals(self, user_id: int, cycle_id: int = None) -> list:
        try:
            return goal_service.get_my_goals(user_id, cycle_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch goals"
            )

    def create_goal(self, user_id: int, cycle_id: int, title: str,
                    description: str, weight: float, target: str) -> dict:
        try:
            return goal_service.create_goal(user_id, cycle_id, title, description, weight, target)
        except (ValidationException, NotFoundException) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create goal"
            )

    def update_goal(self, goal_id: int, user_id: int, updates: dict) -> dict:
        try:
            return goal_service.update_goal(goal_id, user_id, updates)
        except NotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.message))
        except UnauthorizedException as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.message))
        except ValidationException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))

    def record_achievement(self, goal_id: int, user_id: int, achievement: str) -> dict:
        try:
            return goal_service.record_achievement(goal_id, user_id, achievement)
        except (NotFoundException, UnauthorizedException) as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.message))