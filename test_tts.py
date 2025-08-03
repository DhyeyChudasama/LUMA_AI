#!/usr/bin/env python3
"""
Simple test script for the TTS server
Run this after starting the server to test the endpoints
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Root endpoint working\n")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}\n")
        return False

def test_tts_endpoint():
    """Test the TTS endpoint with JSON"""
    print("Testing TTS endpoint (JSON)...")
    
    payload = {
        "text": "Hello! This is a test message from the TTS server.",
        "voice_id": "en-US-Neural2-F",
        "speed": 1.0,
        "pitch": 0.0
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tts",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get("success"):
            print("✅ TTS endpoint working - Audio URL received!")
            print(f"Audio URL: {result.get('audio_url')}")
        else:
            print(f"❌ TTS endpoint failed: {result.get('error')}")
        
        print()
        return result.get("success", False)
        
    except Exception as e:
        print(f"❌ TTS endpoint failed: {e}\n")
        return False

def test_tts_form_endpoint():
    """Test the TTS endpoint with form data"""
    print("Testing TTS endpoint (Form Data)...")
    
    form_data = {
        "text": "This is a test using form data!",
        "voice_id": "en-US-Neural2-F",
        "speed": "1.0",
        "pitch": "0.0"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tts-form",
            data=form_data
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get("success"):
            print("✅ TTS form endpoint working - Audio URL received!")
            print(f"Audio URL: {result.get('audio_url')}")
        else:
            print(f"❌ TTS form endpoint failed: {result.get('error')}")
        
        print()
        return result.get("success", False)
        
    except Exception as e:
        print(f"❌ TTS form endpoint failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting TTS Server Tests")
    print("=" * 50)
    
    # Check if server is running
    print("Checking if server is running...")
    try:
        requests.get(f"{BASE_URL}/", timeout=5)
        print("✅ Server is running\n")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running!")
        print("Please start the server with: python main.py")
        return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    # Run tests
    tests = [
        test_root_endpoint,
        test_tts_endpoint,
        test_tts_form_endpoint
    ]
    
    results = []
    for test in tests:
        results.append(test())
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("=" * 50)
    print("📊 Test Summary:")
    print(f"Root endpoint: {'✅ PASS' if results[0] else '❌ FAIL'}")
    print(f"TTS JSON: {'✅ PASS' if results[1] else '❌ FAIL'}")
    print(f"TTS Form: {'✅ PASS' if results[2] else '❌ FAIL'}")
    
    if all(results):
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check your configuration.")

if __name__ == "__main__":
    main() 