# admin_dao.py
# Fixed Oracle reserved word issues

from db import get_connection, release_connection
from utils.db_utils import read_lob, safe_int, safe_float, safe_str
from typing import List


class AdminDAO:

    def get_ratings_summary(self) -> List[dict]:
        """Returns average ratings grouped by department"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT u.department,
                       COUNT(DISTINCT u.user_id)                                AS total_employees,
                       ROUND(AVG(f.overall_rating), 2)                          AS avg_rating,
                       COUNT(CASE WHEN f.recommendation = 'Promote' THEN 1 END) AS promote_count,
                       COUNT(CASE WHEN f.recommendation = 'PIP'     THEN 1 END) AS pip_count
                FROM USERS u
                LEFT JOIN REVIEWS r
                    ON r.user_id = u.user_id
                   AND r.type  = 'SELF'
                LEFT JOIN FEEDBACK f
                    ON f.review_id = r.review_id
                WHERE u.role      = 'employee'
                  AND u.is_active = 1
                GROUP BY u.department
                ORDER BY avg_rating DESC NULLS LAST
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "department":      safe_str(row[0]),
                    "total_employees": safe_int(row[1]),
                    "avg_rating":      safe_float(row[2]),
                    "promote_count":   safe_int(row[3]),
                    "pip_count":       safe_int(row[4])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_ratings_summary error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_completion_stats(self) -> List[dict]:
        """Returns submission completion percentage per cycle"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT rc.cycle_id,
                       rc.name,
                       rc.status,
                       (SELECT COUNT(*) FROM USERS
                        WHERE role = 'employee'
                          AND is_active = 1)            AS total_employees,
                       COUNT(DISTINCT CASE
                           WHEN r.status IN ('Submitted','Completed')
                           THEN r.user_id END)          AS submitted_count
                FROM REVIEW_CYCLES rc
                LEFT JOIN REVIEWS r
                    ON r.cycle_id = rc.cycle_id
                   AND r.type   = 'SELF'
                GROUP BY rc.cycle_id, rc.name, rc.status
                ORDER BY rc.cycle_id DESC
                """
            )
            rows = cursor.fetchall()
            result = []
            for row in rows:
                total     = safe_int(row[3]) or 0
                submitted = safe_int(row[4]) or 0
                pct       = round(submitted / total * 100, 2) if total > 0 else 0.0
                result.append({
                    "cycle_id":        safe_int(row[0]),
                    "cycle_name":      safe_str(row[1]),
                    "status":          safe_str(row[2]),
                    "total_employees": total,
                    "submitted_count": submitted,
                    "completion_pct":  pct
                })
            return result

        except Exception as e:
            print(f"❌ get_completion_stats error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_export_data(self) -> List[dict]:
        """Gets full review data for CSV export"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT u.user_id,
                       u.name          AS employee_name,
                       u.department,
                       u.email,
                       rc.name         AS cycle_name,
                       r.status        AS review_status,
                       f.overall_rating,
                       f.recommendation,
                       f.feedback_text
                FROM USERS u
                LEFT JOIN REVIEWS r
                    ON r.user_id = u.user_id
                   AND r.type  = 'SELF'
                LEFT JOIN REVIEW_CYCLES rc
                    ON rc.cycle_id = r.cycle_id
                LEFT JOIN FEEDBACK f
                    ON f.review_id = r.review_id
                WHERE u.role      = 'employee'
                  AND u.is_active = 1
                ORDER BY rc.cycle_id DESC, u.department, u.name
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "user_id":        safe_int(row[0]),
                    "employee_name":  safe_str(row[1]),
                    "department":     safe_str(row[2]),
                    "email":          safe_str(row[3]),
                    "cycle_name":     safe_str(row[4]),
                    "review_status":  safe_str(row[5]),
                    "overall_rating": safe_float(row[6]),
                    "recommendation": safe_str(row[7]),
                    "feedback_text":  read_lob(row[8])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_export_data error: {e}")
            raise e
        finally:
            release_connection(conn)