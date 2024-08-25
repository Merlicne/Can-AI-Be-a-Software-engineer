import sqlite3
import json
import pytest
from app import app, DatabaseProxy  # Import your Flask app instance and DatabaseProxy

# --- Pytest Fixtures ---

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_proxy():
    """Create a DatabaseProxy instance with a test database."""
    TEST_DATABASE = 'test_products.db'
    proxy = DatabaseProxy(TEST_DATABASE)
    # Initialize the test database
    with proxy._connect() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
            '''
        )
    yield proxy
    # Clean up after tests
    with proxy._connect() as conn:
        conn.execute("DROP TABLE products")

@pytest.fixture
def product_data():
    """Provide sample product data."""
    return {'name': 'Test Product', 'price': 19.99}


# --- Test Cases ---

def test_get_products_empty(client, db_proxy):
    """Test retrieving products from an empty database."""
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json == []


def test_add_product(client, db_proxy, product_data):
    """Test adding a new product."""
    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'id' in response.json and response.json['id'] is not None

    # Verify product was added to the database
    product = db_proxy.get_product(response.json['id'])
    assert product['name'] == product_data['name']
    assert product['price'] == product_data['price']


def test_add_product_invalid_data(client):
    """Test adding a product with missing data."""
    response = client.post('/products', json={'name': 'Test Product'})  # Missing price
    assert response.status_code == 400
    assert 'error' in response.json


def test_get_product(client, db_proxy, product_data):
    """Test retrieving a specific product."""
    # First, add a product
    product_id = db_proxy.add_product(product_data['name'], product_data['price'])

    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json['id'] == product_id
    assert response.json['name'] == product_data['name']
    assert response.json['price'] == product_data['price']


def test_get_product_not_found(client):
    """Test retrieving a product that does not exist."""
    response = client.get('/products/9999') 
    assert response.status_code == 404
    assert 'error' in response.json


def test_update_product(client, db_proxy, product_data):
    """Test updating an existing product."""
    # Add a product
    product_id = db_proxy.add_product(product_data['name'], product_data['price'])

    # Update the product
    updated_data = {'name': 'Updated Product', 'price': 29.99}
    response = client.put(f'/products/{product_id}', json=updated_data)
    assert response.status_code == 200
    assert 'message' in response.json

    # Verify update in the database
    product = db_proxy.get_product(product_id)
    assert product['name'] == updated_data['name']
    assert product['price'] == updated_data['price']


def test_update_product_not_found(client):
    """Test updating a product that does not exist."""
    response = client.put('/products/9999', json={'name': 'Updated', 'price': 1.99})
    assert response.status_code == 404
    assert 'error' in response.json


def test_delete_product(client, db_proxy, product_data):
    """Test deleting a product."""
    # Add a product
    product_id = db_proxy.add_product(product_data['name'], product_data['price'])

    # Delete the product
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 200
    assert 'message' in response.json

    # Verify deletion from the database
    product = db_proxy.get_product(product_id)
    assert product is None


def test_delete_product_not_found(client):
    """Test deleting a product that does not exist."""
    response = client.delete('/products/9999')
    assert response.status_code == 404
    assert 'error' in response.json