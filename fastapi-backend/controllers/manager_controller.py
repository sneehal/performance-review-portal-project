# manager_controller.py
# Handles HTTP requests for manager review endpoints

from fastapi import HTTPException, status
from services.manager_service import ManagerService
from utils.exceptions import (
    NotFoundException,
    ValidationException,
    UnauthorizedException
)

manager_service = ManagerService()


class ManagerController:

    def get_pending_reviews(self, manager_id: int, user_role: str) -> list:
        """
        Handles GET /manager/pending-reviews

        Returns all team members who have submitted their self-assessment
        and are waiting for the manager to review them.

        Only managers and hr_admin can access this.
        """
        if user_role not in ("manager", "hr_admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Managers can view pending reviews"
            )

        try:
            return manager_service.get_pending_reviews(
                manager_id=manager_id
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch pending reviews: {str(e)}"
            )

    def submit_manager_review(
        self,
        review_id: int,
        manager_id: int,
        user_role: str,
        feedback_text: str,
        overall_rating: float,
        recommendation: str,
        ratings: list
    ) -> dict:
        """
        Handles POST /manager/review/{review_id}

        Manager rates each goal and provides overall feedback.
        This completes the review process for that employee.

        Flow:
        1. Validates manager has access to this review
        2. Inserts manager goal ratings into RATINGS table
        3. Creates FEEDBACK record with overall rating
        4. Updates review status to Completed
        """
        if user_role not in ("manager", "hr_admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Managers can submit reviews"
            )

        try:
            return manager_service.submit_manager_review(
                review_id=review_id,
                manager_id=manager_id,
                feedback_text=feedback_text,
                overall_rating=overall_rating,
                recommendation=recommendation,
                ratings=ratings
            )
        except UnauthorizedException as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=e.message
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
                detail=f"Failed to submit manager review: {str(e)}"
            )

    def get_team_summary(self, manager_id: int, user_role: str) -> list:
        """
        Handles GET /manager/team-summary

        Returns overall rating summary for all team members.
        Shows who is reviewed, who is pending, and average scores.
        """
        if user_role not in ("manager", "hr_admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Managers can view team summary"
            )

        try:
            return manager_service.get_team_summary(
                manager_id=manager_id
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch team summary: {str(e)}"
            )

    def get_comparison(self, review_id: int, user_role: str) -> dict:
        """
        Handles GET /manager/compare/{review_id}

        Returns side-by-side comparison:
        - Employee's self-rating vs Manager's rating for each goal
        - Helps manager identify where perception gaps exist
        """
        if user_role not in ("manager", "hr_admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Managers can view rating comparison"
            )

        try:
            return manager_service.get_comparison(
                review_id=review_id
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch comparison: {str(e)}"
            )