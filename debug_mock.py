#!/usr/bin/env python3
"""
Debug script to test mock responses
"""

from nvidia_agent import NVIDIAAgent

def debug_mock_responses():
    agent = NVIDIAAgent(mock_mode=True)
    
    # Test intent parsing
    print("Testing intent parsing...")
    messages = [
        {"role": "system", "content": "You are an intelligent route-planning assistant."},
        {"role": "user", "content": "I want a scenic route from UC Berkeley to Castro Valley"}
    ]
    response = agent._get_mock_response(messages)
    print(f"Mock response: {response}")
    print(f"Response type: {type(response)}")
    print(f"Response length: {len(response)}")
    
    # Test route planning
    print("\nTesting route planning...")
    messages = [
        {"role": "system", "content": "You are a route planner."},
        {"role": "user", "content": "Generate waypoints for a route"}
    ]
    response = agent._get_mock_response(messages)
    print(f"Mock response: {response}")
    print(f"Response type: {type(response)}")
    print(f"Response length: {len(response)}")

if __name__ == "__main__":
    debug_mock_responses() 