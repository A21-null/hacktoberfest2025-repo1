#!/bin/bash

# Activate the virtual environment
source ~/venv_hacktober25/bin/activate

# Navigate to the app directory
cd "$(dirname "$0")/app"

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Run the FastAPI backend
echo "Starting FastAPI backend on http://localhost:8000"
python main.py