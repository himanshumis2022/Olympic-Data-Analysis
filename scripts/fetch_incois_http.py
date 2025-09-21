import requests
from retrying import retry
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv('INCOIS_BASE', 'https://incois.gov.in/OON')
OUT_DIR = Path(__file__).resolve().parents[1] / 'data' / 'raw'
OUT_DIR.mkdir(parents=True, exist_ok=True)

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch(url: str) -> bytes:
	resp = requests.get(url, timeout=30)
	resp.raise_for_status()
	return resp.content

if __name__ == '__main__':
	print('INCOIS base:', BASE)
	# Stub: Add real endpoints when available
