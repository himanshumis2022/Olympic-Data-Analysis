#!/usr/bin/env python3
"""
Generate sample ARGO float data for FloatChat platform testing
"""

import json
import csv
import random
import datetime
from typing import List, Dict, Any

def generate_realistic_argo_data(num_profiles: int = 100) -> List[Dict[str, Any]]:
    """Generate realistic ARGO float profile data"""
    
    profiles = []
    float_ids = [f"590{6470 + i}" for i in range(20)]  # 20 different floats
    
    # Define ocean regions with realistic temperature/salinity ranges
    ocean_regions = [
        # Tropical Atlantic
        {"lat_range": (-10, 30), "lon_range": (-60, -10), "temp_range": (24, 29), "sal_range": (35.5, 37.0)},
        # North Atlantic
        {"lat_range": (30, 65), "lon_range": (-70, -10), "temp_range": (8, 22), "sal_range": (34.5, 36.5)},
        # Equatorial Pacific
        {"lat_range": (-10, 10), "lon_range": (-180, -80), "temp_range": (26, 30), "sal_range": (34.0, 35.5)},
        # North Pacific
        {"lat_range": (20, 60), "lon_range": (120, -120), "temp_range": (10, 25), "sal_range": (33.5, 35.0)},
        # Southern Ocean
        {"lat_range": (-60, -30), "lon_range": (-180, 180), "temp_range": (0, 15), "sal_range": (33.8, 34.8)},
        # Indian Ocean
        {"lat_range": (-30, 20), "lon_range": (40, 120), "temp_range": (20, 28), "sal_range": (34.5, 36.0)},
        # Mediterranean
        {"lat_range": (30, 45), "lon_range": (0, 40), "temp_range": (15, 26), "sal_range": (37.0, 39.0)},
        # Arctic
        {"lat_range": (65, 80), "lon_range": (-180, 180), "temp_range": (-2, 8), "sal_range": (30.0, 34.5)}
    ]
    
    # Depth-temperature relationship (thermocline)
    def get_temperature_at_depth(surface_temp: float, depth: float) -> float:
        """Calculate temperature at depth using thermocline model"""
        if depth <= 50:
            return surface_temp - (depth * 0.02)  # Mixed layer
        elif depth <= 200:
            return surface_temp - 1 - ((depth - 50) * 0.08)  # Thermocline
        elif depth <= 1000:
            return surface_temp - 13 - ((depth - 200) * 0.01)  # Deep water
        else:
            return max(2.0, surface_temp - 21 - ((depth - 1000) * 0.002))  # Abyssal
    
    # Generate profiles
    for i in range(num_profiles):
        # Select random region
        region = random.choice(ocean_regions)
        
        # Generate location within region
        lat = random.uniform(region["lat_range"][0], region["lat_range"][1])
        lon = random.uniform(region["lon_range"][0], region["lon_range"][1])
        
        # Handle longitude wrapping
        if lon > 180:
            lon -= 360
        elif lon < -180:
            lon += 360
        
        # Generate date (last 12 months)
        start_date = datetime.date(2024, 1, 1)
        end_date = datetime.date(2025, 3, 31)
        random_date = start_date + datetime.timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        # Generate depth (weighted towards shallower depths)
        depth_weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Shallow to deep
        depth_ranges = [(10, 50), (51, 150), (151, 500), (501, 1500), (1501, 2000)]
        depth_range = random.choices(depth_ranges, weights=depth_weights)[0]
        depth = random.randint(depth_range[0], depth_range[1])
        
        # Generate surface temperature based on region and season
        base_temp = random.uniform(region["temp_range"][0], region["temp_range"][1])
        
        # Seasonal variation (Northern hemisphere bias)
        month = random_date.month
        if lat > 0:  # Northern hemisphere
            seasonal_factor = 0.8 * math.cos((month - 7) * math.pi / 6)  # Peak in July
        else:  # Southern hemisphere
            seasonal_factor = 0.8 * math.cos((month - 1) * math.pi / 6)  # Peak in January
        
        surface_temp = base_temp + seasonal_factor
        
        # Calculate temperature at depth
        temperature = get_temperature_at_depth(surface_temp, depth)
        temperature = round(max(-2.0, min(35.0, temperature)), 2)
        
        # Generate salinity (slightly depth dependent)
        base_salinity = random.uniform(region["sal_range"][0], region["sal_range"][1])
        depth_salinity_factor = 0.001 * depth  # Slight increase with depth
        salinity = round(base_salinity + depth_salinity_factor, 2)
        salinity = max(30.0, min(40.0, salinity))
        
        # Select float ID
        float_id = random.choice(float_ids)
        
        profile = {
            "id": i + 1,
            "float_id": float_id,
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "depth": depth,
            "temperature": temperature,
            "salinity": salinity,
            "month": random_date.month,
            "year": random_date.year,
            "date": random_date.strftime("%Y-%m-%d")
        }
        
        profiles.append(profile)
    
    return profiles

def save_data(profiles: List[Dict[str, Any]], base_filename: str):
    """Save data in multiple formats"""
    
    # Calculate metadata
    metadata = {
        "total_profiles": len(profiles),
        "date_range": {
            "start": min(p["date"] for p in profiles),
            "end": max(p["date"] for p in profiles)
        },
        "depth_range": {
            "min": min(p["depth"] for p in profiles),
            "max": max(p["depth"] for p in profiles)
        },
        "temperature_range": {
            "min": min(p["temperature"] for p in profiles),
            "max": max(p["temperature"] for p in profiles)
        },
        "salinity_range": {
            "min": min(p["salinity"] for p in profiles),
            "max": max(p["salinity"] for p in profiles)
        },
        "geographic_coverage": {
            "latitude_range": {
                "min": min(p["latitude"] for p in profiles),
                "max": max(p["latitude"] for p in profiles)
            },
            "longitude_range": {
                "min": min(p["longitude"] for p in profiles),
                "max": max(p["longitude"] for p in profiles)
            }
        },
        "float_ids": sorted(list(set(p["float_id"] for p in profiles)))
    }
    
    # Save JSON
    json_data = {
        "profiles": profiles,
        "metadata": metadata
    }
    
    with open(f"{base_filename}.json", "w") as f:
        json.dump(json_data, f, indent=2)
    
    # Save CSV
    with open(f"{base_filename}.csv", "w", newline="") as f:
        if profiles:
            writer = csv.DictWriter(f, fieldnames=profiles[0].keys())
            writer.writeheader()
            writer.writerows(profiles)
    
    print(f"Generated {len(profiles)} profiles")
    print(f"Saved to {base_filename}.json and {base_filename}.csv")
    print(f"Date range: {metadata['date_range']['start']} to {metadata['date_range']['end']}")
    print(f"Depth range: {metadata['depth_range']['min']}m to {metadata['depth_range']['max']}m")
    print(f"Temperature range: {metadata['temperature_range']['min']}°C to {metadata['temperature_range']['max']}°C")
    print(f"Salinity range: {metadata['salinity_range']['min']} to {metadata['salinity_range']['max']} PSU")

if __name__ == "__main__":
    import math
    
    # Generate different sized datasets
    datasets = [
        (100, "argo_sample_100"),
        (500, "argo_sample_500"),
        (1000, "argo_sample_1000")
    ]
    
    for num_profiles, filename in datasets:
        print(f"\nGenerating {num_profiles} profiles...")
        profiles = generate_realistic_argo_data(num_profiles)
        save_data(profiles, filename)
