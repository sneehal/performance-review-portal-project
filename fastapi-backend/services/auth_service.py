# auth_service.py
# Authentication business logic

from dao.user_dao import UserDAO
from utils.password_utils import hash_password, verify_password
from utils.jwt_utils import create_access_token
from utils.exceptions import (
    ConflictException,
    UnauthorizedException,
    NotFoundException
)

# Create single DAO instance
user_dao = UserDAO()


class AuthService:

    def register_user(
        self,
        name: str,
        email: str,
        password: str,
        role: str,
        department: str,
        manager_id: int
    ) -> dict:
        """
        Registers a new user.

        Steps:
        1. Check email does not already exist
        2. Hash the plain password
        3. Save to database
        4. Return new user_id
        """
        # Step 1: Check duplicate email
        if user_dao.email_exists(email):
            raise ConflictException(
                f"Email '{email}' is already registered. Please login instead."
            )

        # Step 2: Hash password — NEVER store plain text
        hashed_password = hash_password(password)

        # Step 3: Create in database
        new_user_id = user_dao.create_user(
            name=name,
            email=email,
            password_hash=hashed_password,
            role=role,
            department=department,
            manager_id=manager_id
        )

        return {
            "user_id": new_user_id,
            "message": "Registration successful. You can now login."
        }

    def login_user(self, email: str, password: str) -> dict:
        """
        Authenticates user and returns JWT token.

        Steps:
        1. Find user by email
        2. Verify password against stored hash
        3. Create JWT token with user info
        4. Return token and user details
        """
        # Step 1: Find user
        print(f"🔍 Login attempt for email: {email}")
        user = user_dao.find_by_email(email)

        if user is None:
            print(f"❌ User not found for email: {email}")
            raise UnauthorizedException(
                "Invalid email or password"
            )

        print(f"✅ User found: {user.name} | Role: {user.role}")
        print(f"🔐 Stored hash preview: {user.password_hash[:20]}...")

        # Step 2: Verify password
        is_valid = verify_password(password, user.password_hash)
        print(f"🔑 Password verification result: {is_valid}")

        if not is_valid:
            raise UnauthorizedException(
                "Invalid email or password"
            )

        # Step 3: Create JWT token
        token_data = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role
        }
        token = create_access_token(token_data)
        print(f"✅ JWT token created for user_id: {user.user_id}")

        # Step 4: Return everything frontend needs
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "name": user.name,
            "role": user.role,
            "department": user.department
        }

    def get_current_user_profile(self, user_id: int) -> dict:
        """Returns logged-in user profile"""
        user = user_dao.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        return {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "manager_id": user.manager_id
        }