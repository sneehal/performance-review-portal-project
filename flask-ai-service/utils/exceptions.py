# exceptions.py
# Custom exception classes for Flask AI Service
# Same pattern as FastAPI backend for consistency

class NotFoundException(Exception):
    """
    Raised when a requested resource is not found.
    Example: FAQ category not found in database.
    """
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class ValidationException(Exception):
    """
    Raised when input data fails validation.
    Example: Question is empty or too short.
    """
    def __init__(self, message: str = "Validation failed"):
        self.message = message
        super().__init__(self.message)


class LLMException(Exception):
    """
    Raised when the LLM API call fails.
    Example: OpenAI API key is invalid or rate limited.
    """
    def __init__(self, message: str = "AI service error"):
        self.message = message
        super().__init__(self.message)


class DatabaseException(Exception):
    """
    Raised when a database operation fails in Flask service.
    Example: Oracle connection timeout.
    """
    def __init__(self, message: str = "Database error"):
        self.message = message
        super().__init__(self.message)