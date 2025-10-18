from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from backend.models.schemas import (
    ChatRequest, ChatResponse, SessionInfo, ErrorResponse, Correction
)
from backend.services.gemini_service import (
    get_tutor_response, correct_message, get_level_code, get_level_description,
    LEVEL_MAPPING, LEVEL_DESCRIPTIONS
)
from backend.services.memory import (
    get_session, add_message, get_history, 
    create_session, update_level
)

router = APIRouter()


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
    - Usa índice de nivel (1-5) en lugar de string
    - Proporciona retroalimentación inmediata
    
    Args:
        request.user_id: ID único del usuario
        request.message: Mensaje del estudiante en gallego
        request.level_index: Índice del nivel (1=A1, 2=A2, 3=B1, 4=B2, 5=C1)
        request.mode: Tipo de práctica (conversation, grammar, vocabulary)
    
    Returns:
        ChatResponse con mensaje corregido y respuesta del tutor
    """
    
    try:
        # Validar que el índice de nivel es válido
        if not isinstance(request.level_index, int) or request.level_index < 1 or request.level_index > 5:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder(ErrorResponse(
                    detail="level_index debe ser un número entre 1 y 5",
                    code=400
                ))
            )
        
        # Convertir índice a nivel MCER
        level_code = get_level_code(request.level_index)
        level_description = get_level_description(request.level_index)
        
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
    """
    
    try:
        session = get_session(user_id)
        level_code = session["level"]
        
        # Encontrar el índice del nivel actual
        level_index = [k for k, v in LEVEL_MAPPING.items() if v == level_code][0]
        
        return SessionInfo(
            user_id=user_id,
            level_code=level_code,
            level_index=level_index,
            level_description=LEVEL_DESCRIPTIONS[level_index],
            messages_count=session["stats"]["messages_count"],
            corrections=session["stats"]["corrections"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{user_id}/set-level/{level_index}")
def set_user_level(user_id: str, level_index: int):
    """
    Establecer el nivel de un usuario por índice.
    """
    
    try:
        if level_index < 1 or level_index > 5:
            raise HTTPException(
                status_code=400,
                detail="level_index debe estar entre 1 y 5"
            )
        
        level_code = get_level_code(level_index)
        session = get_session(user_id)
        update_level(user_id, level_code)
        
        return {
            "message": f"Nivel actualizado",
            "user_id": user_id,
            "level_index": level_index,
            "level_code": level_code,
            "level_description": get_level_description(level_index)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/levels")
def get_available_levels():
    """
    Obtener lista de todos los niveles disponibles.
    """
    
    return {
        "levels": [
            {
                "index": idx,
                "code": LEVEL_MAPPING[idx],
                "description": LEVEL_DESCRIPTIONS[idx]
            }
            for idx in range(1, 6)
        ]
    }


@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "galician-tutor-backend"}