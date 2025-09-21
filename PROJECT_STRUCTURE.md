# 📁 FloatChat Repository & File Structure

## **🏗️ Project Overview**
FloatChat is a comprehensive AI-powered ARGO float ocean data platform built with a modern full-stack architecture.

## **📂 Root Directory Structure**

```
floatchat/
├── .env                              # Environment variables
├── .github/                          # GitHub workflows & templates
├── .gitignore                        # Git ignore rules
├── README.md                         # Main project documentation
├── SYSTEM_STATUS.md                  # Current system status report
├── floatchat.db                     # SQLite database
├── load_data.py                      # Data loading utilities
├── quick_setup.py                    # Enhanced setup script
├── quickstart.sh                     # Quick start shell script
├── simple_setup.py                   # Simple setup script
├── setup_enhanced_system.py          # Enhanced system setup
├── start_backend.py                  # Backend startup script
├── test_system.py                    # System testing utilities
├── vectorstore/                      # Vector database storage
├── logs/                            # Application logs
├── docs/                            # Documentation files
├── data/                            # Data storage
├── sample_data/                     # Sample datasets
├── scripts/                         # Utility scripts
├── tests/                           # Test files
├── docker-compose.yml               # Docker Compose configuration
├── docker-compose.prod.yml          # Production Docker Compose
└── backend/                         # Backend application
    └── frontend/                    # Frontend applications
```

## **🔧 Backend Structure**

### **Backend Root** (`backend/`)
```
backend/
├── .venv/                           # Python virtual environment
├── Dockerfile                       # Backend Docker configuration
├── requirements.txt                 # Core Python dependencies
├── requirements-local.txt           # Local development dependencies
├── requirements_enhanced.txt        # Enhanced dependencies
└── app/                             # FastAPI application
```

### **FastAPI Application** (`backend/app/`)
```
backend/app/
├── __pycache__/                     # Python cache files
├── analytics.py                     # Analytics engine
├── api/                             # API utilities
├── cli_init_db.py                   # Database initialization CLI
├── crud.py                          # Database CRUD operations
├── db.py                            # Database configuration
├── main.py                          # FastAPI application entry point
├── models.py                        # Database models
├── models/                          # Additional model definitions
├── rag.py                           # RAG (Retrieval-Augmented Generation) system
├── realtime.py                      # Real-time WebSocket functionality
├── routers.py                       # Chat API routes
├── routes_data.py                   # Data API routes
├── services/                        # Service layer
└── startup.py                       # Application startup configuration
```

## **🎨 Frontend Structure**

### **Frontend Root** (`frontend/`)
```
frontend/
├── streamlit/                       # Streamlit dashboard
│   ├── app.py                      # Streamlit application
│   ├── requirements.txt            # Streamlit dependencies
│   └── Dockerfile                  # Streamlit Docker config
└── web/                             # React + TypeScript web app
```

### **React Web Application** (`frontend/web/`)
```
frontend/web/
├── .env                             # Frontend environment variables
├── Dockerfile                       # Frontend Docker configuration
├── index.html                       # Main HTML file
├── package.json                     # Node.js dependencies
├── package-lock.json                # Dependency lock file
├── postcss.config.js               # PostCSS configuration
├── tailwind.config.js              # Tailwind CSS configuration
├── tsconfig.json                    # TypeScript configuration
├── vite.config.ts                   # Vite build configuration
├── dist/                           # Build output directory
├── node_modules/                   # Node.js dependencies
├── public/                         # Public static assets
└── src/                            # Source code
```

### **React Source Code** (`frontend/web/src/`)
```
frontend/web/src/
├── App.tsx                         # Main React application
├── main.tsx                        # React entry point
├── index.css                       # Global CSS styles
├── styles.css                      # Additional styles
├── data/                           # Data utilities
├── lib/                            # Utility libraries
└── components/                     # React components
```

### **React Components** (`frontend/web/src/components/`)
```
frontend/web/src/components/
├── App.tsx                         # Main app component
├── ChatInterface.tsx               # AI chat interface
├── DataVisualization.tsx           # Data visualization charts
├── HelpModal.tsx                   # Help modal component
├── InsertData.tsx                  # Data insertion interface
├── MapVisualization.tsx            # Interactive map component
├── Layout/                         # Layout components
├── components.tsx                  # Component utilities
└── ui/                             # UI component library
    ├── Button.tsx                  # Button component
    ├── Card.tsx                    # Card component
    ├── Input.tsx                   # Input component
    └── Badge.tsx                   # Badge component
```

## **🗃️ Data & Configuration**

### **Sample Data** (`sample_data/`)
```
sample_data/
├── argo_profiles_sample.csv        # Sample ARGO profile data
├── argo_profiles_sample.json       # Sample data in JSON format
├── argo_profiles_sample.nc         # Sample NetCDF data
└── sample_profiles.py              # Sample data generation script
```

### **Scripts & Utilities** (`scripts/`)
```
scripts/
├── setup_database.py               # Database setup utilities
├── data_preprocessing.py           # Data preprocessing scripts
├── api_testing.py                  # API testing utilities
├── deployment.py                   # Deployment scripts
└── monitoring.py                   # System monitoring scripts
```

## **🐳 Docker Configuration**

### **Docker Compose Files**
```
├── docker-compose.yml              # Development Docker Compose
├── docker-compose.prod.yml         # Production Docker Compose
├── backend/Dockerfile              # Backend Docker image
├── frontend/web/Dockerfile         # Frontend Docker image
└── frontend/streamlit/Dockerfile   # Streamlit Docker image
```

## **📚 Documentation & Testing**

### **Documentation** (`docs/`)
```
docs/
├── API_REFERENCE.md                # API documentation
├── DEPLOYMENT.md                   # Deployment guide
├── DEVELOPMENT.md                  # Development guide
├── ARCHITECTURE.md                 # System architecture
└── USER_GUIDE.md                   # User manual
```

### **Testing** (`tests/`)
```
tests/
├── test_api.py                     # API endpoint tests
├── test_database.py                # Database operation tests
├── test_rag.py                     # RAG system tests
└── test_components.py              # Component integration tests
```

## **⚙️ Configuration Files**

### **Environment Configuration**
```
├── .env                            # Root environment variables
├── backend/.env                    # Backend environment variables
├── frontend/web/.env               # Frontend environment variables
└── frontend/streamlit/.env         # Streamlit environment variables
```

### **Git & CI/CD**
```
├── .github/                        # GitHub workflows
│   ├── workflows/
│   └── templates/
├── .gitignore                      # Git ignore rules
└── docker-compose.*.yml            # Docker configurations
```

## **🔧 Key Technologies Used**

### **Backend Stack**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL/PostGIS** - Primary database
- **SQLite** - Development database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### **Frontend Stack**
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Leaflet** - Interactive maps
- **Recharts** - Data visualization
- **Framer Motion** - Animations

### **AI & Data Processing**
- **RAG (Retrieval-Augmented Generation)** - AI chat system
- **Vector Databases** - Semantic search
- **NetCDF** - Scientific data format
- **Pandas** - Data analysis
- **NumPy** - Numerical computing

### **DevOps & Deployment**
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD
- **Nginx** - Reverse proxy
- **SSL/TLS** - Security

## **🚀 Quick Start Commands**

```bash
# Backend Setup
python start_backend.py

# Frontend Setup
cd frontend/web && npm install && npm run dev

# Full System Setup
python quick_setup.py

# Database Initialization
python backend/app/cli_init_db.py

# System Testing
python test_system.py
```

This comprehensive structure supports a full-featured ARGO float data analysis platform with AI-powered chat, interactive visualizations, and real-time data processing capabilities.

---

*Generated on: 2025-09-20T21:41:30+05:30*
