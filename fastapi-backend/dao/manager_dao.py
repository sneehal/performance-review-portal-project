# manager_dao.py
# Fixed Oracle reserved word issues

import oracledb
from db import get_connection, release_connection
from utils.db_utils import read_lob, safe_int, safe_float, safe_str, safe_date
from typing import List, Optional


class ManagerDAO:

    def get_pending_reviews(self, manager_id: int) -> List[dict]:
        """Gets submitted self-assessments waiting for manager review"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT r.review_id,
                       u.user_id,
                       u.name        AS employee_name,
                       u.department,
                       rc.name       AS cycle_name,
                       rc.cycle_id,
                       r.status,
                       r.submitted_at
                FROM REVIEWS r
                JOIN USERS u          ON r.user_id  = u.user_id
                JOIN REVIEW_CYCLES rc ON r.cycle_id = rc.cycle_id
                WHERE u.manager_id = :manager_id
                  AND r.type     = 'SELF'
                  AND r.status   = 'Submitted'
                ORDER BY r.submitted_at ASC
                """,
                {"manager_id": manager_id}
            )
            rows = cursor.fetchall()
            return [
                {
                    "review_id":     safe_int(row[0]),
                    "user_id":       safe_int(row[1]),
                    "employee_name": safe_str(row[2]),
                    "department":    safe_str(row[3]),
                    "cycle_name":    safe_str(row[4]),
                    "cycle_id":      safe_int(row[5]),
                    "status":        safe_str(row[6]),
                    "submitted_at":  safe_date(row[7])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_pending_reviews error: {e}")
            raise e
        finally:
            release_connection(conn)

    def insert_feedback(
        self,
        review_id: int,
        reviewer_id: int,
        feedback_text: str,
        overall_rating: float,
        recommendation: Optional[str]
    ) -> int:
        """Saves manager feedback and marks review as Completed"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT seq_feedback.NEXTVAL FROM DUAL")
            new_feedback_id = int(cursor.fetchone()[0])

            cursor.execute(
                """
                INSERT INTO FEEDBACK
                    (feedback_id, review_id, reviewer_id,
                     feedback_text, overall_rating, recommendation)
                VALUES
                    (:feedback_id, :review_id, :reviewer_id,
                     :feedback_text, :overall_rating, :recommendation)
                """,
                {
                    "feedback_id":    new_feedback_id,
                    "review_id":      review_id,
                    "reviewer_id":    reviewer_id,
                    "feedback_text":  feedback_text,
                    "overall_rating": overall_rating,
                    "recommendation": recommendation
                }
            )

            # Mark review as Completed
            cursor.execute(
                """
                UPDATE REVIEWS
                SET status = 'Completed'
                WHERE review_id = :review_id
                """,
                {"review_id": review_id}
            )

            conn.commit()
            return new_feedback_id

        except Exception as e:
            conn.rollback()
            print(f"❌ insert_feedback error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_team_summary(self, manager_id: int) -> List[dict]:
        """Returns rating summary for all team members"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT u.user_id,
                       u.name,
                       u.department,
                       f.overall_rating,
                       f.recommendation,
                       rc.name    AS cycle_name,
                       r.status AS review_status
                FROM USERS u
                LEFT JOIN REVIEWS r
                    ON r.user_id  = u.user_id
                   AND r.type   = 'SELF'
                LEFT JOIN FEEDBACK f
                    ON f.review_id = r.review_id
                LEFT JOIN REVIEW_CYCLES rc
                    ON rc.cycle_id = r.cycle_id
                WHERE u.manager_id = :manager_id
                  AND u.is_active  = 1
                ORDER BY f.overall_rating DESC NULLS LAST
                """,
                {"manager_id": manager_id}
            )
            rows = cursor.fetchall()
            return [
                {
                    "user_id":        safe_int(row[0]),
                    "name":           safe_str(row[1]),
                    "department":     safe_str(row[2]),
                    "overall_rating": safe_float(row[3]),
                    "recommendation": safe_str(row[4]),
                    "cycle_name":     safe_str(row[5]),
                    "review_status":  safe_str(row[6])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_team_summary error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_comparison_data(self, review_id: int) -> dict:
        """Returns self vs manager rating comparison per goal"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT g.goal_id,
                       g.title,
                       g.weight,
                       self_r.score          AS self_score,
                       self_r.self_comment      AS self_comment,
                       mgr_r.score           AS manager_score,
                       mgr_r.self_comment       AS manager_comment
                FROM GOALS g
                JOIN RATINGS self_r
                    ON self_r.goal_id   = g.goal_id
                   AND self_r.review_id = :review_id
                LEFT JOIN REVIEWS mgr_rev
                    ON mgr_rev.user_id  = (
                           SELECT user_id FROM REVIEWS
                           WHERE review_id = :review_id
                       )
                   AND mgr_rev.type   = 'MANAGER'
                   AND mgr_rev.cycle_id = (
                           SELECT cycle_id FROM REVIEWS
                           WHERE review_id = :review_id
                       )
                LEFT JOIN RATINGS mgr_r
                    ON mgr_r.goal_id   = g.goal_id
                   AND mgr_r.review_id = mgr_rev.review_id
                ORDER BY g.goal_id
                """,
                {"review_id": review_id}
            )
            rows = cursor.fetchall()
            return {
                "review_id": review_id,
                "goals": [
                    {
                        "goal_id":          safe_int(row[0]),
                        "title":            safe_str(row[1]),
                        "weight":           safe_float(row[2]),
                        "self_score":       safe_float(row[3]),
                        "self_comment":     safe_str(row[4]),
                        "manager_score":    safe_float(row[5]),
                        "manager_comment":  safe_str(row[6])
                    }
                    for row in rows
                ]
            }

        except Exception as e:
            print(f"❌ get_comparison_data error: {e}")
            raise e
        finally:
            release_connection(conn)