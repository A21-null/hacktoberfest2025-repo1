#!/bin/bash

echo "🚀 Testing Galician Tutor Integration"
echo "=====================================\n"

# Test 1: Check if backend is accessible
echo "1. Testing backend health check..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is running and accessible"
    curl -s http://localhost:8000/api/chat/health | python3 -m json.tool
else
    echo "❌ Backend is not accessible. Make sure to run ./run_backend.sh first"
    exit 1
fi

echo "\n2. Testing levels endpoint..."
curl -s http://localhost:8000/api/chat/levels | python3 -m json.tool

echo "\n3. Testing chat message endpoint..."
curl -s -X POST http://localhost:8000/api/chat/message \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": "test_user", 
        "message": "Ola, como estas?", 
        "level_index": 1,
        "mode": "conversation"
    }' | python3 -m json.tool

echo "\n✅ Integration test completed!"
echo "Frontend should connect to backend at http://localhost:8000"
echo "Start frontend with: ./run_frontend.sh"