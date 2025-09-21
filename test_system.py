#!/usr/bin/env python3
"""
Test FloatChat system functionality
"""

import requests
import json
import time

def test_floatchat_api():
    """Test the FloatChat API endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("Testing FloatChat API...")
    print("="*50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"OK Health Check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"FAIL Health Check Failed: {e}")
    
    # Test 2: Get profiles
    try:
        response = requests.get(f"{base_url}/data/profiles")
        print(f"OK Get Profiles: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} profiles")
            if data:
                print(f"   Sample: {data[0]}")
    except Exception as e:
        print(f"FAIL Get Profiles Failed: {e}")
    
    # Test 3: Search profiles
    try:
        params = {"lat_min": -90, "lat_max": 90, "limit": 10}
        response = requests.get(f"{base_url}/data/profiles", params=params)
        print(f"OK Search Profiles: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Search returned {len(data)} profiles")
    except Exception as e:
        print(f"FAIL Search Profiles Failed: {e}")
    
    # Test 4: Statistics
    try:
        response = requests.get(f"{base_url}/data/stats")
        print(f"OK Statistics: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Total profiles: {stats.get('total_profiles', 'N/A')}")
            print(f"   Unique floats: {stats.get('unique_floats', 'N/A')}")
    except Exception as e:
        print(f"FAIL Statistics Failed: {e}")
    
    print("="*50)
    print("API Documentation: http://localhost:8000/docs")
    print("Frontend (if running): http://localhost:3000")
    print("="*50)

if __name__ == "__main__":
    # Wait a moment for server to be ready
    time.sleep(2)
    test_floatchat_api()
