# auth_dto.py
# Pydantic models define the shape of request body and responses
# FastAPI uses these for automatic validation

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequestDTO(BaseModel):
    """Request body for POST /auth/register"""
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Work email address")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")
    role: str = Field(default="employee", description="employee, manager, or hr_admin")
    department: Optional[str] = Field(None, max_length=100)
    manager_id: Optional[int] = Field(None, description="Manager's user_id")

    class Config:
        # Example shown in Swagger UI docs
        json_schema_extra = {
            "example": {
                "name": "Alice Smith",
                "email": "alice@company.com",
                "password": "SecurePass@123",
                "role": "employee",
                "department": "Engineering",
                "manager_id": 2
            }
        }


class LoginRequestDTO(BaseModel):
    """Request body for POST /auth/login"""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "alice@company.com",
                "password": "SecurePass@123"
            }
        }


class LoginResponseDTO(BaseModel):
    """Response body for successful login"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    role: str
    department: Optional[str]


class UserProfileDTO(BaseModel):
    """Response for GET /auth/me"""
    user_id: int
    name: str
    email: str
    role: str
    department: Optional[str]
    manager_id: Optional[int]