# response_utils.py
# Standardized response format for Flask AI Service
# Every API response looks the same — frontend knows what to expect

from flask import jsonify


def success_response(data=None, message: str = "Success", status_code: int = 200):
    """
    Creates a standard success response.

    Format:
    {
        "success": true,
        "message": "Answer generated",
        "data": {
            "answer": "...",
            "sources_used": 2
        }
    }

    Args:
        data: The actual response payload
        message: Human readable success message
        status_code: HTTP status code (default 200)

    Returns:
        Flask JSON response tuple (response, status_code)
    """
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code


def error_response(message: str, status_code: int = 400):
    """
    Creates a standard error response.

    Format:
    {
        "success": false,
        "message": "Question too short",
        "data": null
    }

    Args:
        message: Human readable error description
        status_code: HTTP error code (400, 401, 403, 404, 500)

    Returns:
        Flask JSON response tuple (response, status_code)
    """
    response = {
        "success": False,
        "message": message,
        "data": None
    }
    return jsonify(response), status_code


def not_found_response(resource: str = "Resource"):
    """
    Shortcut for 404 responses.

    Example: not_found_response("FAQ")
    Returns: {"success": false, "message": "FAQ not found", "data": null}
    """
    return error_response(
        message=f"{resource} not found",
        status_code=404
    )


def server_error_response(detail: str = ""):
    """
    Shortcut for 500 responses.
    Hides internal error details from client in production.
    """
    message = "Internal server error. Please try again."
    if detail:
        # Only show details in development
        message = f"Internal server error: {detail}"
    return error_response(
        message=message,
        status_code=500
    )