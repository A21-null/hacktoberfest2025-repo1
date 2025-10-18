from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    user_id: str
    message: str
    level: Optional[str] = "A1"
    mode: Optional[str] = "conversation"  # conversation, grammar, vocabulary

class ChatResponse(BaseModel):
    user_id: str
    student_message: str
    tutor_response: str
    level: str
    mode: str

class SessionInfo(BaseModel):
    user_id: str
    level: str
    messages_count: int
    corrections: int

class ErrorResponse(BaseModel):
    detail: str

class CorrectionRequest(BaseModel):
    user_id: str
    message: str
    corrections: List[str]

class CorrectionResponse(BaseModel):
    user_id: str
    original_message: str
    corrected_message: str
    corrections: List[dict]