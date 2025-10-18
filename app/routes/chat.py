from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models.schemas import ChatRequest, ChatResponse, SessionInfo, ErrorResponse, Correction
from app.services.gemini_service import get_tutor_response, correct_message
from app.utils.memory import (
    get_session, add_message, get_history, 
    create_session, update_level
)

router = APIRouter()

LEVELS_MAP = {
    0: "A1",  
    1: "A2", 
    2: "B1",  
    3: "B2", 
    4: "C1",  
    5: "C2"   
}

LEVELS_DESCRIPTION = {
    0: "Principiante (A1)",
    1: "Elemental (A2)",
    2: "Intermedio (B1)",
    3: "Intermedio-Alto (B2)",
    4: "Avanzado (C1)",
    5: "Dominio Pleno (C2)"
}


@router.post(
    "/message",
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Solicitud incorrecta"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
def chat_message(request: ChatRequest):
    """
    Endpoint principal para enviar mensaje al tutor.
    
    - Detecta y corrige automáticamente errores en el mensaje
    - Usa índice de nivel (0-5) en lugar de string
    - Proporciona retroalimentación inmediata
    
    Args:
        request.user_id: ID único del usuario
        request.message: Mensaje del estudiante en gallego
        request.level_index: Índice del nivel (0=A1, 1=A2, ..., 5=C2)
        request.mode: Tipo de práctica (conversation, grammar, vocabulary)
    
    Returns:
        ChatResponse con mensaje corregido y respuesta del tutor
    """
    
    try:
        # Validar que el índice de nivel es válido
        if not isinstance(request.level_index, int) or request.level_index < 0 or request.level_index > 5:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(ErrorResponse(
                    detail="level_index debe ser un número entre 0 y 5",
                    code=400
                ))
            )
        
        # Convertir índice a nivel MCER
        level_code = LEVELS_MAP[request.level_index]
        level_description = LEVELS_DESCRIPTION[request.level_index]
        
        # Obtener o crear sesión
        session = get_session(request.user_id)
        
        # Actualizar nivel si viene en request
        if request.level_index is not None:
            update_level(request.user_id, level_code)
        
        # Obtener historial para contexto
        history = get_history(request.user_id)
        
        # ============ CORRECCIÓN AUTOMÁTICA ============
        # Detectar y corregir errores en el mensaje del estudiante
        correction_result = correct_message(
            message=request.message,
            level=level_code
        )
        
        has_errors = correction_result["has_errors"]
        corrections = [Correction(**c) for c in correction_result["corrections"]] if correction_result["corrections"] else []
        # Si no hay errores, el mensaje corregido debe ser vacío
        corrected_message = "" if not has_errors else correction_result["corrected_message"]
        error_explanation = correction_result["explanation"]
        
        # ============ RESPUESTA DEL TUTOR ============
        # El tutor responde al mensaje (corregido o no)
        tutor_response = get_tutor_response(
            user_message=request.message,
            level=level_code,
            history=history,
            has_errors=has_errors,
            corrections=[c.dict() for c in corrections]
        )
        
        # Guardar en historial
        add_message(request.user_id, "student", request.message)
        add_message(request.user_id, "tutor", tutor_response)
        
        # Si hay errores, incrementar contador de correcciones
        if has_errors:
            session["stats"]["corrections"] += 1
        
        return ChatResponse(
            user_id=request.user_id,
            student_message=request.message,
            tutor_response=tutor_response,
            level=level_code,
            level_index=request.level_index,
            level_description=level_description,
            mode=request.mode or "conversation",
            has_errors=has_errors,
            corrections=corrections,
            corrected_message=corrected_message,
            error_explanation=error_explanation
        )
    
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(ErrorResponse(
                detail=f"Error en los datos: {str(e)}",
                code=400
            ))
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(ErrorResponse(
                detail=f"Error del servidor: {str(e)}",
                code=500
            ))
        )


@router.get("/session/{user_id}", response_model=SessionInfo)
def get_user_session(user_id: str):
    """
    Obtener información de la sesión del usuario.
    
    Devuelve:
    - level_index: Índice del nivel actual
    - level_code: Código MCER (A1, A2, etc.)
    - level_description: Descripción del nivel
    - messages_count: Número de mensajes enviados
    - corrections: Número de correcciones realizadas
    """
    
    try:
        session = get_session(user_id)
        level_code = session["level"]
        
        # Encontrar el índice del nivel actual
        level_index = [k for k, v in LEVELS_MAP.items() if v == level_code][0]
        
        return SessionInfo(
            user_id=user_id,
            level_code=level_code,
            level_index=level_index,
            level_description=LEVELS_DESCRIPTION[level_index],
            messages_count=session["stats"]["messages_count"],
            corrections=session["stats"]["corrections"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{user_id}/set-level/{level_index}")
def set_user_level(user_id: str, level_index: int):
    """
    Establecer el nivel de un usuario por índice.
    
    Args:
        user_id: ID del usuario
        level_index: Índice del nivel (0-5)
    
    Returns:
        Confirmación del cambio de nivel
    """
    
    try:
        if level_index < 0 or level_index > 5:
            raise HTTPException(
                status_code=400,
                detail="level_index debe estar entre 0 y 5"
            )
        
        level_code = LEVELS_MAP[level_index]
        session = get_session(user_id)
        update_level(user_id, level_code)
        
        return {
            "message": f"Nivel actualizado",
            "user_id": user_id,
            "level_index": level_index,
            "level_code": level_code,
            "level_description": LEVELS_DESCRIPTION[level_index]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{user_id}/reset")
def reset_session(user_id: str, level_index: int = 0):
    """
    Reiniciar sesión del usuario con un nivel inicial.
    
    Args:
        user_id: ID del usuario
        level_index: Índice del nivel inicial (default: 0 = A1)
    """
    
    try:
        if level_index < 0 or level_index > 5:
            level_index = 0
        
        level_code = LEVELS_MAP[level_index]
        create_session(user_id, level_code)
        
        return {
            "message": "Sesión reiniciada",
            "user_id": user_id,
            "level_index": level_index,
            "level_code": level_code,
            "level_description": LEVELS_DESCRIPTION[level_index]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}")
def get_user_history(user_id: str, limit: int = 20):
    """
    Obtener historial de conversación del usuario.
    
    Args:
        user_id: ID del usuario
        limit: Número máximo de mensajes a retornar
    
    Returns:
        Lista de mensajes con timestamps
    """
    
    try:
        history = get_history(user_id, limit)
        return {
            "user_id": user_id,
            "total_messages": len(history),
            "messages": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/levels")
def get_available_levels():
    """
    Obtener lista de todos los niveles disponibles.
    
    Returns:
        Diccionario con índices, códigos y descripciones de niveles
    """
    
    return {
        "levels": [
            {
                "index": idx,
                "code": LEVELS_MAP[idx],
                "description": LEVELS_DESCRIPTION[idx]
            }
            for idx in range(6)
        ]
    }