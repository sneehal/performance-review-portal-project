# admin_controller.py
# Handles HTTP requests for HR Admin report endpoints

from fastapi import HTTPException, status
from fastapi.responses import PlainTextResponse
from services.admin_service import AdminService
from utils.exceptions import UnauthorizedException

admin_service = AdminService()


class AdminController:

    def _check_hr_role(self, user_role: str):
        """
        Reusable role check for all admin endpoints.
        Only hr_admin can access admin reports.
        """
        if user_role != "hr_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only HR Admin can access reports"
            )

    def get_ratings_summary(self, user_role: str) -> list:
        """
        Handles GET /admin/reports/ratings-summary

        Returns average ratings grouped by department.
        HR uses this to identify which departments are performing well
        and which need attention.

        Example response:
        [
            {
                "department": "Engineering",
                "total_employees": 10,
                "avg_rating": 3.8,
                "promote_count": 3,
                "pip_count": 1
            }
        ]
        """
        self._check_hr_role(user_role)

        try:
            return admin_service.get_ratings_summary()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch ratings summary: {str(e)}"
            )

    def get_completion_stats(self, user_role: str) -> list:
        """
        Handles GET /admin/reports/completion

        Returns submission completion percentage per review cycle.
        HR uses this to track who has and hasn't submitted their assessments.

        Example response:
        [
            {
                "cycle_name": "Q1 2025 Appraisal",
                "total_employees": 20,
                "submitted_count": 15,
                "completion_pct": 75.0
            }
        ]
        """
        self._check_hr_role(user_role)

        try:
            return admin_service.get_completion_stats()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch completion stats: {str(e)}"
            )

    def export_data_as_csv(self, user_role: str):
        """
        Handles GET /admin/reports/export

        Generates and downloads full review data as a CSV file.
        HR uses this for:
        - Payroll processing
        - Promotion decisions
        - Compliance reporting

        Returns a downloadable CSV file response.
        """
        self._check_hr_role(user_role)

        try:
            csv_content = admin_service.export_to_csv()

            if not csv_content:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No data available to export"
                )

            # Return as a downloadable file
            return PlainTextResponse(
                content=csv_content,
                media_type="text/csv",
                headers={
                    "Content-Disposition": "attachment; filename=review_export.csv"
                }
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to export data: {str(e)}"
            )