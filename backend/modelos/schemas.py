from pydantic import BaseModel
from typing import Optional, List
# Modelos de datos para la aplicación de tutoría de idiomas


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
    level_index: int = 1  # 1=A1, 2=A2, 3=B1, 4=B2, 5=C1
    mode: Optional[str] = "conversation"

class ChatResponse(BaseModel):
    """Respuesta del tutor con análisis de errores"""
    user_id: str
    student_message: str
    tutor_response: str
    level: str  # Código MCER (A1, A2, B1, etc.)
    level_index: int  # Índice del nivel (1-5)
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
    level_index: int  # Índice del nivel (1-5)
    level_description: str  # Descripción del nivel
    messages_count: int  # Total de mensajes enviados
    corrections: int  # Total de correcciones realizadas


class ErrorResponse(BaseModel):
    detail: str
    code: int