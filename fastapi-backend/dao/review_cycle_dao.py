# review_cycle_dao.py
# Fixed to use dict-style parameters for oracledb

import oracledb
from db import get_connection, release_connection
from typing import Optional, List


class ReviewCycleDAO:

    def get_all_cycles(self) -> List[dict]:
        """Returns all review cycles ordered by newest first"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT cycle_id, name, start_date, end_date,
                       self_due_date, manager_due_date, status, created_by
                FROM REVIEW_CYCLES
                ORDER BY cycle_id DESC
                """
            )
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            print(f"❌ get_all_cycles error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_by_id(self, cycle_id: int) -> Optional[dict]:
        """Returns a single review cycle by ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT cycle_id, name, start_date, end_date,
                       self_due_date, manager_due_date, status, created_by
                FROM REVIEW_CYCLES
                WHERE cycle_id = :cycle_id
                """,
                {"cycle_id": cycle_id}
            )
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
        except Exception as e:
            print(f"❌ get_by_id error: {e}")
            raise e
        finally:
            release_connection(conn)

    def create_cycle(
        self,
        name: str,
        start_date,
        end_date,
        self_due_date,
        manager_due_date,
        created_by: int
    ) -> int:
        """Creates a new review cycle, returns new cycle_id"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            # Get next ID from sequence
            cursor.execute("SELECT seq_cycles.NEXTVAL FROM DUAL")
            new_cycle_id = int(cursor.fetchone()[0])

            cursor.execute(
                """
                INSERT INTO REVIEW_CYCLES
                    (cycle_id, name, start_date, end_date,
                     self_due_date, manager_due_date, created_by)
                VALUES
                    (:cycle_id, :name, :start_date, :end_date,
                     :self_due_date, :manager_due_date, :created_by)
                """,
                {
                    "cycle_id": new_cycle_id,
                    "name": name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "self_due_date": self_due_date,
                    "manager_due_date": manager_due_date,
                    "created_by": created_by
                }
            )
            conn.commit()
            return new_cycle_id

        except Exception as e:
            conn.rollback()
            print(f"❌ create_cycle error: {e}")
            raise e
        finally:
            release_connection(conn)

    def update_cycle(self, cycle_id: int, updates: dict) -> bool:
        """Dynamically updates provided fields"""
        if not updates:
            return False

        conn = get_connection()
        try:
            set_parts = [f"{key} = :{key}" for key in updates.keys()]
            set_clause = ", ".join(set_parts)
            updates["cycle_id"] = cycle_id

            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE REVIEW_CYCLES
                SET {set_clause}
                WHERE cycle_id = :cycle_id
                """,
                updates
            )
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            print(f"❌ update_cycle error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_cycle_progress(self, cycle_id: int) -> dict:
        """Calculates submission completion percentage"""
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM USERS WHERE role = 'employee' AND is_active = 1"
            )
            total_employees = int(cursor.fetchone()[0])

            cursor.execute(
                """
                SELECT COUNT(*) FROM REVIEWS
                WHERE cycle_id = :cycle_id
                  AND type = 'SELF'
                  AND status IN ('Submitted', 'Completed')
                """,
                {"cycle_id": cycle_id}
            )
            submitted_count = int(cursor.fetchone()[0])

            completion_pct = (
                round(submitted_count / total_employees * 100, 2)
                if total_employees > 0 else 0.0
            )

            return {
                "cycle_id": cycle_id,
                "total_employees": total_employees,
                "submitted_count": submitted_count,
                "completion_percentage": completion_pct
            }

        except Exception as e:
            print(f"❌ get_cycle_progress error: {e}")
            raise e
        finally:
            release_connection(conn)

    def _row_to_dict(self, row) -> dict:
        return {
            "cycle_id":         int(row[0]),
            "name":             str(row[1]),
            "start_date":       str(row[2]) if row[2] else None,
            "end_date":         str(row[3]) if row[3] else None,
            "self_due_date":    str(row[4]) if row[4] else None,
            "manager_due_date": str(row[5]) if row[5] else None,
            "status":           str(row[6]),
            "created_by":       int(row[7])
        }