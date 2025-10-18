import json
import os
from datetime import datetime

SESSIONS_FILE = "sessions.json"

def load_sessions():
    """Cargar sesiones del archivo JSON"""
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_sessions(sessions):
    """Guardar sesiones en archivo JSON"""
    try:
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2, default=str, ensure_ascii=False)
    except IOError as e:
        print(f"Error guardando sesiones: {e}")

# Cargar sesiones al iniciar
sessions = load_sessions()

def create_session(user_id: str, level: str = "A1") -> dict:
    """Crear nueva sesión de usuario"""
    sessions[user_id] = {
        "level": level,
        "messages": [],
        "stats": {
            "messages_count": 0,
            "corrections": 0
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    save_sessions(sessions)
    return sessions[user_id]

def get_session(user_id: str) -> dict:
    """Obtener sesión de usuario"""
    if user_id not in sessions:
        return create_session(user_id)
    return sessions[user_id]

def add_message(user_id: str, role: str, text: str):
    """Añadir mensaje al historial"""
    session = get_session(user_id)
    session["messages"].append({
        "role": role,
        "text": text,
        "timestamp": datetime.now().isoformat()
    })
    if role == "student":
        session["stats"]["messages_count"] += 1
    
    session["updated_at"] = datetime.now().isoformat()
    save_sessions(sessions)

def get_history(user_id: str, limit: int = 10) -> list:
    """Obtener historial de conversación"""
    session = get_session(user_id)
    messages = session["messages"][-limit:]
    return [
        {
            "role": msg["role"],
            "text": msg["text"],
            "timestamp": msg.get("timestamp", "")
        }
        for msg in messages
    ]

def update_level(user_id: str, new_level: str):
    """Actualizar nivel del usuario"""
    session = get_session(user_id)
    session["level"] = new_level
    session["updated_at"] = datetime.now().isoformat()
    save_sessions(sessions)

def get_all_users():
    """Obtener lista de todos los usuarios"""
    return list(sessions.keys())

def delete_session(user_id: str):
    """Eliminar sesión de un usuario"""
    if user_id in sessions:
        del sessions[user_id]
        save_sessions(sessions)
        return True
    return False

def get_user_stats(user_id: str) -> dict:
    """Obtener estadísticas de un usuario"""
    session = get_session(user_id)
    return {
        "user_id": user_id,
        "level": session["level"],
        "messages_count": session["stats"]["messages_count"],
        "corrections": session["stats"]["corrections"],
        "created_at": session.get("created_at"),
        "updated_at": session.get("updated_at"),
        "total_messages_in_history": len(session["messages"])
    }