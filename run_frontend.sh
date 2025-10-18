#!/bin/bash

# Activate the virtual environment
source ~/venv_hacktober25/bin/activate

# Navigate to the reflex-chat directory
cd "$(dirname "$0")/reflex-chat"

# Install reflex dependencies if needed
echo "Checking reflex installation..."
pip install -r requirements.txt

# Run the Reflex frontend
echo "Starting Reflex frontend..."
reflex run