#!/usr/bin/env python3
"""
Script to start Flask server and ngrok tunnel
"""

import os
import time
import threading
import subprocess
import signal
import sys
from main import app

def start_flask_server():
    """Start the Flask server"""
    print("🚀 Starting Flask server on port 8000...")
    app.run(debug=False, host='127.0.0.1', port=8000, use_reloader=False)

def start_ngrok():
    """Start ngrok tunnel"""
    print("🌐 Starting ngrok tunnel...")
    time.sleep(2)  # Wait for Flask to start
    try:
        # Start ngrok tunnel
        subprocess.run(["ngrok", "http", "8000"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Ngrok stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ngrok error: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n🛑 Shutting down servers...')
    sys.exit(0)

if __name__ == "__main__":
    print("🚀 Starting NVIDIA Navigation API with ngrok tunnel...")
    
    # Ensure environment variables are set before running
    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        print("❌ ERROR: GOOGLE_MAPS_API_KEY environment variable is required!")
        print("Set it with: export GOOGLE_MAPS_API_KEY=your_key_here")
        exit(1)
    
    if not os.getenv("NVIDIA_API_KEY"):
        print("❌ ERROR: NVIDIA_API_KEY environment variable is required!")
        print("Set it with: export NVIDIA_API_KEY=your_key_here")
        exit(1)
    
    try:
        # Handle Ctrl+C
        signal.signal(signal.SIGINT, signal_handler)
        
        print("🎯 NVIDIA Navigation API with ngrok")
        print("=" * 50)
        
        # Start Flask server in background thread
        flask_thread = threading.Thread(target=start_flask_server, daemon=True)
        flask_thread.start()
        
        # Start ngrok (this will block)
        start_ngrok() 
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        sys.exit(0) 