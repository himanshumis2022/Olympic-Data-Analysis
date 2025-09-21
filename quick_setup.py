#!/usr/bin/env python3
"""
Quick setup for FloatChat - works with minimal dependencies
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_basic_environment():
    """Setup basic environment without external dependencies"""
    logger.info("🚀 Starting FloatChat Quick Setup")
    
    project_root = Path(__file__).parent
    
    # Create basic directories
    directories = [
        project_root / "data",
        project_root / "data" / "uploads", 
        project_root / "data" / "processed",
        project_root / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Created: {directory}")
    
    # Create basic .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        env_content = """# FloatChat Environment Configuration
# Basic setup - update as needed

# Database (SQLite for development)
DATABASE_URL=sqlite:///./floatchat.db
DB_TYPE=sqlite

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=dev-secret-key-change-in-production

# LLM Configuration (add your keys)
OPENAI_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-3.5-turbo

# Development
DEBUG=true
LOG_LEVEL=INFO

# Frontend
VITE_API_URL=http://localhost:8000
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        logger.info(f"✓ Created .env file: {env_file}")
    
    # Install basic Python dependencies
    try:
        logger.info("Installing basic Python dependencies...")
        
        basic_deps = [
            "fastapi==0.104.1",
            "uvicorn==0.24.0", 
            "sqlalchemy==2.0.23",
            "pydantic==2.5.0",
            "python-multipart==0.0.6",
            "python-dotenv==1.0.0",
            "pandas==2.1.4",
            "numpy==1.24.4"
        ]
        
        for dep in basic_deps:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            logger.info(f"✓ Installed: {dep}")
        
    except subprocess.CalledProcessError as e:
        logger.warning(f"Some dependencies failed to install: {e}")
    
    # Create simple backend startup script
    backend_script = project_root / "start_backend_simple.py"
    backend_content = '''#!/usr/bin/env python3
"""Simple backend startup for FloatChat"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
if backend_dir.exists():
    sys.path.insert(0, str(backend_dir))

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not available, using environment variables")

# Simple server
if __name__ == "__main__":
    try:
        import uvicorn
        print("🚀 Starting FloatChat Backend...")
        print("📍 Backend will be available at: http://localhost:8000")
        print("📖 API docs at: http://localhost:8000/docs")
        
        uvicorn.run(
            "app.main:app" if Path("backend/app/main.py").exists() else "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except ImportError:
        print("❌ uvicorn not installed. Install with: pip install uvicorn")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
'''
    
    with open(backend_script, 'w') as f:
        f.write(backend_content)
    
    # Create simple frontend startup script  
    frontend_script = project_root / "start_frontend_simple.py"
    frontend_content = '''#!/usr/bin/env python3
"""Simple frontend startup for FloatChat"""

import os
import subprocess
import webbrowser
from pathlib import Path
import time

def start_frontend():
    frontend_dir = Path(__file__).parent / "frontend" / "web"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        print("📁 Expected: frontend/web/")
        return
    
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(["npm", "install"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ npm not found. Please install Node.js and npm")
            print("🔗 Download from: https://nodejs.org/")
            return
    
    print("🚀 Starting FloatChat Frontend...")
    print("📍 Frontend will be available at: http://localhost:3000")
    
    # Start development server
    try:
        subprocess.run(["npm", "run", "dev"])
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Failed to start frontend server")

if __name__ == "__main__":
    start_frontend()
'''
    
    with open(frontend_script, 'w') as f:
        f.write(frontend_content)
    
    # Create sample data loader
    data_loader = project_root / "load_sample_data.py"
    data_content = '''#!/usr/bin/env python3
"""Load sample data into FloatChat"""

import json
import sqlite3
from pathlib import Path
import pandas as pd

def load_sample_data():
    """Load sample ARGO data"""
    
    # Database setup
    db_path = Path("floatchat.db")
    conn = sqlite3.connect(db_path)
    
    # Create profiles table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            float_id TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            depth REAL NOT NULL,
            temperature REAL NOT NULL,
            salinity REAL NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Load sample data
    sample_file = Path("sample_data/argo_profiles.csv")
    if sample_file.exists():
        df = pd.read_csv(sample_file)
        df.to_sql('profiles', conn, if_exists='append', index=False)
        print(f"✓ Loaded {len(df)} sample profiles")
    else:
        # Create minimal sample data
        sample_data = [
            (1, "5906468", 25.7617, -80.1918, 10, 26.5, 36.2, 6, 2024, "2024-06-15"),
            (2, "5906468", 25.7520, -80.1850, 50, 24.8, 36.4, 6, 2024, "2024-06-15"),
            (3, "5906469", 0.0, -30.0, 15, 28.2, 35.8, 5, 2024, "2024-05-20"),
            (4, "5906470", -10.5, 45.2, 25, 24.3, 35.1, 7, 2024, "2024-07-10"),
            (5, "5906471", 35.6, -75.4, 30, 23.8, 36.8, 8, 2024, "2024-08-05")
        ]
        
        conn.executemany("""
            INSERT INTO profiles (id, float_id, latitude, longitude, depth, temperature, salinity, month, year, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        
        print("✓ Created minimal sample data")
    
    conn.commit()
    conn.close()
    print(f"✓ Database ready: {db_path}")

if __name__ == "__main__":
    load_sample_data()
'''
    
    with open(data_loader, 'w') as f:
        f.write(data_content)
    
    logger.info("🎉 Quick Setup Completed!")
    
    # Print instructions
    print("\n" + "="*60)
    print("FLOATCHAT QUICK SETUP COMPLETE!")
    print("="*60)
    print("📋 NEXT STEPS:")
    print()
    print("1. 🔑 Add your OpenAI API key to .env file:")
    print("   OPENAI_API_KEY=your_actual_key_here")
    print()
    print("2. 📊 Load sample data:")
    print("   python load_sample_data.py")
    print()
    print("3. 🚀 Start the backend:")
    print("   python start_backend_simple.py")
    print()
    print("4. 🌐 Start the frontend (in another terminal):")
    print("   python start_frontend_simple.py")
    print()
    print("5. 🎯 Access FloatChat:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print()
    print("📝 OPTIONAL ENHANCEMENTS:")
    print("- Install PostgreSQL for production database")
    print("- Install Node.js/npm for frontend development")
    print("- Add vector database (pip install faiss-cpu)")
    print("- Add NetCDF processing (pip install xarray netcdf4)")
    print("="*60)

if __name__ == "__main__":
    setup_basic_environment()
