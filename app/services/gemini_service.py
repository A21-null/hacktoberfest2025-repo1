import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """Eres un tutor de gallego amable, paciente y profesional.

Instrucciones:
- Responde siempre en gallego cuando sea posible
- Adapta tu nivel al del estudiante indicado
- Corrige errores de forma constructiva y didáctica
- Proporciona ejemplos prácticos
- Si el estudiante usa otro idioma, responde en gallego pero aclara
- Usa vocabulario y gramática apropiados al nivel indicado
- Sé motivador y positivo
- Si hay errores ya corregidos, valida las correcciones y explica por qué"""

CORRECTION_PROMPT = """Analiza este mensaje en gallego y detecta errores gramaticales, ortográficos o de vocabulario.

Responde en JSON con esta estructura:
{{
    "has_errors": true/false,
    "corrections": [
        {{
            "error": "texto incorrecto",
            "correction": "texto correcto",
            "type": "grammar/spelling/vocabulary/punctuation",
            "explanation": "explicación breve del error"
        }}
    ],
    "corrected_message": "mensaje completamente corregido",
    "overall_explanation": "resumen general de los errores encontrados o 'Perfecto!' si no hay errores"
}}

IMPORTANTE: Sé riguroso pero constructivo. Nivel del estudiante: {level}"""


def get_tutor_response(user_message: str, level: str = "A1", history: list = None, 
                       has_errors: bool = False, corrections: list = None) -> str:
    """
    Obtiene respuesta del tutor desde Gemini.
    
    Args:
        user_message: Mensaje del usuario
        level: Nivel MCER (A1, A2, B1, B2, C1, C2)
        history: Historial de conversación anterior
        has_errors: Si el mensaje tiene errores detectados
        corrections: Lista de correcciones realizadas
    
    Returns:
        Respuesta del tutor en gallego
    """
    
    try:
        model = genai.GenerativeModel("models/gemini-pro-latest")
        
        # Construir prompt con contexto
        full_prompt = f"{SYSTEM_PROMPT}\n\nNivel del estudiante: {level}\n\n"
        
        # Si hay errores, incluirlos en el contexto
        if has_errors and corrections:
            full_prompt += "NOTA: El estudiante escribió con algunos errores que ya fueron corregidos:\n"
            for corr in corrections:
                full_prompt += f"- Error: '{corr['error']}' → Corrección: '{corr['correction']}' ({corr['type']})\n"
            full_prompt += "\nTen esto en cuenta en tu respuesta educativa.\n\n"
        
        # Incluir historial si existe
        if history:
            full_prompt += "Historial de conversación (últimos mensajes):\n"
            for msg in history[-5:]:  # Últimos 5 mensajes
                full_prompt += f"{msg['role'].capitalize()}: {msg['text']}\n"
            full_prompt += "\n"
        
        full_prompt += f"Estudiante: {user_message}\nTutor:"
        
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        return f"Error al conectar con Gemini: {str(e)}"


def correct_message(message: str, level: str = "A1") -> dict:
    """
    Analiza un mensaje en gallego y detecta errores.
    
    Args:
        message: Mensaje a analizar
        level: Nivel MCER del estudiante
    
    Returns:
        Diccionario con:
        - has_errors: bool
        - corrections: list de correcciones
        - corrected_message: string
        - explanation: string
    """
    
    try:
        model = genai.GenerativeModel("models/gemini-pro-latest")
        
        prompt = CORRECTION_PROMPT.format(level=level) + f"\n\nMensaje: {message}"
        
        response = model.generate_content(prompt)
        
        # Parsear respuesta JSON
        response_text = response.text
        
        # Limpiar markdown si viene en ```json
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        result = json.loads(response_text.strip())
        
        return {
            "has_errors": result.get("has_errors", False),
            "corrections": result.get("corrections", []),
            "corrected_message": result.get("corrected_message", message),
            "explanation": result.get("overall_explanation", "Sin errores detectados")
        }
    
    except json.JSONDecodeError:
        # Si falla el parseo JSON, devolver respuesta segura
        return {
            "has_errors": False,
            "corrections": [],
            "corrected_message": message,
            "explanation": "No se pudo analizar el mensaje"
        }
    except Exception as e:
        return {
            "has_errors": False,
            "corrections": [],
            "corrected_message": message,
            "explanation": f"Error al analizar: {str(e)}"
        }