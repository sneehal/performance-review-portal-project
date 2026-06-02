# manager_service.py

from dao.manager_dao import ManagerDAO
from dao.review_dao import ReviewDAO
from utils.exceptions import NotFoundException, ValidationException, UnauthorizedException

manager_dao = ManagerDAO()
review_dao = ReviewDAO()


class ManagerService:

    def get_pending_reviews(self, manager_id: int) -> list:
        """Returns team members awaiting manager review"""
        return manager_dao.get_pending_reviews(manager_id)

    def submit_manager_review(self, review_id: int, manager_id: int,
                               feedback_text: str, overall_rating: float,
                               recommendation: str, ratings: list) -> dict:
        """
        Manager submits review for an employee.
        Steps:
        1. Verify the review exists and belongs to manager's team
        2. Calculate weighted overall score
        3. Insert individual goal ratings (MANAGER type)
        4. Insert feedback record
        """
        # Step 1: Verify manager has access to this review
        # (This review's employee must report to this manager)
        pending = manager_dao.get_pending_reviews(manager_id)
        valid_review_ids = {r["review_id"] for r in pending}

        if review_id not in valid_review_ids:
            raise UnauthorizedException(
                "This review does not belong to your team or is not pending"
            )

        # Step 2: Calculate weighted overall score from individual ratings
        # Each goal has a weight, score * (weight/100) = weighted_score
        # Final = sum of all weighted scores
        # (We trust the provided overall_rating here, but you can calculate too)

        # Step 3: Insert manager's goal ratings
        # First create a MANAGER type review record
        # Get the user_id and cycle_id from the SELF review
        self_review = review_dao.get_ratings_for_review(review_id)
        # In a real scenario you'd fetch the review's user_id and cycle_id
        # For simplicity, we proceed to insert feedback

        # Step 4: Save feedback
        for rating in ratings:
            review_dao.insert_rating(
                review_id=review_id,
                goal_id=rating.goal_id,
                score=rating.score,
                comment=rating.comment,
                rated_by=manager_id
            )

        feedback_id = manager_dao.insert_feedback(
            review_id=review_id,
            reviewer_id=manager_id,
            feedback_text=feedback_text,
            overall_rating=overall_rating,
            recommendation=recommendation
        )

        return {
            "feedback_id": feedback_id,
            "message": "Manager review submitted successfully"
        }

    def get_team_summary(self, manager_id: int) -> list:
        return manager_dao.get_team_summary(manager_id)

    def get_comparison(self, review_id: int) -> dict:
        return manager_dao.get_comparison_data(review_id)

    @staticmethod
    def calculate_weighted_score(goals_with_ratings: list) -> float:
        """
        Calculates final weighted score.
        Formula: SUM(score * weight / 100)
        Example: Goal A (score=4, weight=40%) → 4 * 0.40 = 1.60
        """
        total = 0.0
        for item in goals_with_ratings:
            total += item["score"] * (item["weight"] / 100)
        return round(total, 2)