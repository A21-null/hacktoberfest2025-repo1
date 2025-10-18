#!/bin/bash

# Activate the virtual environment
source ~/venv_hacktober25/bin/activate

# Install original backend dependencies (for testing)
echo "Installing original backend dependencies..."
cd app
pip install -r requirements.txt
cd ..

# Install new integrated backend dependencies
echo "Installing new integrated backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies (with API integration)..."
cd reflex-chat
pip install -r requirements.txt
cd ..

echo "Setup complete! Use the following commands to run the application:"
echo ""
echo "To start the INTEGRATED backend: ./run_backend.sh"
echo "To start the frontend:          ./run_frontend.sh"
echo "To test the old backend:        ./run-old-backend.sh"
echo ""
echo "Integrated Backend will be available at: http://localhost:8000"
echo "Frontend will be available at:           http://localhost:3000"
echo ""
echo "The integrated setup connects the Reflex frontend to Gemini AI!"
echo "Make sure to set your GEMINI_API_KEY in backend/.env"