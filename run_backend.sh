#!/bin/bash

# Activate the virtual environment
source ~/venv_hacktober25/bin/activate

# Navigate to the backend directory
cd "$(dirname "$0")/backend"

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Run the integrated FastAPI backend
echo "Starting Galician Tutor Backend on http://localhost:8000"
echo "API Documentation available at: http://localhost:8000/docs"
echo "Backend integrates with Reflex frontend for Gemini AI responses"
echo ""
python main.py