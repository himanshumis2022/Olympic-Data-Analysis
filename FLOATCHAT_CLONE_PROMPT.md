# FloatChat Project Clone Prompt

**Create a comprehensive AI-powered ARGO float ocean data platform called "FloatChat" with the following specifications:**

## Project Overview
FloatChat is an intelligent ocean data analysis platform that provides AI-powered insights into ARGO float data. It features a modern web interface with real-time chat capabilities, interactive data visualizations, and advanced analytics for oceanographic research.

## Architecture & Technology Stack

### Backend Architecture
- **Framework**: FastAPI (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: RAG (Retrieval-Augmented Generation) system for intelligent responses
- **Data Processing**: Pandas, NumPy, SciPy for statistical analysis
- **APIs**: RESTful API with WebSocket support for real-time features
- **Deployment**: Uvicorn ASGI server

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Custom component library
- **Charts**: Recharts for data visualization
- **Maps**: Leaflet for geographic visualization
- **Animations**: Framer Motion for smooth interactions

### AI/ML Components
- **RAG System**: In-memory retrieval with ARGO-specific knowledge base
- **Natural Language Processing**: Enhanced intent parsing for oceanographic queries
- **Analytics Engine**: Statistical analysis and outlier detection
- **Contextual Suggestions**: Dynamic query suggestions based on user input

## File Structure

```
floatchat/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── models.py              # SQLAlchemy database models
│   │   ├── crud.py                # Database CRUD operations
│   │   ├── analytics.py           # Statistical analysis engine
│   │   ├── rag.py                 # RAG system implementation
│   │   ├── realtime.py            # WebSocket and real-time features
│   │   ├── startup.py             # Application startup logic
│   │   └── routers.py             # API route definitions
│   │   ├── routes_argo.py         # ARGO-specific routes
│   │   ├── routes_data.py         # Data management routes
│   │   └── cli_init_db.py         # Database initialization
│   ├── data/                      # Sample data and datasets
│   ├── requirements.txt           # Python dependencies
│   ├── requirements-local.txt     # Local development dependencies
│   └── Dockerfile                 # Container configuration
├── frontend/
│   └── web/
│       ├── src/
│       │   ├── components/        # React components
│       │   │   ├── ChatInterface.tsx    # AI chat interface
│       │   │   ├── DataVisualization.tsx # Data charts and tables
│       │   │   ├── MapVisualization.tsx # Interactive maps
│       │   │   ├── InsertData.tsx       # Data insertion tools
│       │   │   └── HelpModal.tsx        # User help system
│       │   ├── App.tsx            # Main application component
│       │   ├── main.tsx           # Application entry point
│       │   ├── index.css          # Global styles
│       │   └── vite.config.ts     # Vite configuration
│       ├── public/                # Static assets
│       ├── package.json           # Node.js dependencies
│       └── tsconfig.json          # TypeScript configuration
└── README.md                      # Project documentation
```

## Backend Implementation Details

### Database Models (models.py)
```python
# Profile model for ARGO float data
class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    float_id = Column(String, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    depth = Column(Float, index=True)
    temperature = Column(Float, index=True)
    salinity = Column(Float, index=True)
    month = Column(Integer, index=True)
    year = Column(Integer, index=True)
    date = Column(Date, nullable=True)
```

### API Endpoints (routers.py)

#### Chat Endpoints
- `POST /chat/` - Main AI chat endpoint with data insights
- `POST /chat/stream` - Streaming chat responses
- `GET /data/profiles` - Retrieve filtered profile data
- `GET /data/statistics` - Comprehensive statistics
- `GET /data/analytics/*` - Various analytical endpoints
- `GET /data/export/*` - Data export in multiple formats

#### Data Endpoints
- `POST /data/profile` - Create new profile
- `POST /data/profiles/bulk` - Bulk profile insertion
- `GET /data/nearest` - Find nearest profiles to coordinates

### RAG System (rag.py)
```python
# In-memory RAG with ARGO knowledge base
ARGO_KNOWLEDGE_BASE = [
    {
        "id": "argo_overview",
        "text": "ARGO floats are autonomous profiling floats...",
        "metadata": {"category": "overview", "priority": "high"}
    },
    # ... more knowledge entries
]

def retrieve(query: str, k: int = 5) -> List[Dict]:
    # Enhanced retrieval with ARGO-specific scoring
    
def summarize(query: str, contexts: List[Dict]) -> str:
    # Generate contextual responses
```

### Analytics Engine (analytics.py)
```python
class AnalyticsEngine:
    def get_basic_statistics(self) -> Dict[str, Any]
    def get_depth_distribution(self) -> List[Dict[str, Any]]
    def get_temperature_salinity_correlation(self) -> Dict[str, Any]
    def get_geographic_distribution(self, grid_size: float) -> List[Dict[str, Any]]
    def get_temporal_analysis(self) -> Dict[str, Any]
    # ... more analytical methods
```

## Frontend Implementation Details

### Chat Interface Component
```typescript
// Enhanced chat with ARGO-specific intelligence
interface ChatResponse {
  answer: string
  suggestions: string[]
  data_insights: {
    total_profiles?: number
    temperature?: {
      min: number, max: number, avg: number, median: number
    }
    salinity?: {
      min: number, max: number, avg: number, median: number
    }
    depth?: { min: number, max: number, avg: number }
    region?: string
  }
}
```

### Data Visualization Component
- Interactive charts using Recharts
- Real-time data updates
- Export functionality (PNG, CSV, JSON)
- Advanced filtering and search
- Responsive design with Tailwind CSS

### Map Visualization Component
- Leaflet-based interactive maps
- ARGO float location markers
- Geographic filtering capabilities
- Real-time data overlay

## Setup Instructions

### Backend Setup
1. Create virtual environment: `python -m venv .venv`
2. Activate environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Set up PostgreSQL database
5. Initialize database: `python -c "from app.cli_init_db import init_db; init_db()"`
6. Start server: `python -m app.main` or `uvicorn app.main:app --reload`

### Frontend Setup
1. Navigate to frontend directory: `cd frontend/web`
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`
4. Build for production: `npm run build`

### Environment Variables
```bash
# Backend
export ENV=dev
export DATABASE_URL=postgresql://user:password@localhost/floatchat
export ALLOWED_ORIGINS=http://localhost:5173

# Frontend
VITE_API_URL=http://localhost:8000
```

## Key Features Implementation

### 1. AI Chat Interface
- Natural language processing for oceanographic queries
- Intent parsing for location, depth, temperature, salinity filters
- RAG system with ARGO-specific knowledge base
- Real-time streaming responses
- Contextual follow-up suggestions

### 2. Data Visualization
- Interactive charts (bar, line, scatter plots)
- Real-time data updates
- Export functionality (CSV, JSON, NetCDF)
- Advanced filtering and search
- Responsive design

### 3. Analytics Engine
- Statistical analysis and outlier detection
- Geographic distribution analysis
- Temporal pattern analysis
- Correlation studies
- Advanced analytical queries

### 4. Real-time Features
- WebSocket connections for live updates
- Real-time data streaming
- Live analytics updates
- Notification system

## Dependencies

### Backend Requirements
```
fastapi==0.114.2
uvicorn[standard]==0.30.6
pydantic==2.9.2
SQLAlchemy==2.0.35
asyncpg==0.29.0
psycopg2-binary==2.9.9
pandas==2.2.3
numpy==1.26.4
scipy==1.14.1
python-multipart==0.0.9
websockets==12.0
sentence-transformers==3.1.1
chromadb==0.5.11
faiss-cpu==1.8.0.post1
python-dotenv==1.0.1
```

### Frontend Requirements
```
react==18.x
typescript==5.x
vite==5.x
tailwindcss==3.x
recharts==2.x
leaflet==1.x
framer-motion==11.x
lucide-react==0.x
```

## Database Schema

```sql
-- ARGO float profiles table
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    float_id VARCHAR(50),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    depth DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    salinity DOUBLE PRECISION,
    month INTEGER,
    year INTEGER,
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_latitude (latitude),
    INDEX idx_longitude (longitude),
    INDEX idx_depth (depth),
    INDEX idx_temperature (temperature),
    INDEX idx_salinity (salinity),
    INDEX idx_float_id (float_id)
);
```

## Testing & Validation

### Sample Test Queries
1. "Show me temperature patterns near the equator"
2. "What's the salinity distribution in the Pacific?"
3. "Analyze temperature data for May 2025"
4. "Compare temperature vs salinity correlation"
5. "Find deep ocean profiles below 1000m"

### Expected Responses
- Detailed statistical analysis
- Data insights with min/max/avg values
- Geographic context and regional information
- Follow-up query suggestions
- Visual data representations

## Deployment Considerations

### Production Deployment
1. Use Gunicorn with Uvicorn workers
2. Nginx reverse proxy
3. PostgreSQL database
4. Redis for caching
5. Docker containerization
6. Environment variable management

### Performance Optimization
1. Database query optimization with indexes
2. Caching strategies for frequently accessed data
3. Lazy loading for large datasets
4. CDN for static assets
5. Database connection pooling

## Documentation Requirements

1. API documentation with OpenAPI/Swagger
2. User guide and tutorial
3. Developer setup instructions
4. Deployment guide
5. Architecture diagrams
6. Database schema documentation

---

**This prompt contains all the technical specifications needed to recreate the complete FloatChat project. Use this to build the full-stack AI-powered ocean data analysis platform with chat interface, data visualization, and real-time analytics capabilities.**
