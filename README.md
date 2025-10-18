# AI Tutor Gallego - Integrated Setup

This project consists of an integrated Galician language tutor with:
1. **Integrated Backend**: FastAPI application (`/backend`) with Gemini AI integration
2. **Frontend**: Reflex application (`/reflex-chat`) connected to the backend
3. **Original Backend**: Legacy FastAPI application (`/app`) for testing

## Prerequisites

- Python virtual environment at `~/venv_hacktober25/bin/activate`
- All necessary libraries should already be installed in this environment

## Quick Start

1. **Setup (first time only):**
   ```bash
   chmod +x setup.sh run_backend.sh run_frontend.sh
   ./setup.sh
   ```

2. **Run Integrated Backend:**
   ```bash
   ./run_backend.sh
   ```
   Backend will be available at: http://localhost:8000

3. **Run Frontend (in a separate terminal):**
   ```bash
   ./run_frontend.sh
   ```
   Frontend will be available at: http://localhost:3000

4. **Test Legacy Backend (optional):**
   ```bash
   ./run-old-backend.sh
   ```

## Manual Setup

### Integrated Backend Setup
```bash
source ~/venv_hacktober25/bin/activate
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
source ~/venv_hacktober25/bin/activate
cd reflex-chat
pip install -r requirements.txt
reflex run
```

### Legacy Backend Setup (for testing)
```bash
source ~/venv_hacktober25/bin/activate
cd app
pip install -r requirements.txt
python main.py
```

## Environment Variables

Create a `.env` file in the `/backend` directory with your configuration:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Galician Language Levels

The tutor supports 5 proficiency levels:
- **Nivel 1**: Iniciación (A1) - Basic vocabulary and simple phrases
- **Nivel 2**: Básico (A2) - Everyday expressions and common situations  
- **Nivel 3**: Intermedio (B1) - More complex conversations and grammar
- **Nivel 4**: Avanzado (B2) - Advanced grammar and fluent communication
- **Nivel 5**: Experto (C1) - Near-native proficiency and nuanced language

## API Endpoints

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Features

The integrated Galician Tutor provides:
- **AI-Powered Responses**: Google Gemini integration for intelligent tutoring
- **Error Correction**: Automatic detection and correction of Galician grammar/spelling
- **5 Proficiency Levels**: Adaptive learning from beginner to expert
- **Real-time Chat**: Responsive web interface with message streaming
- **User Progress Tracking**: Session management and learning statistics
- **Audio Support**: Voice recording and transcription (legacy backend)
- **Responsive Design**: Works on desktop and mobile devices

## Development

Both applications support hot reloading:
- Backend: Changes to Python files will trigger reload
- Frontend: Reflex automatically reloads on file changes

## Troubleshooting

1. **CUDA Issues**: The backend is configured to fall back to CPU if CUDA issues occur
2. **Port Conflicts**: Backend uses port 8000, frontend uses port 3000
3. **Dependencies**: Make sure all packages are installed in the virtual environment

## Project Structure

```
├── backend/               # Integrated FastAPI Backend with Gemini AI
│   ├── main.py            # Main FastAPI application
│   ├── requirements.txt   # Backend dependencies
│   ├── routes/            # API routes (chat, levels)
│   ├── services/          # Gemini AI service and memory management
│   └── models/            # Pydantic data models
├── reflex-chat/           # Reflex Frontend
│   ├── chat/              # Main chat application with API integration
│   ├── requirements.txt   # Frontend dependencies (including httpx)
│   ├── rxconfig.py        # Reflex configuration
│   └── assets/            # Static assets
├── app/                   # Legacy Backend (for testing)
│   ├── main.py            # Original FastAPI application
│   └── ...               # Original structure preserved
├── run_backend.sh         # Integrated backend startup script
├── run-old-backend.sh     # Legacy backend startup script
├── run_frontend.sh        # Frontend startup script
└── setup.sh              # Setup script for all components
```