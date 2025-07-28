#!/usr/bin/env python3
"""
Test script to start the server and test the API
"""

import os
import time
import threading
import requests
import json
from main import app

def start_server():
    """Start the Flask server in a separate thread"""
    app.run(debug=False, host='127.0.0.1', port=8000, use_reloader=False)

def test_api():
    """Test the API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test health endpoint
        print("\n🩺 Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
        
        # Test home endpoint
        print("\n🏠 Testing home endpoint...")
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Home Status: {response.status_code}")
        print(f"Home Response: {response.json()}")
        
        # Test route endpoint
        print("\n🗺️ Testing route endpoint...")
        test_request = {
            "prompt": "Give me a scenic route from UC Berkeley to Castro Valley"
        }
        
        print(f"Sending request: {test_request}")
        response = requests.post(
            f"{base_url}/api/route", 
            json=test_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Route Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Route Response Keys: {list(result.keys())}")
            print(f"Intent Type: {result['intent']['intent_type']}")
            print(f"Waypoints Count: {len(result['waypoints']['waypoints'])}")
            print("✅ API test successful!")
        else:
            print(f"Route Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    # Ensure environment variables are set before running
    if not os.getenv("GOOGLE_MAPS_API_KEY"):
        print("❌ ERROR: GOOGLE_MAPS_API_KEY environment variable is required!")
        print("Set it with: export GOOGLE_MAPS_API_KEY=your_key_here")
        exit(1)
    
    if not os.getenv("NVIDIA_API_KEY"):
        print("❌ ERROR: NVIDIA_API_KEY environment variable is required!")
        print("Set it with: export NVIDIA_API_KEY=your_key_here")
        exit(1)
    
    print("🚀 Starting NVIDIA Navigation API Test on port 8000")
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test the API
    test_api()
    
    print("\n🎯 Test completed!") 