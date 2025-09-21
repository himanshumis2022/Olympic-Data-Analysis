#!/usr/bin/env python3
"""
Generate 500 realistic ARGO-like ocean profiles and insert into the backend database.
This uses the SQLAlchemy models defined in backend/app/models.py so the data
is consistent with the running FastAPI backend.
"""
from __future__ import annotations

import os
import sys
import random
from datetime import datetime
from pathlib import Path
from typing import Tuple

# Ensure we can import from backend/app
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
APP_DIR = BACKEND_DIR / "app"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Load .env so DATABASE_URL is honored by backend.app.db
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(PROJECT_ROOT / ".env")
except Exception:
    pass

# Import DB and models from the backend
from app.db import SessionLocal, Base, engine  # type: ignore
from app.models import Profile  # type: ignore

random.seed(42)

# Define realistic ocean regions with base temp/sal ranges
REGIONS = [
    {
        "name": "Gulf Stream",
        "lat_range": (20.0, 45.0),
        "lon_range": (-80.0, -30.0),
        "temp_surface": (18.0, 28.0),  # warm surface
        "salinity_surface": (35.0, 37.0),
    },
    {
        "name": "Arctic Ocean",
        "lat_range": (66.0, 80.0),
        "lon_range": (-160.0, 60.0),
        "temp_surface": (-2.0, 5.0),  # very cold
        "salinity_surface": (30.0, 34.0),
    },
    {
        "name": "Tropical Pacific",
        "lat_range": (-10.0, 10.0),
        "lon_range": (140.0, -80.0),  # note: wrap-around handled later
        "temp_surface": (24.0, 30.0),
        "salinity_surface": (33.5, 35.5),
    },
    {
        "name": "Southern Ocean",
        "lat_range": (-60.0, -30.0),
        "lon_range": (-180.0, 180.0),
        "temp_surface": (-1.5, 6.0),
        "salinity_surface": (33.0, 34.8),
    },
    {
        "name": "Mediterranean",
        "lat_range": (30.0, 46.0),
        "lon_range": (-6.0, 36.0),
        "temp_surface": (14.0, 28.0),
        "salinity_surface": (36.0, 39.0),  # high salinity
    },
    {
        "name": "Indian Ocean",
        "lat_range": (-30.0, 20.0),
        "lon_range": (20.0, 120.0),
        "temp_surface": (20.0, 29.0),
        "salinity_surface": (34.0, 36.0),
    },
]

# Typical depths sampled (m)
DEPTH_OPTIONS = [5, 10, 20, 50, 100, 200, 300, 500, 800, 1000]

# Helper to pick lon respecting wrap-around ranges
def rand_lon(lon_range: Tuple[float, float]) -> float:
    lo, hi = lon_range
    if lo <= hi:
        return random.uniform(lo, hi)
    # wrap-around (e.g., 140 to -80 -> 140..180 plus -180..-80)
    if random.random() < (180 - lo) / ((180 - lo) + (hi + 180)):
        return random.uniform(lo, 180)
    return random.uniform(-180, hi)


def depth_adjusted_temp_sal(depth: float, temp_surface: Tuple[float, float], sal_surface: Tuple[float, float]) -> Tuple[float, float]:
    # Temperature decreases with depth; simple lapse (rough heuristic)
    surface_temp = random.uniform(*temp_surface)
    # cool by up to ~20C by 1000m, non-linear-ish
    depth_cooling = min(20.0, (depth / 1000.0) ** 0.7 * 20.0)
    temp = max(-2.0, surface_temp - depth_cooling + random.uniform(-0.5, 0.5))

    # Salinity: slight trend with depth (region-dependent noise)
    surface_sal = random.uniform(*sal_surface)
    sal = min(40.0, max(30.0, surface_sal + (depth / 1000.0) * random.uniform(-0.5, 0.7) + random.uniform(-0.2, 0.2)))
    return temp, sal


def make_float_id(region_idx: int) -> str:
    # synthetic float ids in a region-coded range
    base = 5906000 + region_idx * 50
    return str(base + random.randint(0, 49))


def generate_profiles(n: int = 500):
    profiles = []
    current_years = [2024, 2025]

    for _ in range(n):
        region_idx = random.randrange(len(REGIONS))
        region = REGIONS[region_idx]
        lat = random.uniform(*region["lat_range"])
        lon = rand_lon(region["lon_range"])
        depth = random.choice(DEPTH_OPTIONS)

        temp, sal = depth_adjusted_temp_sal(depth, region["temp_surface"], region["salinity_surface"])

        # Random date across months; align month/year fields
        year = random.choice(current_years)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = datetime(year, month, day).date()

        profiles.append(
            Profile(
                float_id=make_float_id(region_idx),
                latitude=round(lat, 4),
                longitude=round(lon, 4),
                depth=float(depth),
                temperature=round(temp, 2),
                salinity=round(sal, 2),
                month=month,
                year=year,
                date=date,
            )
        )
    return profiles


def main():
    # Ensure tables exist (idempotent)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # Current count
        current = session.query(Profile).count()
        target = 500
        to_insert = max(0, target - current)

        if to_insert > 0:
            new_profiles = generate_profiles(to_insert)
            session.bulk_save_objects(new_profiles)
            session.commit()
            print(f"Inserted {len(new_profiles)} profiles. Total is now {current + len(new_profiles)} (target {target}).")
        else:
            print(f"Database already has {current} profiles (>= {target}). No insert needed.")
    except Exception as e:
        session.rollback()
        print("Error inserting profiles:", e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
