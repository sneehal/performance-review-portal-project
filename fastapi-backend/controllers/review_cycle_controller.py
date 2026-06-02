# review_cycle_controller.py
# Handles HTTP request/response for review cycle endpoints
# Calls service layer and maps exceptions to HTTP status codes

from fastapi import HTTPException, status
from services.review_cycle_service import ReviewCycleService
from utils.exceptions import (
    NotFoundException,
    ValidationException,
    UnauthorizedException
)

# Single instance used by the route
cycle_service = ReviewCycleService()


class ReviewCycleController:

    def get_all_cycles(self) -> list:
        """
        Handles GET /review-cycles
        Returns all review cycles from the database.
        """
        try:
            return cycle_service.get_all_cycles()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch review cycles: {str(e)}"
            )

    def get_cycle_by_id(self, cycle_id: int) -> dict:
        """
        Handles GET /review-cycles/{cycle_id}
        Returns a single review cycle by its ID.
        """
        try:
            return cycle_service.get_cycle_by_id(cycle_id)
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch cycle: {str(e)}"
            )

    def create_cycle(
        self,
        name: str,
        start_date,
        end_date,
        self_due_date,
        manager_due_date,
        created_by: int,
        user_role: str
    ) -> dict:
        """
        Handles POST /review-cycles
        Only HR Admin can create a review cycle.
        """
        # Role check happens here in controller
        if user_role != "hr_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only HR Admin can create review cycles"
            )

        try:
            return cycle_service.create_cycle(
                name=name,
                start_date=start_date,
                end_date=end_date,
                self_due_date=self_due_date,
                manager_due_date=manager_due_date,
                created_by=created_by
            )
        except ValidationException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create cycle: {str(e)}"
            )

    def update_cycle(
        self,
        cycle_id: int,
        updates: dict,
        user_role: str
    ) -> dict:
        """
        Handles PUT /review-cycles/{cycle_id}
        Updates allowed fields. Only HR Admin can update.
        """
        if user_role != "hr_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only HR Admin can update review cycles"
            )

        try:
            return cycle_service.update_cycle(
                cycle_id=cycle_id,
                updates=updates
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except ValidationException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update cycle: {str(e)}"
            )

    def get_cycle_progress(
        self,
        cycle_id: int,
        user_role: str
    ) -> dict:
        """
        Handles GET /review-cycles/{cycle_id}/progress
        Returns completion percentage for a review cycle.
        Only HR Admin can view this.
        """
        if user_role != "hr_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only HR Admin can view cycle progress"
            )

        try:
            return cycle_service.get_progress(cycle_id)
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch progress: {str(e)}"
            )