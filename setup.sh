#!/bin/bash

# Activate the virtual environment
source ~/venv_hacktober25/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd app
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd reflex-chat
pip install -r requirements.txt
cd ..

echo "Setup complete! Use the following commands to run the application:"
echo ""
echo "To start the backend: ./run_backend.sh"
echo "To start the frontend: ./run_frontend.sh"
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000"