#!/usr/bin/env python3
"""
Ultra-simple test server on different port
"""
from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "Server is working!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("Starting ultra-simple server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
