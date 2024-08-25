import sqlite3
import pytest
from app import app, DatabaseProxy  # Import your Flask app and DatabaseProxy

# Use a temporary database for testing
TEST_DATABASE = 'test_products.db'


# Fixture to create a test database and a DatabaseProxy instance
@pytest.fixture
def client_and_db():
    # Create a test client
    app.config['TESTING'] = True
    app.config['DATABASE'] = TEST_DATABASE
    test_client = app.test_client()

    # Create a test database and DatabaseProxy instance
    with app.app_context():
        db_proxy = DatabaseProxy(TEST_DATABASE)
        with db_proxy._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL
                )
            ''')

    yield test_client, db_proxy  # Return the client and DatabaseProxy

    # Clean up the test database after the tests
    with db_proxy._connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS products")


# Test cases for the CRUD API
class TestProductAPI:

    # Test getting all products (empty database)
    def test_get_all_products_empty(self, client_and_db):
        client, db_proxy = client_and_db
        response = client.get('/products')
        assert response.status_code == 200
        assert response.get_json() == []  # Expect an empty list

    # Test adding a new product
    def test_add_product(self, client_and_db):
        client, db_proxy = client_and_db
        data = {'name': 'Test Product', 'price': 19.99}
        response = client.post('/products', json=data)
        assert response.status_code == 201
        assert 'message' in response.get_json()
        assert 'id' in response.get_json()

    # Test getting all products (with one product added)
    def test_get_all_products(self, client_and_db):
        client, db_proxy = client_and_db
        # Add a product first
        self.test_add_product(client_and_db)

        response = client.get('/products')
        assert response.status_code == 200
        products = response.get_json()
        assert len(products) == 1
        assert products[0]['name'] == 'Test Product'
        assert products[0]['price'] == 19.99

    # Test getting a specific product by ID
    def test_get_product_by_id(self, client_and_db):
        client, db_proxy = client_and_db
        # Add a product first
        response = client.post('/products', json={'name': 'Test Product', 'price': 19.99})
        product_id = response.get_json()['id']

        response = client.get(f'/products/{product_id}')
        assert response.status_code == 200
        product = response.get_json()
        assert product['id'] == product_id
        assert product['name'] == 'Test Product'
        assert product['price'] == 19.99

    # Test getting a product with a non-existent ID
    def test_get_product_not_found(self, client_and_db):
        client, db_proxy = client_and_db
        response = client.get('/products/999')  # Assuming 999 is an invalid ID
        assert response.status_code == 404
        assert response.get_json()['message'] == 'Product not found'

    # Test updating an existing product
    def test_update_product(self, client_and_db):
        client, db_proxy = client_and_db
        # Add a product first
        response = client.post('/products', json={'name': 'Test Product', 'price': 19.99})
        product_id = response.get_json()['id']

        data = {'name': 'Updated Product', 'price': 29.99}
        response = client.put(f'/products/{product_id}', json=data)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Product updated successfully'

        # Verify if the update was successful
        response = client.get(f'/products/{product_id}')
        assert response.status_code == 200
        product = response.get_json()
        assert product['name'] == 'Updated Product'
        assert product['price'] == 29.99

    # Test updating a product with a non-existent ID
    def test_update_product_not_found(self, client_and_db):
        client, db_proxy = client_and_db
        data = {'name': 'Updated Product', 'price': 29.99}
        response = client.put('/products/999', json=data)  # Assuming 999 is an invalid ID
        assert response.status_code == 404
        assert response.get_json()['message'] == 'Product not found'

    # Test deleting an existing product
    def test_delete_product(self, client_and_db):
        client, db_proxy = client_and_db
        # Add a product first
        response = client.post('/products', json={'name': 'Test Product', 'price': 19.99})
        product_id = response.get_json()['id']

        response = client.delete(f'/products/{product_id}')
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Product deleted successfully'

        # Try to get the deleted product (should be not found)
        response = client.get(f'/products/{product_id}')
        assert response.status_code == 404
        assert response.get_json()['message'] == 'Product not found'

    # Test deleting a product with a non-existent ID
    def test_delete_product_not_found(self, client_and_db):
        client, db_proxy = client_and_db
        response = client.delete('/products/999')  # Assuming 999 is an invalid ID
        assert response.status_code == 404
        assert response.get_json()['message'] == 'Product not found'


# DatabaseProxy test cases
class TestDatabaseProxy:

    # Test adding a product using DatabaseProxy
    def test_db_add_product(self, client_and_db):
        _, db_proxy = client_and_db
        product_id = db_proxy.add_product('Test Db Product', 19.99)
        assert isinstance(product_id, int)  # Check if the returned ID is an integer

        # Verify if the product exists in the database
        product = db_proxy.get_product_by_id(product_id)
        assert product is not None
        assert product[1] == 'Test Db Product'
        assert product[2] == 19.99

    # Test updating a product using DatabaseProxy
    def test_db_update_product(self, client_and_db):
        _, db_proxy = client_and_db
        # Add a product first
        product_id = db_proxy.add_product('Test Db Product', 19.99)

        # Update the product
        updated_rows = db_proxy.update_product(product_id, 'Updated Db Product', 29.99)
        assert updated_rows == 1  # One row should be updated

        # Verify the update
        product = db_proxy.get_product_by_id(product_id)
        assert product[1] == 'Updated Db Product'
        assert product[2] == 29.99

    # Test deleting a product using DatabaseProxy
    def test_db_delete_product(self, client_and_db):
        _, db_proxy = client_and_db
        # Add a product first
        product_id = db_proxy.add_product('Test Db Product', 19.99)

        # Delete the product
        deleted_rows = db_proxy.delete_product(product_id)
        assert deleted_rows == 1  # One row should be deleted

        # Verify the deletion
        product = db_proxy.get_product_by_id(product_id)
        assert product is None  # Product should not exist anymore