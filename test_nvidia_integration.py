#!/usr/bin/env python3
"""
Test script for NVIDIA integration in Navi
Tests the NVIDIA agent functionality without requiring Google Maps API keys
"""

import json
from nvidia_agent import NVIDIAAgent
from starter import NVIDIAIntentParser

def test_nvidia_agent():
    """Test the NVIDIA agent basic functionality"""
    print("🧪 Testing NVIDIA Agent...")
    
    try:
        agent = NVIDIAAgent()
        print("✅ NVIDIA Agent initialized successfully")
        
        # Test intent parsing
        print("\n📝 Testing intent parsing...")
        intent = agent.parse_intent(
            "I want a scenic route from UC Berkeley to Castro Valley",
            "2607:f140:6000:800e:384d:a5ee:7eb4:fa5e"
        )
        print("✅ Intent parsing successful")
        print(f"   Intent type: {intent.get('intent_type', 'Unknown')}")
        print(f"   Origin: {intent.get('origin', 'Unknown')}")
        print(f"   Destination: {intent.get('destination', 'Unknown')}")
        
        # Test route planning
        print("\n🗺️ Testing route planning...")
        waypoints = agent.plan_route(intent)
        print("✅ Route planning successful")
        print(f"   Generated {len(waypoints)} waypoints")
        
        # Test fitness optimization
        print("\n💪 Testing fitness optimization...")
        current_route = [
            {"name": "UC Berkeley", "lat": 37.8712141, "lng": -122.255463},
            {"name": "Castro Valley", "lat": 37.6955029, "lng": -122.0738678}
        ]
        constraints = ["burn 100 calories", "avoid hills"]
        current_metrics = {"distance_m": 5000, "duration_s": 1800, "calories": 50}
        
        extras = agent.optimize_fitness_route(
            current_route=current_route,
            constraints=constraints,
            mode="walking",
            current_metrics=current_metrics
        )
        print("✅ Fitness optimization successful")
        print(f"   Suggested {len(extras)} extra waypoints")
        
        # Test general chat
        print("\n💬 Testing general chat...")
        response = agent.chat("What's the best way to plan a scenic route?")
        print("✅ General chat successful")
        print(f"   Response length: {len(response)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_nvidia_intent_parser():
    """Test the NVIDIA intent parser"""
    print("\n🧪 Testing NVIDIA Intent Parser...")
    
    try:
        parser = NVIDIAIntentParser()
        print("✅ NVIDIA Intent Parser initialized successfully")
        
        # Test prompt parsing
        print("\n📝 Testing prompt parsing...")
        intent = parser.parse_prompt(
            "I want a 10,000-step fitness walk starting at UC Berkeley",
            "2607:f140:6000:800e:384d:a5ee:7eb4:fa5e"
        )
        print("✅ Prompt parsing successful")
        print(f"   Intent type: {intent.intent_type}")
        print(f"   Origin: {intent.origin}")
        print(f"   Constraints: {intent.constraints}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 NVIDIA Integration Test Suite")
    print("=" * 50)
    
    # Test NVIDIA Agent
    agent_success = test_nvidia_agent()
    
    # Test NVIDIA Intent Parser
    parser_success = test_nvidia_intent_parser()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   NVIDIA Agent: {'✅ PASS' if agent_success else '❌ FAIL'}")
    print(f"   NVIDIA Intent Parser: {'✅ PASS' if parser_success else '❌ FAIL'}")
    
    if agent_success and parser_success:
        print("\n🎉 All tests passed! NVIDIA integration is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 