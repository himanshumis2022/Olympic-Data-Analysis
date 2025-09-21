#!/usr/bin/env python3
"""
Simple setup for FloatChat - minimal dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_floatchat():
    """Setup FloatChat with minimal requirements"""
    print("Starting FloatChat Simple Setup...")
    
    project_root = Path(__file__).parent
    
    # Create directories
    directories = [
        project_root / "data",
        project_root / "data" / "uploads", 
        project_root / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created: {directory}")
    
    # Create .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        env_content = """# FloatChat Configuration
DATABASE_URL=sqlite:///./floatchat.db
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=dev-secret-key
OPENAI_API_KEY=your-openai-api-key-here
DEBUG=true
VITE_API_URL=http://localhost:8000
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"Created .env file: {env_file}")
    
    # Install basic dependencies
    try:
        print("Installing basic dependencies...")
        deps = ["fastapi", "uvicorn", "python-dotenv", "pandas", "sqlalchemy"]
        
        for dep in deps:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                             check=True, capture_output=True, text=True)
                print(f"Installed: {dep}")
            except subprocess.CalledProcessError:
                print(f"Failed to install: {dep}")
        
    except Exception as e:
        print(f"Installation error: {e}")
    
    # Create startup scripts
    backend_script = project_root / "start_backend.py"
    backend_content = """#!/usr/bin/env python3
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
"""
    
    with open(backend_script, 'w', encoding='utf-8') as f:
        f.write(backend_content)
    
    # Create data loader
    data_loader = project_root / "load_data.py"
    data_content = """#!/usr/bin/env python3
import sqlite3
from pathlib import Path

def create_sample_data():
    db_path = Path("floatchat.db")
    conn = sqlite3.connect(db_path)
    
    # Create table
    conn.execute('''
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
            date TEXT
        )
    ''')
    
    # Sample data
    data = [
        ("5906468", 25.7617, -80.1918, 10, 26.5, 36.2, 6, 2024, "2024-06-15"),
        ("5906468", 25.7520, -80.1850, 50, 24.8, 36.4, 6, 2024, "2024-06-15"),
        ("5906469", 0.0, -30.0, 15, 28.2, 35.8, 5, 2024, "2024-05-20"),
        ("5906470", -10.5, 45.2, 25, 24.3, 35.1, 7, 2024, "2024-07-10"),
        ("5906471", 35.6, -75.4, 30, 23.8, 36.8, 8, 2024, "2024-08-05")
    ]
    
    conn.executemany('''
        INSERT INTO profiles (float_id, latitude, longitude, depth, temperature, salinity, month, year, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    conn.close()
    print(f"Created database with {len(data)} sample profiles")

if __name__ == "__main__":
    create_sample_data()
"""
    
    with open(data_loader, 'w', encoding='utf-8') as f:
        f.write(data_content)
    
    print("\nSetup Complete!")
    print("="*50)
    print("NEXT STEPS:")
    print("1. Add OpenAI API key to .env file")
    print("2. Run: python load_data.py")
    print("3. Run: python start_backend.py")
    print("4. Open: http://localhost:8000/docs")
    print("="*50)

if __name__ == "__main__":
    setup_floatchat()
