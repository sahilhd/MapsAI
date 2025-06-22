from flask import Flask, request, jsonify
from starter import FetchAIIntentParser
from scenic_agent import ScenicAgent
from fitness_agent import FitnessAgent
from fallback_agent import FallbackAgent
from polyline_agent import PolylineAgent

app = Flask(__name__)
parser = FetchAIIntentParser()

@app.route('/api/route', methods=['POST'])
def get_route():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        user_ipv6 = data.get("ipv6", "2607:f140:6000:800e:384d:a5ee:7eb4:fa5e")  # fallback IPv6

        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        # Parse prompt to RouteIntent
        intent = parser.parse_prompt(prompt, user_ipv6)

        if intent.intent_type == "Scenic":
            scenicAgent = ScenicAgent()
            resp = scenicAgent.get_scenic_route(intent)
        elif intent.intent_type == "Health":
            fitnessAgent = FitnessAgent()
            resp = fitnessAgent.get_fitness_route(intent)
        else:
            fallbackAgent = FallbackAgent()
            resp = fallbackAgent.get_waypoints(intent)
            polylineAgent = PolylineAgent()
            resp = polylineAgent.get_route_summary(intent, resp.waypoints)

        return jsonify({
            "intent": intent.model_dump(),
            "waypoints": resp.model_dump()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
