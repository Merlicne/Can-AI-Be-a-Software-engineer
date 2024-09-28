import pytest

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

from main import app, db_manager, db_proxy

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db_manager.execute("DROP TABLE IF EXISTS records")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL
            );
            """
            db_proxy.execute(create_table_query)
        yield client

def test_create_record(client):
    # Test creating a new record
    response = client.post('/create', json={'name': 'John', 'value': 'Doe'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data

def test_read_empty_records(client):
    # Test reading when database is empty
    response = client.get('/read')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_read_multiple_records(client):
    # Create multiple records
    client.post('/create', json={'name': 'Alice', 'value': 'Wonderland'})
    client.post('/create', json={'name': 'Bob', 'value': 'Builder'})
    
    # Test reading records
    response = client.get('/read')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0][1] == 'Alice'
    assert data[1][1] == 'Bob'

def test_update_record(client):
    # Create a record
    response = client.post('/create', json={'name': 'Charlie', 'value': 'Chaplin'})
    record_id = response.get_json()['id']
    
    # Update the record
    response = client.put(f'/update/{record_id}', json={'name': 'Charlie', 'value': 'Chapman'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Record updated'
    
    # Verify the record was updated
    response = client.get('/read')
    data = response.get_json()
    assert data[0][2] == 'Chapman'

def test_delete_record(client):
    # Create a record
    response = client.post('/create', json={'name': 'David', 'value': 'Bowie'})
    record_id = response.get_json()['id']
    
    # Delete the record
    response = client.delete(f'/delete/{record_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Record deleted'
    
    # Verify the record was deleted
    response = client.get('/read')
    data = response.get_json()
    assert data == []

def test_proxy_logging_and_execution(client, caplog):
    # Test that proxy logs and executes correctly
    with caplog.at_level('INFO'):
        db_proxy.execute("INSERT INTO records (name, value) VALUES (?, ?)", ('Test', 'Logging'))
        assert 'Executing query' in caplog.text
        assert 'Query Result' in caplog.text

    # Test fetching via proxy
    with caplog.at_level('INFO'):
        result = db_proxy.fetchall("SELECT * FROM records WHERE name = ?", ('Test',))
        assert 'Fetching all records with query' in caplog.text
        assert result[0][1] == 'Test'

    # Test fetching one record via proxy
    with caplog.at_level('INFO'):
        result = db_proxy.fetchone("SELECT * FROM records WHERE name = ?", ('Test',))
        assert 'Fetching one record with query' in caplog.text
        assert result[1] == 'Test'
