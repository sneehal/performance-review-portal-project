# competency_service.py

from dao.competency_dao import CompetencyDAO
from utils.exceptions import ValidationException

comp_dao = CompetencyDAO()


class CompetencyService:

    def get_all_competencies(self) -> list:
        return comp_dao.get_active_competencies()

    def submit_ratings(self, review_id: int, rated_by: int, ratings: list) -> dict:
        """
        Submits competency ratings for a review.
        Each competency gets a score 1-5.
        """
        if not ratings:
            raise ValidationException("No ratings provided")

        for rating in ratings:
            comp_dao.insert_competency_rating(
                review_id=review_id,
                comp_id=rating.comp_id,
                score=rating.score,
                rated_by=rated_by,
                feedback_comment=rating.feedback_comment
            )

        return {"message": f"{len(ratings)} competency ratings saved successfully"}

    def get_ratings(self, review_id: int) -> list:
        return comp_dao.get_ratings_for_review(review_id)