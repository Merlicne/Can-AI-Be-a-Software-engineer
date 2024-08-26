import unittest
import sqlite3
from unittest.mock import patch, MagicMock

from crud_api_proxy import Product, DatabaseProxy, ProductAPI

class TestProductAPI(unittest.TestCase):

    def setUp(self):
        self.db_path = ":memory:"  # Use in-memory database for testing
        self.api = ProductAPI(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL
            )
        """)

    def tearDown(self):
        self.conn.close()

    def test_create_product(self):
        # Test normal case
        product_data = {"name": "Laptop", "price": 1200.00}
        new_product_id = self.api.create(product_data)
        self.assertIsInstance(new_product_id, int)
        self.assertGreater(new_product_id, 0)

        # Test with missing data
        with self.assertRaisesRegex(Exception, "Missing required data: 'price'"):
            self.api.create({"name": "Laptop"})

        # Test with invalid data type
        with self.assertRaisesRegex(Exception, "Error creating product"):
            self.api.create({"name": "Laptop", "price": "invalid"})

    def test_read_product(self):
        # Test reading a specific product
        product_id = self.api.create({"name": "Keyboard", "price": 50.00})
        product = self.api.read(product_id)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.id, product_id)
        self.assertEqual(product.name, "Keyboard")
        self.assertEqual(product.price, 50.00)

        # Test reading non-existent product
        product = self.api.read(999)
        self.assertIsNone(product)

        # Test reading all products
        products = self.api.read()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 1)

    def test_update_product(self):
        # Test updating an existing product
        product_id = self.api.create({"name": "Mouse", "price": 25.00})
        self.api.update(product_id, {"name": "Gaming Mouse", "price": 75.00})

        updated_product = self.api.read(product_id)
        self.assertEqual(updated_product.name, "Gaming Mouse")
        self.assertEqual(updated_product.price, 75.00)

        # Test updating non-existent product
        with self.assertRaisesRegex(Exception, "Product with ID .* not found"):
            self.api.update(999, {"name": "New Name"})

        # Test updating with invalid data type
        with self.assertRaisesRegex(Exception, "Error updating product"):
            self.api.update(product_id, {"price": "invalid"})

    def test_delete_product(self):
        # Test deleting an existing product
        product_id = self.api.create({"name": "Monitor", "price": 200.00})
        self.api.delete(product_id)

        product = self.api.read(product_id)
        self.assertIsNone(product)

        # Test deleting non-existent product
        self.api.delete(999)  # Should not raise an error

    def test_database_proxy_connection(self):
        with DatabaseProxy(self.db_path) as db:
            self.assertIsNotNone(db._conn)
            self.assertTrue(db._conn.is_connected())

    @patch.object(sqlite3, "connect")
    def test_database_proxy_connection_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.OperationalError("Error connecting to database")
        with self.assertRaisesRegex(Exception, "Error connecting to database"):
            with DatabaseProxy(self.db_path) as db:
                pass

    @patch.object(sqlite3.Cursor, "execute")
    def test_database_proxy_create_product(self, mock_execute):
        mock_execute.return_value = MagicMock(lastrowid=1)
        with DatabaseProxy(self.db_path) as db:
            product = Product(name="Test Product", price=10.00)
            product_id = db.create_product(product)
            self.assertEqual(product_id, 1)
            mock_execute.assert_called_once_with(
                "INSERT INTO products (name, price) VALUES (?, ?)",
                (product.name, product.price)
            )

    @patch.object(sqlite3.Cursor, "execute")
    def test_database_proxy_get_product(self, mock_execute):
        mock_execute.return_value = MagicMock(fetchone=lambda: (1, "Test Product", 10.00))
        with DatabaseProxy(self.db_path) as db:
            product = db.get_product(1)
            self.assertIsInstance(product, Product)
            self.assertEqual(product.id, 1)
            self.assertEqual(product.name, "Test Product")
            self.assertEqual(product.price, 10.00)
            mock_execute.assert_called_once_with(
                "SELECT id, name, price FROM products WHERE id = ?", (1,)
            )

    @patch.object(sqlite3.Cursor, "execute")
    def test_database_proxy_get_products(self, mock_execute):
        mock_execute.return_value = MagicMock(
            fetchall=lambda: [(1, "Test Product 1", 10.00), (2, "Test Product 2", 20.00)]
        )
        with DatabaseProxy(self.db_path) as db:
            products = db.get_products()
            self.assertEqual(len(products), 2)
            self.assertIsInstance(products[0], Product)
            self.assertEqual(products[0].id, 1)
            self.assertEqual(products[0].name, "Test Product 1")
            self.assertEqual(products[0].price, 10.00)
            mock_execute.assert_called_once_with(
                "SELECT id, name, price FROM products"
            )

    @patch.object(sqlite3.Cursor, "execute")
    def test_database_proxy_update_product(self, mock_execute):
        with DatabaseProxy(self.db_path) as db:
            product = Product(id=1, name="Updated Product", price=15.00)
            db.update_product(product)
            mock_execute.assert_called_once_with(
                "UPDATE products SET name = ?, price = ? WHERE id = ?",
                (product.name, product.price, product.id)
            )

    @patch.object(sqlite3.Cursor, "execute")
    def test_database_proxy_delete_product(self, mock_execute):
        with DatabaseProxy(self.db_path) as db:
            db.delete_product(1)
            mock_execute.assert_called_once_with(
                "DELETE FROM products WHERE id = ?", (1,)
            )

if __name__ == "__main__":
    unittest.main()