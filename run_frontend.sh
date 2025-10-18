#!/bin/bash

# Activate the virtual environment
source ~/venv_hacktober25/bin/activate

# Navigate to the reflex-chat directory
cd "$(dirname "$0")/reflex-chat"

# Install reflex dependencies if needed
echo "Checking reflex installation and dependencies..."
pip install -r requirements.txt

# Run the Reflex frontend
echo "Starting Reflex frontend with Galician Tutor integration..."
echo "Frontend will connect to backend at http://localhost:8000"
echo "Make sure the backend is running with './run_backend.sh'"
echo ""
reflex run