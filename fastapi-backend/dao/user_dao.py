# user_dao.py
# Database operations for USERS table
# Fixed for oracledb compatibility

import oracledb
from db import get_connection, release_connection
from models.user_model import UserModel
from typing import Optional, List


class UserDAO:

    def find_by_email(self, email: str) -> Optional[UserModel]:
        """
        Finds user by email for login.
        Returns None if not found.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()

            # Use named parameters with oracledb
            cursor.execute(
                """
                SELECT user_id, name, email, password_hash, role,
                       department, manager_id, is_active, created_at
                FROM USERS
                WHERE LOWER(email) = LOWER(:email)
                  AND is_active = 1
                """,
                {"email": email}
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return UserModel(
                user_id=int(row[0]),
                name=str(row[1]),
                email=str(row[2]),
                password_hash=str(row[3]),
                role=str(row[4]),
                department=str(row[5]) if row[5] else None,
                manager_id=int(row[6]) if row[6] else None,
                is_active=int(row[7]),
                created_at=row[8]
            )

        except Exception as e:
            print(f"❌ find_by_email error: {e}")
            raise e
        finally:
            release_connection(conn)

    def find_by_id(self, user_id: int) -> Optional[UserModel]:
        """Finds user by primary key"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT user_id, name, email, password_hash, role,
                       department, manager_id, is_active, created_at
                FROM USERS
                WHERE user_id = :user_id
                """,
                {"user_id": user_id}
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return UserModel(
                user_id=int(row[0]),
                name=str(row[1]),
                email=str(row[2]),
                password_hash=str(row[3]),
                role=str(row[4]),
                department=str(row[5]) if row[5] else None,
                manager_id=int(row[6]) if row[6] else None,
                is_active=int(row[7]),
                created_at=row[8]
            )

        except Exception as e:
            print(f"❌ find_by_id error: {e}")
            raise e
        finally:
            release_connection(conn)

    def email_exists(self, email: str) -> bool:
        """Checks if email is already registered"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM USERS WHERE LOWER(email) = LOWER(:email)",
                {"email": email}
            )
            count = cursor.fetchone()[0]
            return int(count) > 0

        except Exception as e:
            print(f"❌ email_exists error: {e}")
            raise e
        finally:
            release_connection(conn)

    def create_user(
        self,
        name: str,
        email: str,
        password_hash: str,
        role: str,
        department: Optional[str],
        manager_id: Optional[int]
    ) -> int:
        """
        Creates new user in USERS table.
        Returns the auto-generated user_id.

        Uses sequence to get next ID because oracledb
        RETURNING clause can be tricky.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()

            # Get next ID from sequence first
            cursor.execute("SELECT seq_users.NEXTVAL FROM DUAL")
            new_user_id = int(cursor.fetchone()[0])

            # Insert with the generated ID
            cursor.execute(
                """
                INSERT INTO USERS
                    (user_id, name, email, password_hash,
                     role, department, manager_id)
                VALUES
                    (:user_id, :name, :email, :password_hash,
                     :role, :department, :manager_id)
                """,
                {
                    "user_id": new_user_id,
                    "name": name,
                    "email": email,
                    "password_hash": password_hash,
                    "role": role,
                    "department": department,
                    "manager_id": manager_id
                }
            )
            conn.commit()
            print(f"✅ User created with ID: {new_user_id}")
            return new_user_id

        except Exception as e:
            conn.rollback()
            print(f"❌ create_user error: {e}")
            raise e
        finally:
            release_connection(conn)

    def get_team_members(self, manager_id: int) -> List[dict]:
        """Returns all employees reporting to a manager"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT user_id, name, email, role, department
                FROM USERS
                WHERE manager_id = :manager_id
                  AND is_active = 1
                ORDER BY name
                """,
                {"manager_id": manager_id}
            )
            rows = cursor.fetchall()
            return [
                {
                    "user_id": int(row[0]),
                    "name": str(row[1]),
                    "email": str(row[2]),
                    "role": str(row[3]),
                    "department": str(row[4]) if row[4] else None
                }
                for row in rows
            ]

        except Exception as e:
            print(f"❌ get_team_members error: {e}")
            raise e
        finally:
            release_connection(conn)