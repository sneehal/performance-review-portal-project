# review_cycle_service.py

from dao.review_cycle_dao import ReviewCycleDAO
from utils.exceptions import NotFoundException, ValidationException

cycle_dao = ReviewCycleDAO()


class ReviewCycleService:

    def get_all_cycles(self) -> list:
        return cycle_dao.get_all_cycles()

    def get_cycle_by_id(self, cycle_id: int) -> dict:
        cycle = cycle_dao.get_by_id(cycle_id)
        if not cycle:
            raise NotFoundException(f"Review cycle {cycle_id} not found")
        return cycle

    def create_cycle(self, name: str, start_date, end_date,
                     self_due_date, manager_due_date, created_by: int) -> dict:
        """
        Creates a new review cycle.
        Business rule: self_due_date must be before end_date
        """
        if self_due_date >= end_date:
            raise ValidationException("Self-assessment deadline must be before cycle end date")
        if manager_due_date >= end_date:
            raise ValidationException("Manager review deadline must be before cycle end date")
        if start_date >= end_date:
            raise ValidationException("Start date must be before end date")

        cycle_id = cycle_dao.create_cycle(
            name=name,
            start_date=start_date,
            end_date=end_date,
            self_due_date=self_due_date,
            manager_due_date=manager_due_date,
            created_by=created_by
        )
        return {"cycle_id": cycle_id, "message": "Review cycle created successfully"}

    def update_cycle(self, cycle_id: int, updates: dict) -> dict:
        """Updates allowed fields in a review cycle"""
        # Verify cycle exists first
        existing = cycle_dao.get_by_id(cycle_id)
        if not existing:
            raise NotFoundException(f"Review cycle {cycle_id} not found")

        # Only allow these fields to be updated
        allowed_fields = {"name", "start_date", "end_date",
                          "self_due_date", "manager_due_date", "status"}
        filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields and v is not None}

        if not filtered_updates:
            raise ValidationException("No valid fields provided for update")

        cycle_dao.update_cycle(cycle_id, filtered_updates)
        return {"message": "Review cycle updated successfully"}

    def get_progress(self, cycle_id: int) -> dict:
        existing = cycle_dao.get_by_id(cycle_id)
        if not existing:
            raise NotFoundException(f"Review cycle {cycle_id} not found")
        return cycle_dao.get_cycle_progress(cycle_id)