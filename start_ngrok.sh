#!/bin/bash

echo "🌐 Starting ngrok tunnel to localhost:8000"
echo "Make sure your Flask server is running on port 8000 first!"
echo ""
echo "Starting ngrok..."
ngrok http 8000 