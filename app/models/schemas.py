from pydantic import BaseModel
from typing import Optional, List

class Correction(BaseModel):
    """Representa una corrección individual"""
    error: str
    correction: str
    type: str  # grammar, spelling, vocabulary, punctuation
    explanation: str


class ChatRequest(BaseModel):
    """Solicitud de mensaje al tutor"""
    user_id: str
    message: str
    level_index: int = 0  # 0=A1, 1=A2, 2=B1, 3=B2, 4=C1, 5=C2
    mode: Optional[str] = "conversation"  # conversation, grammar, vocabulary


class ChatResponse(BaseModel):
    """Respuesta del tutor con análisis de errores"""
    user_id: str
    student_message: str
    tutor_response: str
    level: str  # Código MCER (A1, A2, B1, etc.)
    level_index: int  # Índice del nivel (0-5)
    level_description: str  # Descripción legible del nivel
    mode: str
    has_errors: bool  # Si se detectaron errores
    corrections: List[Correction]  # Lista de correcciones
    corrected_message: str  # Mensaje completamente corregido
    error_explanation: str  # Explicación general de los errores


class SessionInfo(BaseModel):
    """Información de la sesión del usuario"""
    user_id: str
    level_code: str  # Código MCER
    level_index: int  # Índice del nivel (0-5)
    level_description: str  # Descripción del nivel
    messages_count: int  # Total de mensajes enviados
    corrections: int  # Total de correcciones realizadas

class ErrorResponse(BaseModel):
    detail: str