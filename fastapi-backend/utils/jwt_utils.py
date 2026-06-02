# jwt_utils.py
# JWT token creation and verification using PyJWT
# PyJWT is the most stable JWT library for Python 3.13+
# Replaces python-jose which had Python 2 compatibility issues

import jwt
from datetime import datetime, timedelta, timezone
from config import settings


def create_access_token(data: dict) -> str:
    """
    Creates a signed JWT token with user info embedded inside.

    What is JWT?
    JWT = JSON Web Token
    It has 3 parts separated by dots:
    header.payload.signature

    The payload contains user info like user_id, role, email.
    The signature is created using our SECRET_KEY.
    Only our server can create valid tokens.

    Args:
        data: Dictionary with user info
              Example: {"user_id": 1, "role": "employee", "email": "alice@company.com"}

    Returns:
        JWT token string
        Example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

    Usage:
        token = create_access_token({"user_id": 1, "role": "employee"})
    """
    # Copy data so we don't modify the original dict
    to_encode = data.copy()

    # Set expiry time
    # timezone.utc is used because datetime.utcnow() is deprecated in Python 3.12+
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode["exp"] = expire

    # Sign and encode the token
    # algorithm HS256 = HMAC with SHA-256 (industry standard)
    token = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict:
    """
    Decodes and verifies a JWT token from the Authorization header.

    Steps it does internally:
    1. Splits the token into header, payload, signature
    2. Verifies the signature using SECRET_KEY
    3. Checks if token has expired
    4. Returns the payload (user data)

    Args:
        token: JWT string from Authorization: Bearer <token>

    Returns:
        Dictionary with user data
        Example: {"user_id": 1, "role": "employee", "email": "alice@company.com"}

    Raises:
        ValueError: If token is invalid, expired, or tampered with
    """
    try:
        # decode() automatically verifies signature AND expiry
        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload

    except jwt.ExpiredSignatureError:
        # Token existed but has expired
        raise ValueError("Token has expired. Please login again.")

    except jwt.InvalidTokenError:
        # Token is malformed or signature doesn't match
        raise ValueError("Invalid token. Please login again.")