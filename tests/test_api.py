import os
import pytest

import requests

API = os.getenv('API', 'http://localhost:8000')

def test_health():
	r = requests.get(f'{API}/health', timeout=10)
	assert r.status_code == 200
	assert r.json()['status'] == 'ok'


def test_chat():
	r = requests.post(f'{API}/chat', json={'message': 'nearest floats'}, timeout=15)
	assert r.status_code == 200
	assert 'Query:' in r.json()['answer']

def test_export_netcdf(client):
    response = client.get("/export/netcdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-netcdf"
