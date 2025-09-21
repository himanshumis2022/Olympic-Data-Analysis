#!/usr/bin/env python3
"""Simple test to check if the backend can start"""

import os
import sys

# Set environment
os.environ['ENV'] = 'dev'

try:
    print("🔍 Testing imports...")
    from app.db import Base, engine
    print("✅ Database imports successful")

    from app.models import Profile
    print("✅ Models imported successfully")

    from app.main import app
    print("✅ Main app imported successfully")

    print("🎉 All imports successful! Backend should work.")

except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
