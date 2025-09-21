# FloatChat Sample Data

This directory contains sample ARGO float data for testing and development of the FloatChat platform.

## 📁 Files Overview

### Core Sample Data
- **`argo_sample_data.json`** - 25 sample profiles in JSON format
- **`argo_profiles.csv`** - Same 25 profiles in CSV format
- **`populate_database.sql`** - SQL script to populate PostgreSQL database

### Data Generation Tools
- **`generate_sample_data.py`** - Python script to generate larger realistic datasets
- **`README.md`** - This documentation file

## 🌊 Sample Data Characteristics

### Geographic Coverage
- **Global Distribution**: Profiles from all major ocean basins
- **Latitude Range**: -45.3° to 60.2° (Arctic to Southern Ocean)
- **Longitude Range**: -85.3° to 170.9° (Global coverage)

### Oceanographic Parameters
- **Depth Range**: 10m to 1000m
- **Temperature Range**: 2.8°C to 29.1°C (realistic ocean temperatures)
- **Salinity Range**: 34.1 to 36.8 PSU (practical salinity units)
- **Time Period**: April 2024 to March 2025

### Float Information
- **12 Different Floats**: IDs from 5906468 to 5906479
- **25 Total Profiles**: Multiple depth measurements per float
- **Realistic Trajectories**: Floats show movement over time

## 🚀 Quick Start

### 1. Using JSON Data (Frontend Testing)
```javascript
// Load sample data in your React components
import sampleData from './sample_data/argo_sample_data.json';
const profiles = sampleData.profiles;
```

### 2. Using CSV Data (Data Analysis)
```python
import pandas as pd
df = pd.read_csv('argo_profiles.csv')
print(df.head())
```

### 3. Database Population (Backend Setup)
```bash
# PostgreSQL
psql -d floatchat -f populate_database.sql

# Or using Python/SQLAlchemy
python -c "
import pandas as pd
from sqlalchemy import create_engine
df = pd.read_csv('argo_profiles.csv')
engine = create_engine('postgresql://user:pass@localhost/floatchat')
df.to_sql('profiles', engine, if_exists='append', index=False)
"
```

## 🔧 Generating More Data

### Using the Python Generator
```bash
cd sample_data
python generate_sample_data.py
```

This will generate three datasets:
- **100 profiles** (`argo_sample_100.json/csv`)
- **500 profiles** (`argo_sample_500.json/csv`)
- **1000 profiles** (`argo_sample_1000.json/csv`)

### Customizing Data Generation
```python
from generate_sample_data import generate_realistic_argo_data, save_data

# Generate custom dataset
profiles = generate_realistic_argo_data(num_profiles=2000)
save_data(profiles, "custom_dataset")
```

## 🗺️ Ocean Regions Covered

### Atlantic Ocean
- **Gulf Stream**: Warm, high-salinity water (Florida Current)
- **North Atlantic**: Cooler temperatures, moderate salinity
- **Equatorial Atlantic**: Warm tropical waters
- **South Atlantic**: Temperate to cool waters

### Pacific Ocean
- **Tropical Pacific**: Warm, low-salinity waters
- **North Pacific**: Temperate waters with seasonal variation
- **Eastern Pacific**: Upwelling regions with cooler water

### Indian Ocean
- **Western Indian**: Warm tropical waters
- **Southern Indian**: Cooler waters near Antarctica

### Other Regions
- **Mediterranean Sea**: High salinity, warm waters
- **Arctic Ocean**: Cold, low-salinity waters
- **Southern Ocean**: Cold Antarctic waters

## 📊 Data Quality Features

### Realistic Oceanography
- **Thermocline Structure**: Temperature decreases with depth
- **Halocline Effects**: Salinity variations with depth
- **Seasonal Patterns**: Temperature varies by season and hemisphere
- **Regional Characteristics**: Each ocean basin has realistic properties

### ARGO Float Behavior
- **Drift Patterns**: Floats show realistic movement
- **Profile Cycles**: Multiple measurements per float
- **Temporal Spacing**: Realistic time intervals between profiles

## 🔍 Testing Scenarios

### Map Visualization Testing
```javascript
// Test different regions
const equatorialProfiles = profiles.filter(p => 
  Math.abs(p.latitude) < 10
);

const deepProfiles = profiles.filter(p => p.depth > 500);
```

### AI Chat Testing
Try these queries with the sample data:
- "Show me temperature patterns near the equator"
- "What's the salinity distribution in May 2024?"
- "Find profiles deeper than 500 meters"
- "Analyze temperature vs depth relationships"

### Analytics Testing
```python
# Temperature-Salinity analysis
import matplotlib.pyplot as plt
plt.scatter(df['salinity'], df['temperature'], c=df['depth'])
plt.xlabel('Salinity (PSU)')
plt.ylabel('Temperature (°C)')
plt.colorbar(label='Depth (m)')
```

## 🛠️ Database Schema

The sample data assumes this table structure:
```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    float_id VARCHAR(20) NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    depth INTEGER NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    salinity DECIMAL(5, 2) NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📈 Performance Considerations

### Indexing
The SQL script creates indexes on:
- Location (latitude, longitude)
- Depth, temperature, salinity
- Date and float_id

### Data Size Guidelines
- **Development**: 25-100 profiles
- **Testing**: 500-1000 profiles  
- **Demo**: 1000+ profiles
- **Production**: Use real ARGO data

## 🌐 Real ARGO Data Sources

For production use, consider these real data sources:
- **ARGO Global Data Assembly Centre**: https://www.argodatamgt.org/
- **NOAA ARGO Data**: https://www.aoml.noaa.gov/argo/
- **Copernicus Marine Service**: https://marine.copernicus.eu/

## 🤝 Contributing

To add more sample data:
1. Follow the existing data format
2. Ensure realistic oceanographic values
3. Include geographic diversity
4. Update this README with new features

## 📝 Data Format Reference

### JSON Structure
```json
{
  "profiles": [
    {
      "id": 1,
      "float_id": "5906468",
      "latitude": 25.7617,
      "longitude": -80.1918,
      "depth": 10,
      "temperature": 26.5,
      "salinity": 36.2,
      "month": 6,
      "year": 2024,
      "date": "2024-06-15"
    }
  ],
  "metadata": {
    "total_profiles": 25,
    "date_range": {...},
    "depth_range": {...}
  }
}
```

### CSV Columns
- `id`: Unique profile identifier
- `float_id`: ARGO float identifier
- `latitude`: Decimal degrees (-90 to 90)
- `longitude`: Decimal degrees (-180 to 180)
- `depth`: Depth in meters
- `temperature`: Temperature in Celsius
- `salinity`: Salinity in PSU
- `month`: Month (1-12)
- `year`: Year
- `date`: ISO date format (YYYY-MM-DD)

---

**Happy Testing! 🌊🤖📊**
