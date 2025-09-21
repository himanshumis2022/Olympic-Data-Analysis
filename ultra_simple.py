#!/usr/bin/env python3
"""
Ultra-simple test server
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
    print("Starting ultra-simple server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
