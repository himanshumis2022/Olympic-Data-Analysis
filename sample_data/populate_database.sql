-- Sample ARGO Float Data for FloatChat Platform
-- This script populates the database with realistic test data

-- Create table if it doesn't exist (adjust based on your schema)
CREATE TABLE IF NOT EXISTS profiles (
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

-- Clear existing data (optional)
-- TRUNCATE TABLE profiles RESTART IDENTITY;

-- Insert sample data
INSERT INTO profiles (float_id, latitude, longitude, depth, temperature, salinity, month, year, date) VALUES
-- Gulf Stream / North Atlantic
('5906468', 25.7617, -80.1918, 10, 26.5, 36.2, 6, 2024, '2024-06-15'),
('5906468', 25.7520, -80.1850, 50, 24.8, 36.4, 6, 2024, '2024-06-15'),
('5906468', 25.7423, -80.1782, 100, 22.1, 36.6, 6, 2024, '2024-06-15'),

-- Equatorial Atlantic
('5906469', 0.0, -30.0, 15, 28.2, 35.8, 5, 2024, '2024-05-20'),
('5906469', 0.1, -29.9, 75, 25.6, 36.0, 5, 2024, '2024-05-20'),

-- Indian Ocean
('5906470', -10.5, 45.2, 25, 24.3, 35.1, 7, 2024, '2024-07-10'),
('5906470', -10.4, 45.3, 150, 18.7, 35.5, 7, 2024, '2024-07-10'),

-- North Atlantic
('5906471', 35.6, -75.4, 30, 23.8, 36.8, 8, 2024, '2024-08-05'),
('5906471', 35.7, -75.3, 200, 15.2, 35.9, 8, 2024, '2024-08-05'),

-- South Atlantic
('5906472', -25.8, 28.1, 40, 21.5, 35.3, 9, 2024, '2024-09-12'),
('5906472', -25.9, 28.0, 300, 12.8, 34.8, 9, 2024, '2024-09-12'),

-- North Atlantic (Cold water)
('5906473', 60.2, -20.5, 20, 8.4, 34.2, 4, 2024, '2024-04-18'),
('5906473', 60.1, -20.6, 500, 4.1, 34.9, 4, 2024, '2024-04-18'),

-- Southern Ocean
('5906474', -45.3, 170.8, 35, 16.7, 34.6, 10, 2024, '2024-10-03'),
('5906474', -45.2, 170.9, 800, 2.8, 34.7, 10, 2024, '2024-10-03'),

-- Western Pacific (Tropical)
('5906475', 15.2, 120.5, 12, 29.1, 34.1, 11, 2024, '2024-11-08'),
('5906475', 15.3, 120.4, 1000, 3.2, 34.6, 11, 2024, '2024-11-08'),

-- Eastern Pacific
('5906476', -5.1, -85.3, 18, 27.8, 35.0, 12, 2024, '2024-12-01'),
('5906476', -5.0, -85.2, 250, 14.6, 35.2, 12, 2024, '2024-12-01'),

-- North Atlantic (Winter)
('5906477', 42.8, -70.1, 45, 19.3, 35.8, 1, 2025, '2025-01-15'),
('5906477', 42.9, -70.0, 600, 6.7, 35.1, 1, 2025, '2025-01-15'),

-- Western Indian Ocean
('5906478', -15.6, 55.8, 22, 26.4, 35.4, 2, 2025, '2025-02-10'),
('5906478', -15.5, 55.9, 400, 11.2, 35.0, 2, 2025, '2025-02-10'),

-- Eastern Atlantic
('5906479', 8.3, -15.7, 28, 25.9, 36.1, 3, 2025, '2025-03-05'),
('5906479', 8.4, -15.6, 750, 5.8, 34.9, 3, 2025, '2025-03-05'),

-- Additional profiles for better coverage
-- Mediterranean Sea
('5906480', 36.5, 14.2, 15, 22.8, 38.5, 6, 2024, '2024-06-20'),
('5906480', 36.4, 14.3, 200, 16.2, 38.8, 6, 2024, '2024-06-20'),

-- Arctic Ocean
('5906481', 75.2, -15.8, 25, 1.2, 32.1, 8, 2024, '2024-08-15'),
('5906481', 75.1, -15.9, 300, -0.8, 34.2, 8, 2024, '2024-08-15'),

-- Central Pacific
('5906482', 20.5, -155.0, 35, 25.4, 35.2, 9, 2024, '2024-09-25'),
('5906482', 20.4, -155.1, 500, 8.9, 34.8, 9, 2024, '2024-09-25'),

-- South Pacific
('5906483', -30.2, -120.5, 40, 18.7, 34.9, 11, 2024, '2024-11-18'),
('5906483', -30.1, -120.4, 800, 4.5, 34.6, 11, 2024, '2024-11-18'),

-- Benguela Current
('5906484', -25.8, 12.5, 20, 19.5, 35.1, 1, 2025, '2025-01-28'),
('5906484', -25.7, 12.6, 400, 12.3, 34.8, 1, 2025, '2025-01-28');

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_profiles_location ON profiles(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_profiles_depth ON profiles(depth);
CREATE INDEX IF NOT EXISTS idx_profiles_temperature ON profiles(temperature);
CREATE INDEX IF NOT EXISTS idx_profiles_salinity ON profiles(salinity);
CREATE INDEX IF NOT EXISTS idx_profiles_date ON profiles(date);
CREATE INDEX IF NOT EXISTS idx_profiles_float_id ON profiles(float_id);

-- Create a view for easy querying
CREATE OR REPLACE VIEW profile_summary AS
SELECT 
    COUNT(*) as total_profiles,
    COUNT(DISTINCT float_id) as unique_floats,
    MIN(date) as earliest_date,
    MAX(date) as latest_date,
    MIN(depth) as min_depth,
    MAX(depth) as max_depth,
    ROUND(MIN(temperature)::numeric, 2) as min_temperature,
    ROUND(MAX(temperature)::numeric, 2) as max_temperature,
    ROUND(MIN(salinity)::numeric, 2) as min_salinity,
    ROUND(MAX(salinity)::numeric, 2) as max_salinity,
    ROUND(MIN(latitude)::numeric, 4) as min_latitude,
    ROUND(MAX(latitude)::numeric, 4) as max_latitude,
    ROUND(MIN(longitude)::numeric, 4) as min_longitude,
    ROUND(MAX(longitude)::numeric, 4) as max_longitude
FROM profiles;

-- Query to verify data
SELECT * FROM profile_summary;
