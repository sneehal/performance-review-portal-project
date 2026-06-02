# review_controller.py
# Handles HTTP requests for employee self-assessment endpoints
# This is the MAIN controller for employee review workflow

from fastapi import HTTPException, status
from services.review_service import ReviewService
from utils.exceptions import (
    NotFoundException,
    ValidationException,
    ConflictException,
    UnauthorizedException
)

review_service = ReviewService()


class ReviewController:

    def get_my_review(self, user_id: int, cycle_id: int) -> dict:
        """
        Handles GET /reviews/my/{cycle_id}
        Returns the employee's self-assessment review for a given cycle.
        Includes all goal ratings inside.

        Example response:
        {
            "review_id": 1,
            "status": "Draft",
            "overall_comment": "...",
            "ratings": [
                {"goal_id": 1, "score": 4.0, "comment": "..."}
            ]
        }
        """
        try:
            return review_service.get_my_review(
                user_id=user_id,
                cycle_id=cycle_id
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch review: {str(e)}"
            )

    def submit_self_assessment(
        self,
        user_id: int,
        cycle_id: int,
        overall_comment: str,
        ratings: list
    ) -> dict:
        """
        Handles POST /reviews/self-assessment

        This is the CORE employee self-assessment endpoint.
        Employee rates themselves on each goal and writes comments.

        Flow:
        1. Validates cycle is Active and deadline not passed
        2. Checks for duplicate submission
        3. Creates REVIEWS record with status = Draft
        4. Inserts all goal RATINGS
        5. Returns review_id

        After calling this, employee must call PUT /reviews/{id}/submit
        to change status from Draft to Submitted.
        """
        try:
            return review_service.submit_self_assessment(
                user_id=user_id,
                cycle_id=cycle_id,
                overall_comment=overall_comment,
                ratings=ratings
            )
        except ConflictException as e:
            # Employee already submitted for this cycle
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.message
            )
        except ValidationException as e:
            # Cycle not active, deadline passed, etc.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to submit self-assessment: {str(e)}"
            )

    def submit_review(self, review_id: int, user_id: int) -> dict:
        """
        Handles PUT /reviews/{review_id}/submit

        Changes review status from Draft to Submitted.
        Once submitted, the manager can see it in their pending reviews.

        Business rule:
        - Only the owner of the review can submit it
        - Review must be in Draft status
        """
        try:
            return review_service.submit_review(
                review_id=review_id,
                user_id=user_id
            )
        except ValidationException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to submit review: {str(e)}"
            )

    def get_review_history(self, user_id: int) -> list:
        """
        Handles GET /reviews/history
        Returns all past reviews for the employee across all cycles.
        Used in the My Review History page.
        """
        try:
            return review_service.get_review_history(user_id=user_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch review history: {str(e)}"
            )

    def get_review_with_ratings(self, review_id: int, user_id: int) -> dict:
        """
        Handles GET /reviews/{review_id}
        Returns full review details including all goal ratings.
        Employee can only view their own reviews.
        """
        try:
            return review_service.get_review_with_ratings(
                review_id=review_id,
                user_id=user_id
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.message
            )
        except UnauthorizedException as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch review details: {str(e)}"
            )