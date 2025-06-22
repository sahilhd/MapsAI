# fallback_agent.py

import os
import json
import re
import googlemaps
from dotenv import load_dotenv
from typing import List, Dict, Any
from pydantic import BaseModel
from models import RouteIntent
from gpt_agent import ChatGPTAgent

# Load environment variables from .env file
load_dotenv()

class FallbackRouteMetrics(BaseModel):
    waypoints: List[Dict[str, Any]]

class FallbackAgent:
    """
    Handles all non-Health intents by:
      1) Prepending any GSR stops after the origin
      2) Delegating to ChatGPT for the full route waypoints
      3) Merging them into one ordered list without duplicates
    """
    def __init__(self, maps_key=None, openai_key=None, model="gpt-3.5-turbo"):
        self.gmaps = googlemaps.Client(key=maps_key or os.getenv("GOOGLE_MAPS_API_KEY"))
        self.gpt   = ChatGPTAgent(api_key=openai_key or os.getenv("OPENAI_API_KEY"),
                                  model=model)

    def _geocode_name(self, place_name: str) -> Dict[str, float]:
        resp = self.gmaps.geocode(place_name)
        if not resp:
            raise RuntimeError(f"Geocoding failed for '{place_name}'")
        loc = resp[0]["geometry"]["location"]
        return {"lat": loc["lat"], "lng": loc["lng"]}

    def get_waypoints(self, intent: RouteIntent) -> FallbackRouteMetrics:
        # 1) Fixed list: origin + GSR stops
        fixed: List[Dict[str, Any]] = [{"name": intent.origin}]
        if intent.stops:
            for stop in intent.stops:
                if gsr := stop.get("gsr"):
                    g = gsr[0]
                    fixed.append({
                        "name": g["name"],
                        "lat": g["latitude"],
                        "lng": g["longitude"]
                    })

        # 2) Ask GPT for full waypoint list
        prompt = (
            f"You are a route planner.\n"
            f"Intent: {intent.intent_type}\n"
            f"Origin: {intent.origin}\n"
            f"Destination: {intent.destination or intent.origin}\n"
            f"Travel modes: {intent.travel_modes or ['driving']}\n"
            f"Constraints: {intent.constraints}\n"
            f"Avoid: {intent.avoid or []}\n"
            f"Stops: {intent.stops or []}\n\n"
            "Return ONLY a JSON array of waypoints "
            "[{\"name\":...,\"lat\":...,\"lng\":...},…]. No explanation."
        )
        raw = self.gpt.chat(prompt, temperature=0.1, max_tokens=300)

        # 3) Extract JSON array
        start, end = raw.find("["), raw.rfind("]")
        if start == -1 or end == -1:
            raise RuntimeError("No JSON array found in GPT response")
        arr_text = raw[start:end+1]
        try:
            gpt_wpts = json.loads(arr_text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON from GPT: {e}\nRaw: {raw}")

        # 4) Geocode any placeholder coordinates
        for wp in gpt_wpts:
            if not isinstance(wp.get("lat"), (int, float)) or not isinstance(wp.get("lng"), (int, float)):
                coords = self._geocode_name(wp["name"])
                wp["lat"], wp["lng"] = coords["lat"], coords["lng"]

        # 5) Merge without duplicates, preserving order:
        merged: List[Dict[str, Any]] = []
        seen = set()
        def key(pt):
            return f"{pt.get('name')}|{pt.get('lat')}|{pt.get('lng')}"

        # a) GPT's origin
        if gpt_wpts:
            merged.append(gpt_wpts[0])
            seen.add(key(gpt_wpts[0]))
        # b) Fixed GSR stops
        for pt in fixed[1:]:
            k = key(pt)
            if k not in seen:
                merged.append(pt)
                seen.add(k)
        # c) GPT's remaining waypoints
        for pt in gpt_wpts[1:]:
            k = key(pt)
            if k not in seen:
                merged.append(pt)
                seen.add(k)
        # d) Fallback if empty
        if not merged:
            merged = fixed

        return FallbackRouteMetrics(waypoints=merged)


# --- Example Usage ---
if __name__ == "__main__":
    from models import RouteIntent
    raw = {
      "intent_type": "Event",
      "origin": "UC Berkeley",
      "destination": "rooftop bar",
      "travel_modes": ["driving"],
      "constraints": ["date night"],
      "avoid": None,
      "optimize_waypoints": True,
      "stops": [
        {
          "name": "sushi",
          "gsr": [{
            "name": "Kura Revolving Sushi Bar",
            "address": "2100 University Ave, Berkeley, CA 94704, United States",
            "latitude": 37.8720247,
            "longitude": -122.2682292
          }]
        },
        {
          "name": "arcade",
          "gsr": [{
            "name": "Game On",
            "address": "1235 Tenth St, Berkeley, CA 94710, United States",
            "latitude": 37.8811533,
            "longitude": -122.2968616
          }]
        }
      ]
    }
    intent = RouteIntent(**raw)
    agent = FallbackAgent()
    metrics = agent.get_waypoints(intent)
    print(metrics.json(indent=2))
