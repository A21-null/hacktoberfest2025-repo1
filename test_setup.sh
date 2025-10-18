#!/bin/bash

# Test script to verify the local setup works
source ~/venv_hacktober25/bin/activate

echo "Testing backend dependencies..."
cd app
python -c "
import fastapi
import uvicorn
import whisper
import torch
print('✓ All backend dependencies available')
"

echo "Testing frontend dependencies..."
cd ../reflex-chat
python -c "
import reflex
print('✓ Reflex available')
"

echo ""
echo "✓ Local setup verification complete!"
echo "Run ./run_backend.sh and ./run_frontend.sh to start the application."