#!/usr/bin/env python3
"""
Setup script for enhanced FloatChat system with NetCDF processing and RAG pipeline
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FloatChatSetup:
    """Setup and configuration for enhanced FloatChat system"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend" / "web"
        self.sample_data_dir = self.project_root / "sample_data"
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are installed"""
        logger.info("Checking prerequisites...")
        
        prerequisites = {
            'python': {'command': 'python --version', 'min_version': '3.8'},
            'node': {'command': 'node --version', 'min_version': '16.0'},
            'npm': {'command': 'npm --version', 'min_version': '8.0'},
            'postgresql': {'command': 'psql --version', 'min_version': '12.0'}
        }
        
        all_good = True
        
        for name, info in prerequisites.items():
            try:
                result = subprocess.run(
                    info['command'].split(),
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(f"✓ {name}: {result.stdout.strip()}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error(f"✗ {name}: Not found or not working")
                all_good = False
        
        return all_good
    
    def setup_python_environment(self):
        """Setup Python virtual environment and install dependencies"""
        logger.info("Setting up Python environment...")
        
        # Create virtual environment if it doesn't exist
        venv_path = self.project_root / "venv"
        if not venv_path.exists():
            logger.info("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        
        # Determine activation script
        if os.name == 'nt':  # Windows
            activate_script = venv_path / "Scripts" / "activate.bat"
            pip_path = venv_path / "Scripts" / "pip.exe"
        else:  # Unix/Linux/Mac
            activate_script = venv_path / "bin" / "activate"
            pip_path = venv_path / "bin" / "pip"
        
        # Install enhanced requirements
        requirements_file = self.backend_dir / "requirements_enhanced.txt"
        if requirements_file.exists():
            logger.info("Installing enhanced Python dependencies...")
            subprocess.run([
                str(pip_path), "install", "-r", str(requirements_file)
            ], check=True)
        else:
            logger.warning("Enhanced requirements file not found, using basic requirements")
            basic_requirements = self.backend_dir / "requirements.txt"
            if basic_requirements.exists():
                subprocess.run([
                    str(pip_path), "install", "-r", str(basic_requirements)
                ], check=True)
    
    def setup_database(self):
        """Setup and initialize database with enhanced schema"""
        logger.info("Setting up database...")
        
        # Database configuration
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'floatchat'),
            'username': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password')
        }
        
        # Create database if it doesn't exist
        try:
            import psycopg2
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
            
            # Connect to PostgreSQL server
            conn = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['username'],
                password=db_config['password']
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_config['database']}'")
            if not cursor.fetchone():
                logger.info(f"Creating database: {db_config['database']}")
                cursor.execute(f"CREATE DATABASE {db_config['database']}")
            
            cursor.close()
            conn.close()
            
            logger.info("✓ Database setup completed")
            
        except ImportError:
            logger.error("psycopg2 not installed. Install with: pip install psycopg2-binary")
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
    
    def run_database_migrations(self):
        """Run database migrations to create enhanced schema"""
        logger.info("Running database migrations...")
        
        try:
            # Change to backend directory
            original_cwd = os.getcwd()
            os.chdir(self.backend_dir)
            
            # Run Alembic migrations
            subprocess.run(["alembic", "upgrade", "head"], check=True)
            
            logger.info("✓ Database migrations completed")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Migration failed: {e}")
        finally:
            os.chdir(original_cwd)
    
    def populate_sample_data(self):
        """Populate database with sample ARGO data"""
        logger.info("Populating sample data...")
        
        # Check if sample data exists
        sample_sql = self.sample_data_dir / "populate_database.sql"
        sample_csv = self.sample_data_dir / "argo_profiles.csv"
        
        if sample_sql.exists():
            try:
                # Run SQL script
                db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/floatchat')
                subprocess.run([
                    "psql", db_url, "-f", str(sample_sql)
                ], check=True)
                
                logger.info("✓ Sample data populated from SQL script")
                
            except subprocess.CalledProcessError:
                logger.warning("SQL script failed, trying CSV import...")
                self._import_csv_data(sample_csv)
        
        elif sample_csv.exists():
            self._import_csv_data(sample_csv)
        
        else:
            logger.warning("No sample data found. Generate with: python sample_data/generate_sample_data.py")
    
    def _import_csv_data(self, csv_file: Path):
        """Import CSV data using pandas"""
        try:
            import pandas as pd
            from sqlalchemy import create_engine
            
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Create database connection
            db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/floatchat')
            engine = create_engine(db_url)
            
            # Import data
            df.to_sql('profiles', engine, if_exists='append', index=False)
            
            logger.info(f"✓ Imported {len(df)} profiles from CSV")
            
        except Exception as e:
            logger.error(f"CSV import failed: {e}")
    
    def setup_frontend(self):
        """Setup frontend dependencies and build"""
        logger.info("Setting up frontend...")
        
        if not self.frontend_dir.exists():
            logger.error("Frontend directory not found")
            return
        
        # Change to frontend directory
        original_cwd = os.getcwd()
        os.chdir(self.frontend_dir)
        
        try:
            # Install dependencies
            logger.info("Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
            
            # Build frontend (optional)
            if input("Build frontend for production? (y/N): ").lower() == 'y':
                logger.info("Building frontend...")
                subprocess.run(["npm", "run", "build"], check=True)
            
            logger.info("✓ Frontend setup completed")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Frontend setup failed: {e}")
        finally:
            os.chdir(original_cwd)
    
    def setup_environment_variables(self):
        """Setup environment variables"""
        logger.info("Setting up environment variables...")
        
        env_file = self.project_root / ".env"
        
        if env_file.exists():
            logger.info("✓ .env file already exists")
            return
        
        # Default environment variables
        env_vars = {
            # Database
            'DATABASE_URL': 'postgresql://postgres:password@localhost/floatchat',
            'DB_HOST': 'localhost',
            'DB_PORT': '5432',
            'DB_NAME': 'floatchat',
            'DB_USER': 'postgres',
            'DB_PASSWORD': 'password',
            
            # API
            'API_HOST': '0.0.0.0',
            'API_PORT': '8000',
            'SECRET_KEY': 'your-secret-key-change-this-in-production',
            
            # LLM Configuration
            'OPENAI_API_KEY': 'your-openai-api-key',
            'LLM_MODEL': 'gpt-3.5-turbo',
            
            # Vector Database
            'VECTOR_DB_PATH': './data/vector_db',
            'EMBEDDING_MODEL': 'all-MiniLM-L6-v2',
            
            # NetCDF Processing
            'NETCDF_UPLOAD_DIR': './data/uploads',
            'NETCDF_PROCESSED_DIR': './data/processed',
            
            # Frontend
            'VITE_API_URL': 'http://localhost:8000',
            
            # Development
            'DEBUG': 'true',
            'LOG_LEVEL': 'INFO'
        }
        
        # Write environment file
        with open(env_file, 'w') as f:
            f.write("# FloatChat Environment Configuration\n")
            f.write("# Generated by setup script\n\n")
            
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        logger.info(f"✓ Created .env file: {env_file}")
        logger.warning("⚠️  Please update the .env file with your actual API keys and passwords!")
    
    def create_data_directories(self):
        """Create necessary data directories"""
        logger.info("Creating data directories...")
        
        directories = [
            self.project_root / "data",
            self.project_root / "data" / "uploads",
            self.project_root / "data" / "processed",
            self.project_root / "data" / "vector_db",
            self.project_root / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"✓ Created: {directory}")
    
    def generate_startup_scripts(self):
        """Generate startup scripts for development"""
        logger.info("Generating startup scripts...")
        
        # Backend startup script
        backend_script = self.project_root / "start_backend.py"
        backend_content = '''#!/usr/bin/env python3
"""Start FloatChat backend server"""

import os
import sys
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Start server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True
    )
'''
        
        with open(backend_script, 'w') as f:
            f.write(backend_content)
        
        # Frontend startup script
        frontend_script = self.project_root / "start_frontend.py"
        frontend_content = '''#!/usr/bin/env python3
"""Start FloatChat frontend development server"""

import os
import subprocess
from pathlib import Path

# Change to frontend directory
frontend_dir = Path(__file__).parent / "frontend" / "web"
os.chdir(frontend_dir)

# Start development server
subprocess.run(["npm", "run", "dev"])
'''
        
        with open(frontend_script, 'w') as f:
            f.write(frontend_content)
        
        # Make scripts executable on Unix systems
        if os.name != 'nt':
            os.chmod(backend_script, 0o755)
            os.chmod(frontend_script, 0o755)
        
        logger.info("✓ Generated startup scripts")
    
    def run_setup(self):
        """Run complete setup process"""
        logger.info("🚀 Starting FloatChat Enhanced Setup")
        
        try:
            # Check prerequisites
            if not self.check_prerequisites():
                logger.error("❌ Prerequisites check failed. Please install missing components.")
                return False
            
            # Setup steps
            self.setup_environment_variables()
            self.create_data_directories()
            self.setup_python_environment()
            self.setup_database()
            self.run_database_migrations()
            self.populate_sample_data()
            self.setup_frontend()
            self.generate_startup_scripts()
            
            logger.info("🎉 FloatChat Enhanced Setup Completed Successfully!")
            
            # Print next steps
            print("\n" + "="*60)
            print("NEXT STEPS:")
            print("="*60)
            print("1. Update .env file with your API keys:")
            print("   - OPENAI_API_KEY for LLM functionality")
            print("   - Database credentials if different")
            print()
            print("2. Start the backend server:")
            print("   python start_backend.py")
            print()
            print("3. Start the frontend server (in another terminal):")
            print("   python start_frontend.py")
            print()
            print("4. Access FloatChat at: http://localhost:3000")
            print()
            print("5. Test NetCDF processing:")
            print("   - Upload NetCDF files via API")
            print("   - Try natural language queries")
            print("="*60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            return False

def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup FloatChat Enhanced System")
    parser.add_argument("--project-root", help="Project root directory")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend setup")
    parser.add_argument("--skip-sample-data", action="store_true", help="Skip sample data population")
    
    args = parser.parse_args()
    
    setup = FloatChatSetup(args.project_root)
    
    if setup.run_setup():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
