import sqlite3
import json
import pytest
from app import app, DatabaseProxy  # Import your Flask app and DatabaseProxy

# --- Fixtures ---

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db_proxy():
    """Create a DatabaseProxy instance with a test database."""
    test_db = 'test_products.db'
    proxy = DatabaseProxy(test_db)

    # Create the table
    with proxy.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

    yield proxy

    # Clean up - delete the test database
    # import os
    # os.remove(test_db) 

@pytest.fixture
def test_data(db_proxy):
    """Insert some test data into the database."""
    db_proxy.add_product("Test Product 1", 10.0)
    db_proxy.add_product("Test Product 2", 20.0)
    

# --- Test Cases ---

def test_get_products(client, db_proxy, test_data):
    """Test retrieving all products."""
    response = client.get('/products')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data) == 2  # Make sure both test products are returned

def test_get_product(client, db_proxy, test_data):
    """Test retrieving a specific product by ID."""
    response = client.get('/products/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Product 1'

def test_get_product_not_found(client):
    """Test retrieving a product that does not exist."""
    response = client.get('/products/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'message' in data

def test_add_product(client, db_proxy, test_data):
    """Test adding a new product."""
    new_product = {'name': 'New Product', 'price': 15.5}
    response = client.post('/products', json=new_product)

    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data 
    assert data['name'] == 'New Product'
    assert data['price'] == 15.5

    # Check if the product exists in the database
    db_product = db_proxy.get_product(data['id'])
    assert db_product is not None

def test_update_product(client, db_proxy, test_data):
    """Test updating an existing product."""
    updated_product = {'name': 'Updated Product', 'price': 25.0}
    response = client.put('/products/1', json=updated_product)
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Updated Product'
    assert data['price'] == 25.0

    # Check if the product was updated in the database
    db_product = db_proxy.get_product(1)
    assert db_product['name'] == 'Updated Product'
    assert db_product['price'] == 25.0

def test_delete_product(client, db_proxy, test_data):
    """Test deleting a product."""
    response = client.delete('/products/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Product with id 1 deleted successfully'

    # Check if the product is actually deleted
    deleted_product = db_proxy.get_product(1)
    assert deleted_product is None  

# --- DatabaseProxy Test Cases ---

def test_db_proxy_get_products(db_proxy, test_data):
    products = db_proxy.get_products()
    assert isinstance(products, list)
    assert len(products) > 0 

def test_db_proxy_get_product(db_proxy, test_data):
    product = db_proxy.get_product(1)
    assert isinstance(product, dict)
    assert product['id'] == 1 

def test_db_proxy_add_product(db_proxy):
    product = db_proxy.add_product("Test Product 3", 30.0)
    assert isinstance(product, dict)
    assert product['name'] == "Test Product 3" 

def test_db_proxy_update_product(db_proxy, test_data):
    updated = db_proxy.update_product(1, "Updated Name", 15.0)
    assert updated['name'] == "Updated Name"

def test_db_proxy_delete_product(db_proxy, test_data):
    db_proxy.delete_product(1)
    assert db_proxy.get_product(1) is None