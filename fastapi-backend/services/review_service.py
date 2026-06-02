# review_service.py
# Added missing methods: get_review_history and get_review_with_ratings

from datetime import date
from dao.review_dao import ReviewDAO
from dao.goal_dao import GoalDAO
from dao.review_cycle_dao import ReviewCycleDAO
from utils.exceptions import (
    ConflictException,
    ValidationException,
    NotFoundException,
    UnauthorizedException
)
from datetime import date, datetime

review_dao = ReviewDAO()
goal_dao = GoalDAO()
cycle_dao = ReviewCycleDAO()


class ReviewService:

    def submit_self_assessment(
        self,
        user_id: int,
        cycle_id: int,
        overall_comment: str,
        ratings: list
    ) -> dict:
        """
        Full self-assessment submission flow.
        Validates, creates review, inserts all ratings.
        """
        # Validate cycle exists and is Active
        cycle = cycle_dao.get_by_id(cycle_id)
        if not cycle:
            raise NotFoundException(f"Review cycle {cycle_id} not found")
        if cycle["status"] != "Active":
            raise ValidationException(
                "Self-assessment can only be submitted for Active cycles"
            )

        # Check deadline
        self_due_value = cycle["self_due_date"]
        print(f"Cycle self_due_date from DB: {self_due_value} (type: {type(self_due_value)})")

        if isinstance(self_due_value, date):
            self_due = self_due_value
        else:
            self_due = datetime.strptime(str(self_due_value).split(" ")[0], "%Y-%m-%d").date()

        if date.today() > self_due:
            print(f"Today's date: {date.today()}, Self due date: {self_due}")
            raise ValidationException(
                f"Self-assessment deadline has passed. Due date was {self_due}"
            )

        # Check duplicate
        if review_dao.check_duplicate_review(user_id, cycle_id, "SELF"):
            raise ConflictException(
                "You have already submitted a self-assessment for this cycle"
            )

        # Validate goals belong to this user and cycle
        my_goals = goal_dao.get_user_goals(user_id, cycle_id)
        my_goal_ids = {g["goal_id"] for g in my_goals}
        for rating in ratings:
            if rating.goal_id not in my_goal_ids:
                raise ValidationException(
                    f"Goal {rating.goal_id} does not belong to you in this cycle"
                )

        # Create review record (Draft status)
        review_id = review_dao.create_review(
            user_id=user_id,
            cycle_id=cycle_id,
            review_type="SELF",
            overall_comment=overall_comment
        )

        # Insert all goal ratings
        for rating in ratings:
            review_dao.insert_rating(
                review_id=review_id,
                goal_id=rating.goal_id,
                score=rating.score,
                comment=rating.comment,
                rated_by=user_id
            )

        return {
            "review_id": review_id,
            "message": "Self-assessment saved as Draft. Call submit to finalize."
        }

    def submit_review(self, review_id: int, user_id: int) -> dict:
        """Changes review status from Draft to Submitted"""
        success = review_dao.submit_review(review_id, user_id)
        if not success:
            raise ValidationException(
                "Cannot submit. Review not found, already submitted, or does not belong to you"
            )
        return {"message": "Review submitted successfully. Your manager can now see it."}

    def get_my_review(self, user_id: int, cycle_id: int) -> dict:
        """Gets employee's review with all ratings for a specific cycle"""
        review = review_dao.get_review_by_cycle(user_id, cycle_id)
        if not review:
            raise NotFoundException(
                f"No review found for cycle {cycle_id}. "
                f"Please submit a self-assessment first."
            )
        # Attach ratings to the review
        ratings = review_dao.get_ratings_for_review(review["review_id"])
        review["ratings"] = ratings
        return review

    def get_review_history(self, user_id: int) -> list:
        """
        Gets all reviews across all cycles for an employee.
        Used in the My Review History page.

        Returns reviews with basic info (no ratings detail).
        For detailed ratings, use get_review_with_ratings.
        """
        reviews = review_dao.get_all_reviews_for_user(user_id)
        return reviews

    def get_review_with_ratings(
        self,
        review_id: int,
        user_id: int
    ) -> dict:
        """
        Gets a complete review with all goal ratings.
        Used when employee clicks on a past review to view details.

        Security: Employee can only view their own reviews.
        """
        review = review_dao.get_review_by_id(review_id)
        if not review:
            raise NotFoundException(f"Review {review_id} not found")

        # Security check: user can only see their own reviews
        if review["user_id"] != user_id:
            raise UnauthorizedException(
                "You can only view your own reviews"
            )

        # Attach ratings
        ratings = review_dao.get_ratings_for_review(review_id)
        review["ratings"] = ratings
        return review