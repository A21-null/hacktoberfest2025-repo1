from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="AI Tutor Gallego")

# CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar rutas
from app.routes.chat import router as chat_router
from app.routes.audio import router as audio_router
from app.routes.audio_stream import router as audio_stream_router

app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(audio_router, prefix="/api/audio", tags=["audio"])
app.include_router(audio_stream_router)

@app.get("/")
def root():
    return {"message": "AI Tutor Gallego - Backend activo"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",  # localhost for local development
        port=8000,
        reload=True,       # Enable hot reloading for development
        log_level="info"
    )