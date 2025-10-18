from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.chat import router as chat_router

app = FastAPI(
    title="Galician Tutor Backend",
    description="AI-powered Galician language tutor with 5 proficiency levels",
    version="1.0.0"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def root():
    return {
        "message": "Galician Tutor Backend - Integrated with Reflex Frontend",
        "version": "1.0.0",
        "levels": ["A1", "A2", "B1", "B2", "C1"],
        "endpoints": [
            "/api/chat/message",
            "/api/chat/session/{user_id}", 
            "/api/chat/levels",
            "/api/chat/health"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "backend": "galician-tutor"}


if __name__ == "__main__":
    import uvicorn
    # Use import string instead of app object for reload to work properly
    uvicorn.run(
        "main:app",  # ← Changed from 'app' to "main:app" 
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )