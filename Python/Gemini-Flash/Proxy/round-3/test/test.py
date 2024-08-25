import unittest
import sqlite3
from product_api import Product, DatabaseProxy, ProductAPI

class TestProductAPI(unittest.TestCase):

    def setUp(self):
        """Setup for test cases. Creates a temporary database."""
        self.db_path = ":memory:"  # Use in-memory database for testing
        self.api = ProductAPI(self.db_path)

    def tearDown(self):
        """Cleanup after test cases."""
        self.api.close()

    def test_connect(self):
        """Test establishing a database connection."""
        self.assertIsNotNone(self.api.db.conn)
        self.assertIsNotNone(self.api.db.cursor)

    def test_create(self):
        """Test creating a new product."""
        product = Product(None, "Test Product", 10.00, "Test description")
        product_id = self.api.create(product)
        self.assertIsNotNone(product_id)

        # Check if the product exists in the database
        created_product = self.api.read(product_id)
        self.assertEqual(created_product.name, "Test Product")
        self.assertEqual(created_product.price, 10.00)
        self.assertEqual(created_product.description, "Test description")

    def test_create_duplicate_product_id(self):
        """Test creating a product with an existing product ID (should fail)."""
        product1 = Product(1, "Test Product 1", 15.00, "Test description 1")
        self.api.create(product1)  # Create with ID 1

        product2 = Product(1, "Test Product 2", 20.00, "Test description 2")
        product_id = self.api.create(product2)  # Attempt to create with ID 1 again
        self.assertIsNone(product_id)  # Product ID should be None due to error

    def test_read(self):
        """Test reading a single product."""
        product = Product(None, "Test Product", 10.00, "Test description")
        product_id = self.api.create(product)
        read_product = self.api.read(product_id)
        self.assertEqual(read_product.product_id, product_id)
        self.assertEqual(read_product.name, "Test Product")
        self.assertEqual(read_product.price, 10.00)
        self.assertEqual(read_product.description, "Test description")

    def test_read_all(self):
        """Test reading all products."""
        products = [
            Product(None, "Product 1", 10.00),
            Product(None, "Product 2", 20.00),
            Product(None, "Product 3", 30.00),
        ]
        for product in products:
            self.api.create(product)

        all_products = self.api.read()
        self.assertEqual(len(all_products), 3)

    def test_read_non_existent_product(self):
        """Test reading a non-existent product."""
        read_product = self.api.read(100)
        self.assertIsNone(read_product)

    def test_update(self):
        """Test updating a product."""
        product = Product(None, "Test Product", 10.00, "Test description")
        product_id = self.api.create(product)

        updated_product = Product(product_id, "Updated Product", 15.00, "Updated description")
        update_success = self.api.update(updated_product)
        self.assertTrue(update_success)

        # Check if the product was updated in the database
        updated_product_from_db = self.api.read(product_id)
        self.assertEqual(updated_product_from_db.name, "Updated Product")
        self.assertEqual(updated_product_from_db.price, 15.00)
        self.assertEqual(updated_product_from_db.description, "Updated description")

    def test_update_non_existent_product(self):
        """Test updating a non-existent product."""
        product = Product(100, "Non-existent Product", 10.00, "Test description")
        update_success = self.api.update(product)
        self.assertFalse(update_success)

    def test_delete(self):
        """Test deleting a product."""
        product = Product(None, "Test Product", 10.00, "Test description")
        product_id = self.api.create(product)

        delete_success = self.api.delete(product_id)
        self.assertTrue(delete_success)

        # Check if the product was deleted
        deleted_product = self.api.read(product_id)
        self.assertIsNone(deleted_product)

    def test_delete_non_existent_product(self):
        """Test deleting a non-existent product."""
        delete_success = self.api.delete(100)
        self.assertFalse(delete_success)

    def test_close(self):
        """Test closing the database connection."""
        self.api.close()
        self.assertIsNone(self.api.db.conn)
        self.assertIsNone(self.api.db.cursor)

    def test_execute(self):
        """Test executing a simple query."""
        query = "SELECT COUNT(*) FROM products"
        self.api.db.execute(query)
        result = self.api.db.fetchall()
        self.assertIsNotNone(result)

    def test_execute_with_parameters(self):
        """Test executing a query with parameters."""
        product = Product(None, "Test Product", 10.00, "Test description")
        product_id = self.api.create(product)

        query = "SELECT * FROM products WHERE product_id = ?"
        self.api.db.execute(query, (product_id,))
        result = self.api.db.fetchall()
        self.assertEqual(len(result), 1)

    def test_fetchall(self):
        """Test fetching all rows from the cursor."""
        query = "SELECT * FROM products"
        self.api.db.execute(query)
        result = self.api.db.fetchall()
        self.assertIsNotNone(result)

    def test_commit(self):
        """Test committing changes to the database."""
        product = Product(None, "Test Product", 10.00, "Test description")
        product_id = self.api.create(product)
        self.api.db.commit()  # Commit the transaction
        self.assertIsNotNone(self.api.read(product_id))

    def test_connect_error(self):
        """Test connecting to a non-existent database (should fail)."""
        db_path = "nonexistent.db"  # Replace with a non-existent path
        proxy = DatabaseProxy(db_path)
        with self.assertRaises(sqlite3.OperationalError):
            proxy.connect()

    def test_execute_error(self):
        """Test executing an invalid SQL query (should fail)."""
        query = "INVALID SQL QUERY"
        with self.assertRaises(sqlite3.OperationalError):
            self.api.db.execute(query)

if __name__ == '__main__':
    unittest.main()