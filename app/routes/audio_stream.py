from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import whisper
import tempfile
import os
import torch

router = APIRouter()

# Global variable to store model
model = None


def get_model():
    global model
    if model is None:
        # Force CPU usage to avoid CUDA compatibility issues with GTX 1050
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        torch.cuda.is_available = lambda: False
        device = "cpu"
        print("Using CPU for Whisper model (CUDA disabled)")
        
        model = whisper.load_model("base", device=device)
    return model


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
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        try:
            # Get model and transcribe
            whisper_model = get_model()
            result = whisper_model.transcribe(temp_audio_path, language="gl")
            await websocket.send_text(str(result["text"]))
        except Exception as e:
            await websocket.send_text(f"Error al transcribir: {str(e)}")
        finally:
            os.remove(temp_audio_path)
