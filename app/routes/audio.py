from fastapi import APIRouter, UploadFile, File, HTTPException
import whisper

router = APIRouter()

# Carga el modelo Whisper 
model = whisper.load_model("base")

@router.post("/transcribe-audio")
def transcribe_audio(file: UploadFile = File(...)):
    """
    Recibe un archivo de audio y devuelve la transcripción usando Whisper.
    """
    try:
        if not file.filename.lower().endswith((".wav", ".mp3", ".m4a", ".ogg", ".flac")):
            raise HTTPException(status_code=400, detail="Formato de audio no soportado")
        # Guarda el archivo temporalmente
        audio_bytes = file.file.read()
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)
        # Transcribe
        result = model.transcribe(temp_path)
        # Elimina el archivo temporal
        import os
        os.remove(temp_path)
        return {"transcription": result["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al transcribir: {str(e)}")
