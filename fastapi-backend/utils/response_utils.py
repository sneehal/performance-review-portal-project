# response_utils.py
# Standardized API response format
# Every API response will look the same - consistent for frontend

def success_response(data=None, message: str = "Success", status_code: int = 200) -> dict:
    """
    Standard success response format.
    
    Example output:
    {
        "success": true,
        "message": "User registered successfully",
        "data": { "user_id": 1 }
    }
    """
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str, status_code: int = 400) -> dict:
    """
    Standard error response format.
    
    Example output:
    {
        "success": false,
        "message": "Email already exists",
        "data": null
    }
    """
    return {
        "success": False,
        "message": message,
        "data": None
    }