import os
import requests
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Use same path logic as backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # floatchat/scripts -> floatchat
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
DB_DIR = os.path.join(BACKEND_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)
db_path = os.path.join(DB_DIR, "floatchat.db")
DATABASE_URL = f"sqlite:///{db_path}"
API = os.getenv("API") or "http://localhost:8000"

def main():
	engine = create_engine(DATABASE_URL)
	with engine.begin() as conn:
		rows = conn.execute(text("SELECT id, lat as latitude, lon as longitude, depth, temperature, salinity FROM profiles LIMIT 5000")).mappings().all()
	docs = []
	for r in rows:
		text_content = f"Profile {r['id']} at ({r['latitude']:.3f},{r['longitude']:.3f}) depth {r['depth']}m T={r['temperature']:.2f} S={r['salinity']:.2f}"
		docs.append({"id": r['id'], "text": text_content, "metadata": {"lat": r['latitude'], "lon": r['longitude'], "depth": r['depth']}})
	# send to backend to hold in-memory
	r = requests.post(f"{API}/admin/index", json={"docs": docs}, timeout=60)
	r.raise_for_status()
	print(f"Indexed {len(docs)} documents in backend memory")

if __name__ == '__main__':
	main()
