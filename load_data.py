#!/usr/bin/env python3
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
