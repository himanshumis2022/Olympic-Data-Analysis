import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Use same path logic as backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # floatchat/scripts -> floatchat
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
DB_DIR = os.path.join(BACKEND_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, "floatchat.db")
DATABASE_URL = f"sqlite:///{db_path}"

def main():
	engine = create_engine(DATABASE_URL)
	root = Path(__file__).resolve().parents[1] / 'data' / 'processed'
	parquet = root / 'synthetic_profiles.parquet'
	csv = root / 'synthetic_profiles.csv'
	if parquet.exists():
		df = pd.read_parquet(parquet)
		print(f"Loading parquet: {parquet}")
	elif csv.exists():
		df = pd.read_csv(csv)
		print(f"Loading csv: {csv}")
	else:
		raise SystemExit("No processed data file found.")
	df.to_sql('profiles', engine, if_exists='append', index=False)
	print("Loaded", len(df), "rows into profiles")

if __name__ == '__main__':
	main()
