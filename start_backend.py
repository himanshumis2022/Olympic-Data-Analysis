#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
if backend_dir.exists():
    sys.path.insert(0, str(backend_dir))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if __name__ == "__main__":
    try:
        import uvicorn
        print("Starting FloatChat Backend...")
        print("Backend: http://localhost:8000")
        print("API Docs: http://localhost:8000/docs")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except ImportError:
        print("uvicorn not installed. Install with: pip install uvicorn")
    except Exception as e:
        print(f"Failed to start: {e}")
