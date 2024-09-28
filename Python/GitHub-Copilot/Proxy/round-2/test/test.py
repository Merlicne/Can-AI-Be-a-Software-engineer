# test_app.py
import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))
from main import app, db_proxy

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_record(client):
    response = client.post('/create', json={'data': 'Test Data'})
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'id' in json_data

def test_read_records_empty(client):
    response = client.get('/read')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == []

def test_read_records(client):
    client.post('/create', json={'data': 'Test Data 1'})
    client.post('/create', json={'data': 'Test Data 2'})
    response = client.get('/read')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2

def test_update_record(client):
    response = client.post('/create', json={'data': 'Test Data'})
    record_id = response.get_json()['id']
    response = client.put('/update', json={'id': record_id, 'data': 'Updated Data'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['rows_updated'] == 1

def test_delete_record(client):
    response = client.post('/create', json={'data': 'Test Data'})
    record_id = response.get_json()['id']
    response = client.delete('/delete', json={'id': record_id})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['rows_deleted'] == 1

def test_proxy_add_record():
    record_id = db_proxy.add_record('Proxy Test Data')
    assert record_id is not None

def test_proxy_fetch_records():
    records = db_proxy.fetch_records()
    assert isinstance(records, list)

def test_proxy_update_record():
    record_id = db_proxy.add_record('Proxy Test Data')
    rows_updated = db_proxy.update_record(record_id, 'Updated Proxy Data')
    assert rows_updated == 1

def test_proxy_delete_record():
    record_id = db_proxy.add_record('Proxy Test Data')
    rows_deleted = db_proxy.delete_record(record_id)
    assert rows_deleted == 1