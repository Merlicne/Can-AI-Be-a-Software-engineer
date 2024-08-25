import pytest
import sqlite3
from flask import Flask, request, jsonify
from your_module import app, DatabaseProxy, DatabaseManager  # Adjust import as necessary

# Setup a test database
@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db_proxy = DatabaseProxy('test.db')
            db_proxy.connect()
            db_proxy.db_manager.create_table()
        yield client
        db_proxy.db_manager.close()

# Test POST /create
def test_create_record(test_client):
    response = test_client.post('/create', json={'data': 'Test Data'})
    assert response.status_code == 201
    assert response.json['message'] == 'Record created'

# Test GET /read
def test_read_records(test_client):
    response = test_client.get('/read')
    assert response.status_code == 200
    assert len(response.json) > 0

# Test PUT /update
def test_update_record(test_client):
    response = test_client.put('/update', json={'id': 1, 'data': 'Updated Data'})
    assert response.status_code == 200
    assert response.json['message'] == 'Record updated'

# Test DELETE /delete
def test_delete_record(test_client):
    response = test_client.delete('/delete', json={'id': 1})
    assert response.status_code == 200
    assert response.json['message'] == 'Record deleted'

# Test Proxy Class
def test_proxy_methods():
    db_proxy = DatabaseProxy('test.db')
    db_proxy.connect()
    db_proxy.create('Proxy Test Data')
    records = db_proxy.read()
    assert len(records) > 0
    db_proxy.update(records[0][0], 'Proxy Updated Data')
    updated_records = db_proxy.read()
    assert updated_records[0][1] == 'Proxy Updated Data'
    db_proxy.delete(records[0][0])
    final_records = db_proxy.read()
    assert len(final_records) == 0
    db_proxy.close()

if __name__ == '__main__':
    pytest.main(['--cov=your_module', '--cov-report=term-missing'])