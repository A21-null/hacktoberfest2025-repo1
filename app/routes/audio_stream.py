from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import whisper
import tempfile
import os

router = APIRouter()
model = whisper.load_model("base") 

@router.websocket("/ws/audio-stream")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    audio_bytes = b""
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_bytes += data
    except WebSocketDisconnect:
        # Cuando el cliente cierra la conexión, procesamos el audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        try:
            result = model.transcribe(temp_audio_path, language="gl")
            await websocket.send_text(result["text"])
        except Exception as e:
            await websocket.send_text(f"Error al transcribir: {str(e)}")
        finally:
            os.remove(temp_audio_path)
