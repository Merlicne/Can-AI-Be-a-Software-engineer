import pytest
from flask import Flask
from flask.testing import FlaskClient

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

from main import app, db_manager, db_proxy  # Assuming the previous code is in `api_code.py`

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db_manager.create_table()
        yield client

def test_create_record(client: FlaskClient):
    response = client.post('/create', json={'data': 'Test Data'})
    assert response.status_code == 201
    assert b'Record added' in response.data

    records = db_proxy.fetch_records()
    assert len(records) == 1
    assert records[0][1] == 'Test Data'

def test_read_empty_db(client: FlaskClient):
    response = client.get('/read')
    assert response.status_code == 200
    assert response.json == []

def test_read_records(client: FlaskClient):
    client.post('/create', json={'data': 'Test Data 1'})
    client.post('/create', json={'data': 'Test Data 2'})
    
    response = client.get('/read')
    assert response.status_code == 200
    records = response.json
    assert len(records) == 2
    assert records[0][1] == 'Test Data 1'
    assert records[1][1] == 'Test Data 2'

def test_update_record(client: FlaskClient):
    client.post('/create', json={'data': 'Test Data'})
    response = client.put('/update/1', json={'data': 'Updated Data'})
    assert response.status_code == 200
    assert b'Record updated' in response.data

    records = db_proxy.fetch_records()
    assert records[0][1] == 'Updated Data'

def test_delete_record(client: FlaskClient):
    client.post('/create', json={'data': 'Test Data'})
    response = client.delete('/delete/1')
    assert response.status_code == 200
    assert b'Record deleted' in response.data

    records = db_proxy.fetch_records()
    assert len(records) == 0

def test_proxy_cache(client: FlaskClient):
    client.post('/create', json={'data': 'Test Data 1'})
    client.post('/create', json={'data': 'Test Data 2'})

    # Fetching records first time (should be uncached)
    records_uncached = db_proxy.fetch_records()
    assert len(records_uncached) == 2

    # Simulate fetching from cache
    records_cached = db_proxy.fetch_records()
    assert records_cached == records_uncached

def test_proxy_logging(client: FlaskClient, caplog):
    client.post('/create', json={'data': 'Test Data'})
    
    with caplog.at_level('INFO'):
        db_proxy.fetch_records()
        db_proxy.update_record(1, 'New Data')
        db_proxy.delete_record(1)

    assert "DatabaseProxy: Fetching records" in caplog.text
    assert "DatabaseProxy: Updating record with ID 1: New Data" in caplog.text
    assert "DatabaseProxy: Deleting record with ID 1" in caplog.text
