# competency_controller.py
# Handles HTTP requests for competency rating endpoints

from fastapi import HTTPException, status
from services.competency_service import CompetencyService
from utils.exceptions import (
    NotFoundException,
    ValidationException
)

comp_service = CompetencyService()


class CompetencyController:

    def get_all_competencies(self) -> list:
        """
        Handles GET /competencies

        Returns all active competencies defined by HR.
        Used to populate the competency rating form on the frontend.

        Example response:
        [
            {"comp_id": 1, "name": "Communication", "description": "..."},
            {"comp_id": 2, "name": "Technical Skills", "description": "..."}
        ]
        """
        try:
            return comp_service.get_all_competencies()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch competencies: {str(e)}"
            )

    def submit_competency_ratings(
        self,
        review_id: int,
        rated_by: int,
        ratings: list
    ) -> dict:
        """
        Handles POST /competency-ratings

        Saves competency ratings for a review.
        Both employees and managers can rate competencies separately.
        Results are later compared side by side.

        Example ratings input:
        [
            {"comp_id": 1, "score": 4.0, "comment": "Good communicator"},
            {"comp_id": 2, "score": 3.5, "comment": "Solid technical skills"}
        ]
        """
        try:
            return comp_service.submit_ratings(
                review_id=review_id,
                rated_by=rated_by,
                ratings=ratings
            )
        except ValidationException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save competency ratings: {str(e)}"
            )

    def get_competency_ratings(self, review_id: int) -> list:
        """
        Handles GET /competency-ratings/{review_id}

        Returns all competency scores for a specific review.
        Used to render the radar/bar chart comparison on the frontend.
        """
        try:
            return comp_service.get_ratings(review_id=review_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch competency ratings: {str(e)}"
            )