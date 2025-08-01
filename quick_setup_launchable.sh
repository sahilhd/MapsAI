#!/bin/bash

echo "🚀 Setting up NVIDIA Navigation API on Launchable..."

# Create project structure
mkdir -p nvidia-navigation-api
cd nvidia-navigation-api

# Create requirements.txt
cat > requirements.txt << 'EOF'
Flask==2.3.3
googlemaps==4.10.0
pydantic==2.4.2
requests==2.31.0
python-dotenv==1.0.0
EOF

# Create main.py (simplified version)
cat > main.py << 'EOF'
import os
import logging
import traceback
from flask import Flask, request, jsonify
from starter import NVIDIAIntentParser
from scenic_agent import ScenicAgent
from fitness_agent import FitnessAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "🚀 NVIDIA Navigation API is running!",
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "route": "/api/route"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "nvidia-navigation-api"})

@app.route('/api/route', methods=['POST'])
def get_route():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')
        
        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        logger.info(f"Received prompt: {user_prompt}")
        
        # Parse intent using NVIDIA
        intent_parser = NVIDIAIntentParser()
        intent = intent_parser.parse_prompt(user_prompt)
        
        logger.info(f"Intent parsed: {intent.intent_type}")
        
        # Always use ScenicAgent for consistent waypoints format
        logger.info(f"Using Scenic Agent for {intent.intent_type} intent (waypoints format)")
        scenicAgent = ScenicAgent()
        resp = scenicAgent.get_scenic_route(intent)
        
        logger.info("Route generated successfully")
        return jsonify(resp)
        
    except Exception as e:
        logger.error(f"Error processing route: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting NVIDIA Navigation API on port 8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
EOF

# Create a simple test script
cat > test_api.py << 'EOF'
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"Health: {response.status_code} - {response.json()}")
    
    # Test route endpoint
    print("\n🗺️ Testing route endpoint...")
    test_data = {
        "prompt": "I want a scenic route from UC Berkeley to Castro Valley"
    }
    
    response = requests.post(
        f"{base_url}/api/route",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Route: {response.status_code}")
    if response.status_code == 200:
        print("✅ API working!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    test_api()
EOF

echo "✅ Project structure created!"
echo ""
echo "📋 Next steps:"
echo "1. Install dependencies: pip install -r requirements.txt"
echo "2. Set environment variables:"
echo "   export GOOGLE_MAPS_API_KEY=your_key_here"
echo "   export NVIDIA_API_KEY=your_key_here"
echo "3. Run the server: python3 main.py"
echo "4. In another terminal, test: python3 test_api.py"
echo ""
echo "🔑 Your API keys:"
echo "Google Maps: AIzaSyDri5kshKbo_8zv3MujFMVtCAX3boXsg_M"
echo "NVIDIA: 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"
EOF

chmod +x quick_setup_launchable.sh
echo "✅ Quick setup script created!"
echo ""
echo "🎯 COPY THIS SCRIPT TO YOUR LAUNCHABLE TERMINAL:"
echo "1. Look for the Ubuntu terminal window from brev shell"
echo "2. Copy the contents of quick_setup_launchable.sh"
echo "3. Paste and run it there" 