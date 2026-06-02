# chatbot_routes.py
# Now uses updated controller with response_utils

from flask import Blueprint, request
from controllers.chatbot_controller import ChatbotController
from utils.response_utils import error_response

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")
controller = ChatbotController()


@chatbot_bp.route("/ask", methods=["POST"])
def ask():
    """
    POST /chatbot/ask

    Employee or Manager asks for AI assistance.

    Request Body:
    {
        "question": "Help me write a self-assessment for my React project",
        "user_id": 3
    }

    Response:
    {
        "success": true,
        "message": "Answer generated successfully",
        "data": {
            "question": "...",
            "answer": "...",
            "sources_used": 2
        }
    }
    """
    # Make sure request has JSON body
    if not request.is_json:
        return error_response(
            message="Content-Type must be application/json",
            status_code=415
        )

    data = request.get_json()

    if not data:
        return error_response(
            message="Request body cannot be empty",
            status_code=400
        )

    question = data.get("question", "").strip()
    user_id = data.get("user_id", None)

    return controller.ask(question=question, user_id=user_id)


@chatbot_bp.route("/health", methods=["GET"])
def health():
    """
    GET /chatbot/health
    Used by Docker and Kubernetes to check if service is alive.
    """
    from utils.response_utils import success_response
    return success_response(
        data={"service": "Flask AI Service", "status": "healthy"},
        message="Service is running"
    )