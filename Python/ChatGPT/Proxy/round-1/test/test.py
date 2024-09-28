import pytest
import sqlite3
from flask import Flask, jsonify, request

# Assuming the code for DatabaseProxy, DatabaseManager, and Flask app is saved in `app.py`
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

from main import app, DatabaseProxy

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_database():
    proxy = DatabaseProxy("test.db")
    proxy.connect()
    proxy.create_table()
    yield proxy
    proxy._db_manager._connection.close()

def test_create_record(client, setup_database):
    response = client.post('/create', json={"name": "Test Name", "value": 42})
    assert response.status_code == 201
    assert response.json == {"message": "Record created successfully"}

    # Verify record in database
    records = setup_database.fetch_records()
    assert len(records) == 1
    assert records[0][1] == "Test Name"
    assert records[0][2] == 42

def test_read_records_empty(client, setup_database):
    response = client.get('/read')
    assert response.status_code == 200
    assert response.json == []

def test_read_records_non_empty(client, setup_database):
    setup_database.add_record({"name": "Test Name", "value": 42})
    response = client.get('/read')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == "Test Name"
    assert response.json[0]['value'] == 42

def test_update_record(client, setup_database):
    setup_database.add_record({"name": "Old Name", "value": 1})
    record_id = setup_database.fetch_records()[0][0]

    response = client.put(f'/update/{record_id}', json={"name": "New Name", "value": 100})
    assert response.status_code == 200
    assert response.json == {"message": "Record updated successfully"}

    # Verify update in database
    record = setup_database.fetch_records()[0]
    assert record[1] == "New Name"
    assert record[2] == 100

def test_delete_record(client, setup_database):
    setup_database.add_record({"name": "To Be Deleted", "value": 99})
    record_id = setup_database.fetch_records()[0][0]

    response = client.delete(f'/delete/{record_id}')
    assert response.status_code == 200
    assert response.json == {"message": "Record deleted successfully"}

    # Verify record is deleted
    records = setup_database.fetch_records()
    assert len(records) == 0

def test_proxy_logging_and_control(setup_database):
    proxy = setup_database

    # Test the logging of create operation
    proxy.add_record({"name": "Log Test", "value": 123})
    assert len(proxy.fetch_records()) == 1

    # Test the logging of read operation
    proxy.fetch_records()

    # Test the logging of update operation
    record_id = proxy.fetch_records()[0][0]
    proxy.update_record(record_id, {"name": "Updated Log Test", "value": 321})
    assert proxy.fetch_records()[0][2] == 321

    # Test the logging of delete operation
    proxy.delete_record(record_id)
    assert len(proxy.fetch_records()) == 0

    # In a real scenario, here you would check logs or mock the print statements.

if __name__ == "__main__":
    pytest.main(["--cov=app", "--cov-report=term-missing"])
