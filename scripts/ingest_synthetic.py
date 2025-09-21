import os
import pandas as pd
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parents[1] / 'data' / 'processed'
RAW_DIR = Path(__file__).resolve().parents[1] / 'data' / 'raw'

OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

rows = []
for i in range(1000):
	lat = np.random.uniform(-60, 60)
	lon = np.random.uniform(-180, 180)
	depth = np.random.choice([5, 10, 20, 50, 100, 200, 500])
	temp = np.random.normal(15 - depth*0.02, 2)
	sal = np.random.normal(34.5 + depth*0.001, 0.2)
	month = np.random.randint(1,13)
	year = 2023
	rows.append((i, lat, lon, depth, temp, sal, month, year))

df = pd.DataFrame(rows, columns=['id','lat','lon','depth','temperature','salinity','month','year'])

csv_path = OUT_DIR / 'synthetic_profiles.csv'
df.to_csv(csv_path, index=False)
print(f"Wrote {csv_path}")

try:
	parquet_path = OUT_DIR / 'synthetic_profiles.parquet'
	df.to_parquet(parquet_path, index=False)
	print(f"Wrote {parquet_path}")
except Exception as e:
	print("Skipping parquet (pyarrow not available):", e)
