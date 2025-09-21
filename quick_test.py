#!/usr/bin/env python3
"""
Quick test of FloatChat backend
"""

import requests
import json

def quick_test():
    """Quick test of the backend"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Quick FloatChat Backend Test")
    print("="*40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"   Response: {response.json()}")
        else:
            print(f"⚠️  Backend responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test API docs endpoint
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API Documentation is accessible")
        else:
            print(f"⚠️  API docs responded with status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  API docs error: {e}")
    
    print("="*40)
    print("🌐 Access URLs:")
    print(f"   Backend API: {base_url}")
    print(f"   API Documentation: {base_url}/docs")
    print(f"   Interactive API: {base_url}/redoc")
    print("="*40)
    
    return True

if __name__ == "__main__":
    quick_test()
