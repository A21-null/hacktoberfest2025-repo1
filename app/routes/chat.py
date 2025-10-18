from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, SessionInfo, ErrorResponse, CorrectionRequest, CorrectionResponse
from app.services.gemini_service import get_tutor_response
from app.utils.memory import (
    get_session, add_message, get_history, 
    create_session, update_level
)

router = APIRouter()

@router.post("/message", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def chat_message(request: ChatRequest):
    """Endpoint principal para enviar mensaje al tutor"""
    if not request.message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    try:
        # Obtener o crear sesión
        session = get_session(request.user_id)
        
        # Actualizar nivel si viene en request
        if request.level and request.level != session["level"]:
            update_level(request.user_id, request.level)
        
        # Obtener historial para contexto
        history = get_history(request.user_id)
        
        # Obtener respuesta del tutor
        tutor_response = get_tutor_response(
            user_message=request.message,
            level=request.level or session["level"],
            history=history
        )
        
        # Guardar en historial
        add_message(request.user_id, "student", request.message)
        add_message(request.user_id, "tutor", tutor_response)
        
        return ChatResponse(
            user_id=request.user_id,
            student_message=request.message,
            tutor_response=tutor_response,
            level=request.level or session["level"],
            mode=request.mode or "conversation"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{user_id}", response_model=SessionInfo, responses={404: {"model": ErrorResponse}})
def get_user_session(user_id: str):
    """Obtener información de la sesión del usuario"""
    
    session = get_session(user_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return SessionInfo(
        user_id=user_id,
        level=session["level"],
        messages_count=session["stats"]["messages_count"],
        corrections=session["stats"]["corrections"]
    )

@router.post("/session/{user_id}/reset", response_model=ErrorResponse)
def reset_session(user_id: str, level: str = "A1"):
    """Reiniciar sesión del usuario"""
    
    create_session(user_id, level)
    return ErrorResponse(detail=f"Sesión reiniciada para {user_id} en nivel {level}")

@router.get("/history/{user_id}", responses={404: {"model": ErrorResponse}})
def get_user_history(user_id: str, limit: int = 20):
    """Obtener historial de conversación del usuario"""
    
    history = get_history(user_id, limit)
    if not history:
        raise HTTPException(status_code=404, detail="No hay historial para este usuario")
    return {"user_id": user_id, "messages": history}

@router.post("/correction", response_model=CorrectionResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
def correction(request: CorrectionRequest):
    """Endpoint para corrección de mensajes"""
    if not request.message:
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    try:
        # Aquí iría la lógica real de corrección
        corrected_message = request.message  # Simulación
        corrections = [{"error": c, "suggestion": "..."} for c in request.corrections]
        
        return CorrectionResponse(
            user_id=request.user_id,
            original_message=request.message,
            corrected_message=corrected_message,
            corrections=corrections
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
