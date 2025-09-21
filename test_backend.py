#!/usr/bin/env python3
"""
Standalone test for backend API components
"""
import sys
import os
sys.path.append('backend')

def test_database():
    """Test database connection and queries"""
    try:
        from app.db import DATABASE_URL
        from sqlalchemy import create_engine
        from app.crud import query_profiles

        print("Testing database connection...")
        engine = create_engine(DATABASE_URL)
        print(f"Database URL: {DATABASE_URL}")

        # Test basic connection
        with engine.begin() as conn:
            result = conn.execute("SELECT COUNT(*) FROM profiles")
            count = result.scalar()
            print(f"Total profiles in database: {count}")

            # Test query_profiles function
            rows = query_profiles(engine, limit=5)
            print(f"Query returned {len(rows)} profiles")
            if rows:
                print("Sample profile:", rows[0])

        return True
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_app():
    """Test creating a minimal FastAPI app"""
    try:
        from fastapi import FastAPI, Query
        from fastapi.responses import JSONResponse
        from sqlalchemy import create_engine
        from app.db import DATABASE_URL
        from app.crud import query_profiles

        print("Testing FastAPI app creation...")

        # Create minimal app
        app = FastAPI(title="FloatChat Test API")

        # Add routes
        @app.get("/health")
        async def health():
            return {"status": "ok"}

        @app.get("/data/profiles")
        async def profiles(limit: int = Query(1000, ge=1, le=5000)):
            try:
                engine = create_engine(DATABASE_URL)
                rows = query_profiles(engine, limit=limit)
                return {"results": rows}
            except Exception as e:
                return {"error": str(e)}

        print("FastAPI app created successfully!")
        print("Available routes:")
        for route in app.routes:
            if hasattr(route, 'path'):
                print(f"  {route.path} - {getattr(route, 'methods', 'N/A')}")

        return app
    except Exception as e:
        print(f"FastAPI test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=== FloatChat Backend Test ===")

    # Test database first
    db_ok = test_database()
    if not db_ok:
        print("Database test failed, cannot continue")
        sys.exit(1)

    # Test FastAPI app
    app = test_fastapi_app()
    if app:
        print("\n=== Starting test server ===")
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    else:
        print("FastAPI test failed")
