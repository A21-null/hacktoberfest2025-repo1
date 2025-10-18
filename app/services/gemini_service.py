import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Listando modelos disponibles...")
for m in genai.list_models():
    print(m.name)
print("Fin de listado.")

SYSTEM_PROMPT = """Eres un tutor de gallego amable, paciente y profesional.

Instrucciones:
- Responde siempre en gallego cuando sea posible
- Adapta tu nivel al del estudiante
- Corrige errores de forma constructiva y didáctica
- Proporciona ejemplos prácticos
- Si el estudiante usa otro idioma, responde en gallego pero aclara
- Usa vocabulario y gramática apropiados al nivel indicado
- Sé motivador y positivo"""

def get_tutor_response(user_message: str, level: str = "A1", history: list = None) -> str:
    """
    Obtiene respuesta del tutor desde Gemini
    
    Args:
        user_message: Mensaje del usuario
        level: Nivel de gallego (A1, A2, B1, B2, C1, C2)
        history: Historial de conversación anterior
    
    Returns:
        Respuesta del tutor en gallego
    """
    
    try:
        model = genai.GenerativeModel("models/gemini-pro-latest")
        
        # Construir prompt con contexto
        full_prompt = f"{SYSTEM_PROMPT}\n\nNivel del estudiante: {level}\n\n"
        
        if history:
            full_prompt += "Historial de conversación:\n"
            for msg in history[-5:]:  # Últimos 5 mensajes para contexto
                full_prompt += f"{msg['role']}: {msg['text']}\n"
        
        full_prompt += f"\nEstudiante: {user_message}\nTutor:"
        
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        return f"Error al conectar con Gemini: {str(e)}"