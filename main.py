from flask import Flask, request, jsonify
import logging
import traceback
from starter import NVIDIAIntentParser
from scenic_agent import ScenicAgent
from fitness_agent import FitnessAgent
from fallback_agent import FallbackAgent
from polyline_agent import PolylineAgent

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
parser = NVIDIAIntentParser()

@app.route('/api/route', methods=['POST'])
def get_route():
    try:
        logger.info("Received POST request to /api/route")
        
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        prompt = data.get("prompt")
        user_ipv6 = data.get("ipv6", "2607:f140:6000:800e:384d:a5ee:7eb4:fa5e")  # fallback IPv6

        if not prompt:
            logger.error("Missing prompt in request")
            return jsonify({"error": "Missing prompt"}), 400

        logger.info(f"Processing prompt: {prompt}")
        
        # Parse prompt to RouteIntent
        logger.info("Parsing prompt to RouteIntent...")
        intent = parser.parse_prompt(prompt, user_ipv6)
        logger.info(f"Intent parsed: {intent.intent_type}")

        # Route to appropriate agent - Always return waypoints for iOS compatibility
        if intent.intent_type == "Scenic":
            logger.info("Using Scenic Agent")
            scenicAgent = ScenicAgent()
            resp = scenicAgent.get_scenic_route(intent)
        elif intent.intent_type == "Health":
            logger.info("Using Fitness Agent")
            fitnessAgent = FitnessAgent()
            resp = fitnessAgent.get_fitness_route(intent)
        else:
            # For Event, Commute, and Other intents, use Scenic Agent for waypoints format
            logger.info(f"Using Scenic Agent for {intent.intent_type} intent (waypoints format)")
            scenicAgent = ScenicAgent()
            resp = scenicAgent.get_scenic_route(intent)

        logger.info("Preparing response...")
        response = {
            "intent": intent.model_dump(),
            "waypoints": resp.model_dump()
        }
        
        logger.info("Response ready, sending to client")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in get_route: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "message": "NVIDIA Navigation API is running"}), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "NVIDIA Navigation API",
        "endpoints": {
            "POST /api/route": "Submit navigation request",
            "GET /health": "Health check",
            "GET /": "This help message"
        },
        "example_request": {
            "prompt": "Give me a scenic route from UC Berkeley to Castro Valley",
            "ipv6": "optional_ipv6_for_location_context"
        }
    }), 200

if __name__ == '__main__':
    logger.info("Starting Flask application on port 8000...")
    app.run(debug=True, host='0.0.0.0', port=8000)
