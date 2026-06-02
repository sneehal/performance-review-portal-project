# admin_service.py

import csv
import io
from dao.admin_dao import AdminDAO

admin_dao = AdminDAO()


class AdminService:

    def get_ratings_summary(self) -> list:
        return admin_dao.get_ratings_summary()

    def get_completion_stats(self) -> list:
        return admin_dao.get_completion_stats()

    def export_to_csv(self) -> str:
        """
        Exports full review data as CSV string.
        HR downloads this for payroll/promotion decisions.
        """
        data = admin_dao.get_export_data()
        if not data:
            return ""

        output = io.StringIO()
        fieldnames = [
            "user_id", "employee_name", "department", "email",
            "cycle_name", "review_status", "overall_rating",
            "recommendation", "feedback_text"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return output.getvalue()