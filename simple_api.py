#!/usr/bin/env python3
"""
Minimal working API server for FloatChat
Serves the profiles data that already exists in the database
"""
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
import os
import sys

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Database setup
from app.db import DATABASE_URL

app = FastAPI(title="FloatChat API", version="0.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database engine
engine = None

def get_engine():
    global engine
    if engine is None:
        engine = create_engine(DATABASE_URL)
    return engine

@app.get("/")
async def root():
    return {"message": "FloatChat API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/data/profiles")
async def get_profiles(
    min_lat: float = Query(None, ge=-90, le=90),
    max_lat: float = Query(None, ge=-90, le=90),
    min_lon: float = Query(None, ge=-180, le=180),
    max_lon: float = Query(None, ge=-180, le=180),
    limit: int = Query(500, ge=1, le=5000)
):
    """Get ARGO float profiles with optional filtering"""
    try:
        # Build query
        clauses = []
        params = {"limit": limit}

        if min_lat is not None:
            clauses.append("lat >= :min_lat")
            params["min_lat"] = min_lat
        if max_lat is not None:
            clauses.append("lat <= :max_lat")
            params["max_lat"] = max_lat
        if min_lon is not None:
            clauses.append("lon >= :min_lon")
            params["min_lon"] = min_lon
        if max_lon is not None:
            clauses.append("lon <= :max_lon")
            params["max_lon"] = max_lon

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""

        query = text(f"""
            SELECT id, lat as latitude, lon as longitude, depth, temperature, salinity, month, year
            FROM profiles{where}
            LIMIT :limit
        """)

        with get_engine().begin() as conn:
            rows = conn.execute(query, params).mappings().all()

        return {"results": [dict(row) for row in rows]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/data/nearest")
async def get_nearest_profiles(lat: float, lon: float, limit: int = 10):
    """Find nearest profiles to given coordinates"""
    try:
        query = text("""
            SELECT id, lat as latitude, lon as longitude, depth, temperature, salinity, month, year,
                   ((lat-:lat)*(lat-:lat) + (lon-:lon)*(lon-:lon)) AS dist2
            FROM profiles
            ORDER BY dist2 ASC
            LIMIT :limit
        """)

        with get_engine().begin() as conn:
            rows = conn.execute(query, {"lat": lat, "lon": lon, "limit": limit}).mappings().all()

        return {"results": [dict(row) for row in rows]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting FloatChat API...")
    print("API available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
