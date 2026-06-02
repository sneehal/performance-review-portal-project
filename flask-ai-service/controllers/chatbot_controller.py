# chatbot_controller.py
# Now uses standardized response_utils

from services.chatbot_service import ChatbotService
from utils.response_utils import success_response, error_response, server_error_response
from utils.exceptions import ValidationException, LLMException, DatabaseException

chatbot_service = ChatbotService()


class ChatbotController:

    def ask(self, question: str, user_id: int = None):
        """
        Handles POST /chatbot/ask

        Validates the question, calls the chatbot service
        which runs the full RAG flow, and returns the AI response.

        Success Response:
        {
            "success": true,
            "message": "Answer generated",
            "data": {
                "question": "Help me write feedback...",
                "answer": "Here is a professional self-assessment...",
                "sources_used": 2
            }
        }
        """
        # Validate input
        if not question:
            return error_response(
                message="Question is required",
                status_code=400
            )

        if len(question.strip()) < 5:
            return error_response(
                message="Question is too short. Please ask a complete question.",
                status_code=400
            )

        if len(question) > 1000:
            return error_response(
                message="Question is too long. Maximum 1000 characters allowed.",
                status_code=400
            )

        try:
            result = chatbot_service.answer_question(
                question=question.strip(),
                user_id=user_id
            )
            return success_response(
                data=result,
                message="Answer generated successfully"
            )

        except ValidationException as e:
            return error_response(
                message=e.message,
                status_code=400
            )

        except DatabaseException as e:
            return error_response(
                message="Could not fetch policy data. Please try again.",
                status_code=503
            )

        except LLMException as e:
            return error_response(
                message="AI service is temporarily unavailable. Please try again.",
                status_code=503
            )

        except Exception as e:
            return server_error_response(detail=str(e))