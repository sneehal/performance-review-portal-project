# review_dao.py
# Fixed Oracle reserved word issues
# 'comment', 'type', 'status' need double quotes in SQL

import oracledb
from db import get_connection, release_connection
from utils.db_utils import read_lob, safe_int, safe_float, safe_str, safe_date
from typing import Optional, List


class ReviewDAO:

    def check_duplicate_review(
        self,
        user_id: int,
        cycle_id: int,
        review_type: str
    ) -> bool:
        """Checks if a review already exists for this user+cycle+type"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM REVIEWS
                WHERE user_id  = :user_id
                  AND cycle_id = :cycle_id
                  AND "type"   = :review_type
                """,
                {
                    "user_id":     user_id,
                    "cycle_id":    cycle_id,
                    "review_type": review_type
                }
            )
            return int(cursor.fetchone()[0]) > 0

        except Exception as e:
            print(f"❌ check_duplicate_review error: {e}")
            raise e
        finally:
            release_connection(conn)

    def create_review(
        self,
        user_id: int,
        cycle_id: int,
        review_type: str,
        overall_comment: Optional[str]
    ) -> int:
        """Creates a REVIEWS record with status Draft"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT seq_reviews.NEXTVAL FROM DUAL")
            new_review_id = int(cursor.fetchone()[0])

            cursor.execute(
                """
                INSERT INTO REVIEWS
                    (review_id, user_id, cycle_id, "type",
                     "status", overall_comment)
                VALUES
                    (:review_id, :user_id, :cycle_id, :review_type,
                     'Draft', :overall_comment)
                """,
                {
                    "review_id":       new_review_id,
                    "user_id":         user_id,
                    "cycle_id":        cycle_id,
                    "review_type":     review_type,
                    "overall_comment": overall_comment
                }
            )
            conn.commit()
            return new_review_id

        except Exception as e:
            conn.rollback()
            print(f"❌ create_review error: {e}")
            raise e
        finally:
            release_connection(conn)

    def insert_rating(
        self,
        review_id: int,
        goal_id: int,
        score: float,
        comment: Optional[str],
        rated_by: int
    ):
        """Inserts a single goal rating"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT seq_ratings.NEXTVAL FROM DUAL")
            new_rating_id = int(cursor.fetchone()[0])

            cursor.execute(
                """
                INSERT INTO RATINGS
                    (rating_id, review_id, goal_id,
                     score, "comment", rated_by)
                VALUES
                    (:rating_id, :review_id, :goal_id,
                     :score, :comment, :rated_by)
                """,
                {
                    "rating_id": new_rating_id,
                    "review_id": review_id,
                    "goal_id":   goal_id,
                    "score":     score,
                    "comment":   comment,
                    "rated_by":  rated_by
                }
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"❌ insert_rating error: {e}")
            raise e
        finally:
            release_connection(conn)

    def submit_review(self, review_id: int, user_id: int) -> bool:
        """Changes status from Draft to Submitted"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE REVIEWS
                SET "status"     = 'Submitted',
                    submitted_at = CURRENT_TIMESTAMP
                WHERE review_id  = :review_id
                  AND user_id    = :user_id
                  AND "status"   = 'Draft'
                """,
                {"review_id": review_id, "user_id": user_id}
            )
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            print(f"❌ submit_review error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_review_by_cycle(
        self,
        user_id: int,
        cycle_id: int
    ) -> Optional[dict]:
        """Gets employee SELF review for a specific cycle"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT review_id,
                       user_id,
                       cycle_id,
                       type,
                       status,
                       overall_comment,
                       submitted_at,
                       created_at
                FROM REVIEWS
                WHERE user_id  = :user_id
                  AND cycle_id = :cycle_id
                  AND type   = 'SELF'
                """,
                {"user_id": user_id, "cycle_id": cycle_id}
            )
            row = cursor.fetchone()
            if not row:
                return None
            return self._review_row_to_dict(row)

        except Exception as e:
            print(f"❌ get_review_by_cycle error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_review_by_id(self, review_id: int) -> Optional[dict]:
        """Gets a single review by ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT review_id,
                       user_id,
                       cycle_id,
                       type,
                       status,
                       overall_comment,
                       submitted_at,
                       created_at
                FROM REVIEWS
                WHERE review_id = :review_id
                """,
                {"review_id": review_id}
            )
            row = cursor.fetchone()
            if not row:
                return None
            return self._review_row_to_dict(row)

        except Exception as e:
            print(f"❌ get_review_by_id error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_ratings_for_review(self, review_id: int) -> List[dict]:
        """
        Gets all goal ratings for a review.
        'comment' is Oracle reserved word — must use double quotes.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT r.rating_id,
                       r.goal_id,
                       g.title,
                       r.score,
                       r.self_comment,
                       r.rated_by
                FROM RATINGS r
                JOIN GOALS g ON r.goal_id = g.goal_id
                WHERE r.review_id = :review_id
                ORDER BY r.goal_id
                """,
                {"review_id": review_id}
            )
            rows = cursor.fetchall()
            return [
                {
                    "rating_id":  safe_int(row[0]),
                    "goal_id":    safe_int(row[1]),
                    "goal_title": safe_str(row[2]),
                    "score":      safe_float(row[3]),
                    "feedback_comment":    safe_str(row[4]),
                    "rated_by":   safe_int(row[5])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_ratings_for_review error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_all_reviews_for_user(self, user_id: int) -> List[dict]:
        """Gets all reviews across all cycles for a user"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT r.review_id,
                       r.cycle_id,
                       rc.name   AS cycle_name,
                       r."type",
                       r."status",
                       r.overall_comment,
                       r.submitted_at,
                       r.created_at
                FROM REVIEWS r
                JOIN REVIEW_CYCLES rc ON r.cycle_id = rc.cycle_id
                WHERE r.user_id = :user_id
                ORDER BY r.created_at DESC
                """,
                {"user_id": user_id}
            )
            rows = cursor.fetchall()
            return [
                {
                    "review_id":       safe_int(row[0]),
                    "cycle_id":        safe_int(row[1]),
                    "cycle_name":      safe_str(row[2]),
                    "type":            safe_str(row[3]),
                    "status":          safe_str(row[4]),
                    "overall_comment": read_lob(row[5]),
                    "submitted_at":    safe_date(row[6]),
                    "created_at":      safe_date(row[7])
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_all_reviews_for_user error: {e}")
            raise e
        finally:
            release_connection(conn)

    def _review_row_to_dict(self, row) -> dict:
        """
        Converts REVIEWS table row to dict.
        overall_comment is CLOB.
        type and status need double quotes in SQL
        but are returned as normal strings here.
        """
        return {
            "review_id":       safe_int(row[0]),
            "user_id":         safe_int(row[1]),
            "cycle_id":        safe_int(row[2]),
            "type":            safe_str(row[3]),
            "status":          safe_str(row[4]),
            "overall_comment": read_lob(row[5]),
            "submitted_at":    safe_date(row[6]),
            "created_at":      safe_date(row[7])
        }