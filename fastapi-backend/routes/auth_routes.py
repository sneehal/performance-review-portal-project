# auth_routes.py
# Only defines URL endpoints and maps them to controllers
# No business logic here!

from fastapi import APIRouter, Depends, Header
from typing import Optional
from dto.auth_dto import RegisterRequestDTO, LoginRequestDTO
from controllers.auth_controller import AuthController
from utils.response_utils import success_response

# Create a router — think of it as a mini-app for /auth endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_controller = AuthController()


@router.post("/register", summary="Register a new user")
def register(body: RegisterRequestDTO):
    """
    Registers a new user (employee, manager, or hr_admin).
    
    - **name**: Full name of the user
    - **email**: Unique work email
    - **password**: Minimum 6 characters
    - **role**: employee, manager, or hr_admin
    """
    result = auth_controller.register(
        name=body.name,
        email=body.email,
        password=body.password,
        role=body.role,
        department=body.department,
        manager_id=body.manager_id
    )
    return success_response(data=result, message="User registered successfully")


@router.post("/login", summary="Login and get JWT token")
def login(body: LoginRequestDTO):
    """
    Authenticates a user and returns a JWT token.
    Use this token in the Authorization header for all protected routes.
    """
    result = auth_controller.login(email=body.email, password=body.password)
    return success_response(data=result, message="Login successful")


@router.get("/me", summary="Get current logged-in user profile")
def get_me(authorization: Optional[str] = Header(None)):
    """
    Returns the profile of the currently logged-in user.
    Requires: Authorization: Bearer <token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Bearer token required")

    token = authorization.split(" ")[1]
    result = auth_controller.get_me(token=token)
    return success_response(data=result)