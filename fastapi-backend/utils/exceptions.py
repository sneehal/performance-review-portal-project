# exceptions.py
# Custom exception classes for clean error handling

class NotFoundException(Exception):
    """Raised when a requested resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedException(Exception):
    """Raised when user doesn't have permission"""
    def __init__(self, message: str = "Unauthorized access"):
        self.message = message
        super().__init__(self.message)


class ValidationException(Exception):
    """Raised when input data fails business validation"""
    def __init__(self, message: str = "Validation failed"):
        self.message = message
        super().__init__(self.message)


class ConflictException(Exception):
    """Raised when a duplicate resource is created"""
    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)