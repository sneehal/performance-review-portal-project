# password_utils.py
# Password hashing using passlib with bcrypt
# bcrypt is the industry standard for password hashing

from passlib.context import CryptContext

# Create bcrypt context
# deprecated="auto" means old hash formats get upgraded automatically
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(plain_password: str) -> str:
    """
    Converts a plain text password into a secure bcrypt hash.

    Why bcrypt?
    - Automatically adds a random salt (prevents rainbow table attacks)
    - Slow by design (makes brute force attacks very slow)
    - The hash includes the salt, so you don't store salt separately

    Args:
        plain_password: Raw password from registration form
                        Example: "MyPassword@123"

    Returns:
        Bcrypt hash string
        Example: "$2b$12$EixZaYVK1fsbw1ZfbX3OXe..."

    Usage:
        hashed = hash_password("MyPassword@123")
        # Store hashed in database, NEVER store plain_password
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain password matches the stored bcrypt hash.

    How it works:
    - Extracts the salt from the stored hash
    - Hashes the plain_password using that same salt
    - Compares the result with the stored hash

    Args:
        plain_password: Password typed by user during login
        hashed_password: Hash stored in USERS table

    Returns:
        True if password matches, False otherwise

    Usage:
        is_valid = verify_password("MyPassword@123", stored_hash)
        if not is_valid:
            raise UnauthorizedException("Wrong password")
    """
    return pwd_context.verify(plain_password, hashed_password)