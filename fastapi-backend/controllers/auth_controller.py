# auth_controller.py
# Handles HTTP request parsing and calls service methods
# Returns proper HTTP responses

from fastapi import HTTPException, status
from services.auth_service import AuthService
from utils.jwt_utils import decode_access_token
from utils.exceptions import ConflictException, UnauthorizedException, NotFoundException

auth_service = AuthService()


class AuthController:

    def register(self, name: str, email: str, password: str,
                 role: str, department: str, manager_id: int) -> dict:
        """Handles POST /auth/register"""
        try:
            return auth_service.register_user(name, email, password, role, department, manager_id)
        except ConflictException as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.message))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed. Please try again."
            )

    def login(self, email: str, password: str) -> dict:
        """Handles POST /auth/login"""
        try:
            return auth_service.login_user(email, password)
        except UnauthorizedException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e.message)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed. Please try again."
            )

    def get_me(self, token: str) -> dict:
        """Handles GET /auth/me — returns current user profile"""
        try:
            payload = decode_access_token(token)
            user_id = payload.get("user_id")
            return auth_service.get_current_user_profile(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        except NotFoundException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e.message)
            )

    def get_token_data(self, token: str) -> dict:
        """
        Decodes JWT and returns user info.
        Used by other controllers to verify authentication.
        """
        try:
            return decode_access_token(token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token. Please login again."
            )