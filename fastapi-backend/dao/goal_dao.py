# goal_dao.py
# Fixed CLOB handling for description field

import oracledb
from db import get_connection, release_connection
from utils.db_utils import read_lob, safe_int, safe_float, safe_str, safe_date
from typing import Optional, List


class GoalDAO:

    def get_user_goals(
        self,
        user_id: int,
        cycle_id: Optional[int] = None
    ) -> List[dict]:
        """
        Gets all goals for a user.
        Handles CLOB description field properly.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()

            if cycle_id is not None:
                cursor.execute(
                    """
                    SELECT goal_id, user_id, cycle_id, title, description,
                           weight, target, achievement, created_at
                    FROM GOALS
                    WHERE user_id  = :user_id
                      AND cycle_id = :cycle_id
                    ORDER BY goal_id
                    """,
                    {"user_id": user_id, "cycle_id": cycle_id}
                )
            else:
                cursor.execute(
                    """
                    SELECT goal_id, user_id, cycle_id, title, description,
                           weight, target, achievement, created_at
                    FROM GOALS
                    WHERE user_id = :user_id
                    ORDER BY cycle_id DESC, goal_id
                    """,
                    {"user_id": user_id}
                )

            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]

        except Exception as e:
            print(f"❌ get_user_goals error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_goal_by_id(self, goal_id: int) -> Optional[dict]:
        """Gets a single goal by its primary key"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT goal_id, user_id, cycle_id, title, description,
                       weight, target, achievement, created_at
                FROM GOALS
                WHERE goal_id = :goal_id
                """,
                {"goal_id": goal_id}
            )
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None

        except Exception as e:
            print(f"❌ get_goal_by_id error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_total_weight(self, user_id: int, cycle_id: int) -> float:
        """Gets sum of all goal weights for user in a cycle"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT NVL(SUM(weight), 0)
                FROM GOALS
                WHERE user_id  = :user_id
                  AND cycle_id = :cycle_id
                """,
                {"user_id": user_id, "cycle_id": cycle_id}
            )
            result = cursor.fetchone()[0]
            return safe_float(result) or 0.0

        except Exception as e:
            print(f"❌ get_total_weight error: {e}")
            raise e
        finally:
            release_connection(conn)

    def create_goal(
        self,
        user_id: int,
        cycle_id: int,
        title: str,
        description: Optional[str],
        weight: float,
        target: Optional[str]
    ) -> int:
        """Creates a new goal and returns goal_id"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            # Get next ID from sequence
            cursor.execute("SELECT seq_goals.NEXTVAL FROM DUAL")
            new_goal_id = int(cursor.fetchone()[0])

            cursor.execute(
                """
                INSERT INTO GOALS
                    (goal_id, user_id, cycle_id, title,
                     description, weight, target)
                VALUES
                    (:goal_id, :user_id, :cycle_id, :title,
                     :description, :weight, :target)
                """,
                {
                    "goal_id":     new_goal_id,
                    "user_id":     user_id,
                    "cycle_id":    cycle_id,
                    "title":       title,
                    "description": description,
                    "weight":      weight,
                    "target":      target
                }
            )
            conn.commit()
            return new_goal_id

        except Exception as e:
            conn.rollback()
            print(f"❌ create_goal error: {e}")
            raise e
        finally:
            release_connection(conn)

    def update_goal(
        self,
        goal_id: int,
        user_id: int,
        updates: dict
    ) -> bool:
        """Updates goal fields dynamically"""
        if not updates:
            return False

        conn = get_connection()
        try:
            set_parts = [f"{key} = :{key}" for key in updates.keys()]
            set_clause = ", ".join(set_parts)
            updates["goal_id"] = goal_id
            updates["user_id"] = user_id

            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE GOALS
                SET {set_clause}
                WHERE goal_id = :goal_id
                  AND user_id = :user_id
                """,
                updates
            )
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            print(f"❌ update_goal error: {e}")
            raise e
        finally:
            release_connection(conn)

    def update_achievement(
        self,
        goal_id: int,
        user_id: int,
        achievement: str
    ) -> bool:
        """Records actual achievement for a goal"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE GOALS
                SET achievement = :achievement
                WHERE goal_id = :goal_id
                  AND user_id = :user_id
                """,
                {
                    "achievement": achievement,
                    "goal_id":     goal_id,
                    "user_id":     user_id
                }
            )
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            print(f"❌ update_achievement error: {e}")
            raise e
        finally:
            release_connection(conn)

    def _row_to_dict(self, row) -> dict:
        """
        Converts DB row to dict.
        IMPORTANT: description is CLOB — must use read_lob()
        """
        return {
            "goal_id":     safe_int(row[0]),
            "user_id":     safe_int(row[1]),
            "cycle_id":    safe_int(row[2]),
            "title":       safe_str(row[3]),
            "description": read_lob(row[4]),   # ← CLOB field
            "weight":      safe_float(row[5]),
            "target":      safe_str(row[6]),
            "achievement": safe_str(row[7]),
            "created_at":  safe_date(row[8])
        }