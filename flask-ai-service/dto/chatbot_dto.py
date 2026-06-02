# chatbot_dto.py
# Simple dataclass for request/response validation in Flask

from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatRequestDTO:
    question: str
    user_id: Optional[int] = None
    context_type: Optional[str] = None  # "self_assessment" or "manager_feedback"