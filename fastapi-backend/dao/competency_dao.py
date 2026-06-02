# competency_dao.py
# Fixed Oracle reserved word issues for 'comment' column

import oracledb
from db import get_connection, release_connection
from utils.db_utils import safe_int, safe_float, safe_str
from typing import List, Optional


class CompetencyDAO:

    def get_active_competencies(self) -> List[dict]:
        """Returns all active competencies"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT comp_id,
                       name,
                       description,
                       is_active
                FROM COMPETENCIES
                WHERE is_active = 1
                ORDER BY comp_id
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    "comp_id":     safe_int(row[0]),
                    "name":        safe_str(row[1]),
                    "description": safe_str(row[2]),
                    "is_active":   safe_int(row[3])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_active_competencies error: {e}")
            raise e
        finally:
            release_connection(conn)

    def insert_competency_rating(
        self,
        review_id: int,
        comp_id: int,
        score: float,
        rated_by: int,
        feedback_comment: Optional[str]
    ):
        """Inserts a single competency rating"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT seq_comp_ratings.NEXTVAL FROM DUAL")
            new_cr_id = int(cursor.fetchone()[0])

            cursor.execute(
                """
                INSERT INTO COMPETENCY_RATINGS
                    (cr_id, review_id, comp_id,
                     score, rated_by, feedback_comment)
                VALUES
                    (:cr_id, :review_id, :comp_id,
                     :score, :rated_by, :feedback_comment)
                """,
                {
                    "cr_id":     new_cr_id,
                    "review_id": review_id,
                    "comp_id":   comp_id,
                    "score":     score,
                    "rated_by":  rated_by,
                    "feedback_comment":   feedback_comment
                }
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"❌ insert_competency_rating error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_ratings_for_review(self, review_id: int) -> List[dict]:
        """Gets all competency ratings for a review"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT cr.cr_id,
                       cr.comp_id,
                       c.name     AS competency_name,
                       cr.score,
                       cr.rated_by,
                       cr.feedback_comment
                FROM COMPETENCY_RATINGS cr
                JOIN COMPETENCIES c ON cr.comp_id = c.comp_id
                WHERE cr.review_id = :review_id
                ORDER BY cr.comp_id
                """,
                {"review_id": review_id}
            )
            rows = cursor.fetchall()
            return [
                {
                    "cr_id":           safe_int(row[0]),
                    "comp_id":         safe_int(row[1]),
                    "competency_name": safe_str(row[2]),
                    "score":           safe_float(row[3]),
                    "rated_by":        safe_int(row[4]),
                    "feedback_comment": safe_str(row[5])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_ratings_for_review error: {e}")
            raise e
        finally:
            release_connection(conn)