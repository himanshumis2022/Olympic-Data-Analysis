import ftputil
from retrying import retry
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

FTP_HOST = os.getenv('IFREMER_FTP', 'ftp.ifremer.fr')
FTP_BASE = os.getenv('IFREMER_FTP_BASE', '/ifremer/argo')
OUT_DIR = Path(__file__).resolve().parents[1] / 'data' / 'raw'
OUT_DIR.mkdir(parents=True, exist_ok=True)

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_listing(subpath: str = ''):
	with ftputil.FTPHost(FTP_HOST, 'anonymous', 'anonymous@') as host:
		host.use_list_a_option = True
		base = FTP_BASE + ('/' + subpath if subpath else '')
		files = host.listdir(base)
		return base, files

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_file(remote_path: str, local_path: Path):
	with ftputil.FTPHost(FTP_HOST, 'anonymous', 'anonymous@') as host:
		host.use_list_a_option = True
		if local_path.exists():
			return
		local_path.parent.mkdir(parents=True, exist_ok=True)
		host.download(remote_path, str(local_path))

if __name__ == '__main__':
	base, files = fetch_listing('dac')
	print('Found entries:', len(files))
	# This is a stub: download a small subset when discovered
