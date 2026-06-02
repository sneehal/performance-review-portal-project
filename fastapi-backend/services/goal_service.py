# goal_service.py

from dao.goal_dao import GoalDAO
from dao.review_cycle_dao import ReviewCycleDAO
from utils.exceptions import ValidationException, NotFoundException, UnauthorizedException

goal_dao = GoalDAO()
cycle_dao = ReviewCycleDAO()


class GoalService:

    def get_my_goals(self, user_id: int, cycle_id: int = None) -> list:
        return goal_dao.get_user_goals(user_id, cycle_id)

    def create_goal(self, user_id: int, cycle_id: int, title: str,
                    description: str, weight: float, target: str) -> dict:
        """
        Creates a new goal.
        Business rules:
        1. Cycle must exist and be Active
        2. New weight + existing total must not exceed 100%
        """
        # Rule 1: Cycle must be Active
        cycle = cycle_dao.get_by_id(cycle_id)
        if not cycle:
            raise NotFoundException(f"Review cycle {cycle_id} not found")
        if cycle["status"] != "Active":
            raise ValidationException("Goals can only be added to Active review cycles")

        # Rule 2: Weight validation
        current_total = goal_dao.get_total_weight(user_id, cycle_id)
        if current_total + weight > 100:
            remaining = 100 - current_total
            raise ValidationException(
                f"Weight exceeds 100%. You can assign maximum {remaining:.2f}% more"
            )

        goal_id = goal_dao.create_goal(
            user_id=user_id,
            cycle_id=cycle_id,
            title=title,
            description=description,
            weight=weight,
            target=target
        )
        return {"goal_id": goal_id, "message": "Goal created successfully"}

    def update_goal(self, goal_id: int, user_id: int, updates: dict) -> dict:
        """Updates a goal. User can only edit their own goals."""
        goal = goal_dao.get_goal_by_id(goal_id)
        if not goal:
            raise NotFoundException(f"Goal {goal_id} not found")
        if goal["user_id"] != user_id:
            raise UnauthorizedException("You can only edit your own goals")

        # If weight is being updated, validate new total
        if "weight" in updates and updates["weight"] is not None:
            current_total = goal_dao.get_total_weight(user_id, goal["cycle_id"])
            new_total = current_total - goal["weight"] + updates["weight"]
            if new_total > 100:
                raise ValidationException(f"Total weight would exceed 100% (current: {current_total}%)")

        allowed = {"title", "description", "weight", "target"}
        filtered = {k: v for k, v in updates.items() if k in allowed and v is not None}

        goal_dao.update_goal(goal_id, user_id, filtered)
        return {"message": "Goal updated successfully"}

    def record_achievement(self, goal_id: int, user_id: int, achievement: str) -> dict:
        """Records actual achievement for a goal at review time"""
        goal = goal_dao.get_goal_by_id(goal_id)
        if not goal:
            raise NotFoundException(f"Goal {goal_id} not found")
        if goal["user_id"] != user_id:
            raise UnauthorizedException("You can only update your own goals")

        goal_dao.update_achievement(goal_id, user_id, achievement)
        return {"message": "Achievement recorded successfully"}