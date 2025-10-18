# AI Tutor Gallego - Local Setup

This project consists of two main components:
1. **Backend**: FastAPI application (`/app`)
2. **Frontend**: Reflex application (`/reflex-chat`)

## Prerequisites

- Python virtual environment at `~/venv_hacktober25/bin/activate`
- All necessary libraries should already be installed in this environment

## Quick Start

1. **Setup (first time only):**
   ```bash
   chmod +x setup.sh run_backend.sh run_frontend.sh
   ./setup.sh
   ```

2. **Run Backend:**
   ```bash
   ./run_backend.sh
   ```
   Backend will be available at: http://localhost:8000

3. **Run Frontend (in a separate terminal):**
   ```bash
   ./run_frontend.sh
   ```
   Frontend will be available at: http://localhost:3000

## Manual Setup

### Backend Setup
```bash
source ~/venv_hacktober25/bin/activate
cd app
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

## Environment Variables

Create a `.env` file in the `/app` directory with your configuration:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## API Endpoints

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Frontend Features

The Reflex frontend provides:
- Chat interface for the Galician tutor
- Audio recording and transcription
- User authentication and settings

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
├── app/                    # FastAPI Backend
│   ├── main.py            # Main FastAPI application
│   ├── requirements.txt   # Backend dependencies
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   ├── models/            # Data models
│   └── utils/             # Utilities
├── reflex-chat/           # Reflex Frontend
│   ├── chat/              # Main chat application
│   ├── requirements.txt   # Frontend dependencies
│   ├── rxconfig.py        # Reflex configuration
│   └── assets/            # Static assets
├── run_backend.sh         # Backend startup script
├── run_frontend.sh        # Frontend startup script
└── setup.sh              # Initial setup script
```