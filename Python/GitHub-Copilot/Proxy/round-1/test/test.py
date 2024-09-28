import pytest
from flask import Flask, jsonify, request
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))
from main import app, db_proxy
from database_manager import DatabaseManager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db_proxy.create_table()
        yield client

def test_create_record(client):
    response = client.post('/create', json={'data': 'test data'})
    assert response.status_code == 201
    assert response.json == {"message": "Record added"}

def test_read_records_empty(client):
    response = client.get('/read')
    assert response.status_code == 200
    assert response.json == []

def test_create_and_read_records(client):
    client.post('/create', json={'data': 'test data 1'})
    client.post('/create', json={'data': 'test data 2'})
    response = client.get('/read')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_update_record(client):
    client.post('/create', json={'data': 'test data'})
    response = client.put('/update/1', json={'data': 'updated data'})
    assert response.status_code == 200
    assert response.json == {"message": "Record updated"}
    response = client.get('/read')
    assert response.json[0][1] == 'updated data'

def test_delete_record(client):
    client.post('/create', json={'data': 'test data'})
    response = client.delete('/delete/1')
    assert response.status_code == 200
    assert response.json == {"message": "Record deleted"}
    response = client.get('/read')
    assert response.json == []