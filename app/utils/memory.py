sessions = {}

def create_session(user_id: str, level: str = "A1") -> dict:
    #Crear nueva sesión de usuario
    sessions[user_id] = {
        "level": level,
        "messages": [],
        "stats": {"messages_count": 0, "corrections": 0}
    }
    return sessions[user_id]

def get_session(user_id: str) -> dict:
    #Obtener sesión de usuario
    if user_id not in sessions:
        return create_session(user_id)
    return sessions[user_id]

def add_message(user_id: str, role: str, text: str):
    #Añadir mensaje al historial
    session = get_session(user_id)
    session["messages"].append({"role": role, "text": text})
    if role == "student":
        session["stats"]["messages_count"] += 1

def get_history(user_id: str, limit: int = 10) -> list:
    #Obtener historial de conversación
    session = get_session(user_id)
    return session["messages"][-limit:]

def update_level(user_id: str, new_level: str):
    #Actualizar nivel del usuario
    session = get_session(user_id)
    session["level"] = new_level
