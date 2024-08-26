import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock

from your_module import DatabaseProxy, ProductAPI  # Replace "your_module" with the actual module name


class TestDatabaseProxy(unittest.TestCase):

    def setUp(self):
        self.db_file = ":memory:"  # In-memory database for testing
        self.db_proxy = DatabaseProxy(self.db_file)

    def test_connect(self):
        self.db_proxy.connect()
        self.assertIsNotNone(self.db_proxy.conn)

    def test_close(self):
        self.db_proxy.connect()
        self.db_proxy.close()
        self.assertIsNone(self.db_proxy.conn)

    @patch("sqlite3.connect")
    def test_execute_success(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, "Product 1", "Description 1", 10.0, 5)]

        query = "SELECT * FROM products"
        result = self.db_proxy.execute(query)

        self.assertEqual(result, [{"id": 1, "name": "Product 1", "description": "Description 1", "price": 10.0, "quantity": 5}])
        mock_connect.assert_called_once_with(self.db_file)
        mock_cursor.execute.assert_called_once_with(query)
        mock_cursor.fetchall.assert_called_once()
        mock_connect.return_value.commit.assert_called_once()

    @patch("sqlite3.connect")
    def test_execute_with_params(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [(1, "Product 1", "Description 1", 10.0, 5)]

        query = "SELECT * FROM products WHERE id = ?"
        params = (1,)
        result = self.db_proxy.execute(query, params)

        self.assertEqual(result, [{"id": 1, "name": "Product 1", "description": "Description 1", "price": 10.0, "quantity": 5}])
        mock_connect.assert_called_once_with(self.db_file)
        mock_cursor.execute.assert_called_once_with(query, params)
        mock_cursor.fetchall.assert_called_once()
        mock_connect.return_value.commit.assert_called_once()

    @patch("sqlite3.connect")
    def test_execute_failure(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")

        query = "SELECT * FROM products"
        with self.assertRaises(sqlite3.Error):
            self.db_proxy.execute(query)

        mock_connect.assert_called_once_with(self.db_file)
        mock_cursor.execute.assert_called_once_with(query)
        mock_connect.return_value.rollback.assert_called_once()

    def test_context_manager(self):
        with self.db_proxy as db:
            self.assertIsNotNone(db.conn)
        self.assertIsNone(self.db_proxy.conn)


class TestProductAPI(unittest.TestCase):

    def setUp(self):
        self.db_file = ":memory:"
        self.api = ProductAPI(self.db_file)

        # Initialize database table
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """)

    def test_create_product_success(self):
        product_data = {
            "name": "Product 1",
            "description": "Description 1",
            "price": 10.0,
            "quantity": 5,
        }
        created_product = self.api.create_product(product_data)

        self.assertEqual(created_product['name'], "Product 1")
        self.assertEqual(created_product['description'], "Description 1")
        self.assertEqual(created_product['price'], 10.0)
        self.assertEqual(created_product['quantity'], 5)
        self.assertIsNotNone(created_product['id'])

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_create_product_failure(self, mock_execute):
        mock_execute.side_effect = sqlite3.Error("Database error")
        product_data = {
            "name": "Product 1",
            "description": "Description 1",
            "price": 10.0,
            "quantity": 5,
        }

        with self.assertRaisesRegex(Exception, "Failed to create product"):
            self.api.create_product(product_data)

        mock_execute.assert_called_once()

    def test_get_products_success(self):
        # Add some products to the database
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES ('Product 1', 'Description 1', 10.0, 5)")
            cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES ('Product 2', 'Description 2', 20.0, 10)")

        products = self.api.get_products()
        self.assertEqual(len(products), 2)

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_get_products_failure(self, mock_execute):
        mock_execute.side_effect = sqlite3.Error("Database error")

        with self.assertRaisesRegex(Exception, "Failed to retrieve products"):
            self.api.get_products()

        mock_execute.assert_called_once()

    def test_get_product_success(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES ('Product 1', 'Description 1', 10.0, 5)")

        product = self.api.get_product(1)
        self.assertEqual(product['name'], "Product 1")
        self.assertEqual(product['description'], "Description 1")
        self.assertEqual(product['price'], 10.0)
        self.assertEqual(product['quantity'], 5)

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_get_product_not_found(self, mock_execute):
        mock_execute.return_value = []
        product = self.api.get_product(1)
        self.assertIsNone(product)
        mock_execute.assert_called_once()

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_get_product_failure(self, mock_execute):
        mock_execute.side_effect = sqlite3.Error("Database error")

        with self.assertRaisesRegex(Exception, "Failed to retrieve product"):
            self.api.get_product(1)

        mock_execute.assert_called_once()

    def test_update_product_success(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES ('Product 1', 'Description 1', 10.0, 5)")

        updated_product = self.api.update_product(1, {"name": "Updated Product", "description": "Updated Description"})

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = 1")
            result = cursor.fetchone()
            self.assertEqual(result[1], "Updated Product")
            self.assertEqual(result[2], "Updated Description")

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_update_product_not_found(self, mock_execute):
        mock_execute.return_value = []
        updated_product = self.api.update_product(1, {"name": "Updated Product", "description": "Updated Description"})
        self.assertIsNone(updated_product)
        mock_execute.assert_called_once()

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_update_product_failure(self, mock_execute):
        mock_execute.side_effect = sqlite3.Error("Database error")

        with self.assertRaisesRegex(Exception, "Failed to update product"):
            self.api.update_product(1, {"name": "Updated Product", "description": "Updated Description"})

        mock_execute.assert_called_once()

    def test_delete_product_success(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, description, price, quantity) VALUES ('Product 1', 'Description 1', 10.0, 5)")

        deleted = self.api.delete_product(1)
        self.assertTrue(deleted)

        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = 1")
            result = cursor.fetchone()
            self.assertIsNone(result)

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_delete_product_not_found(self, mock_execute):
        mock_execute.return_value = []
        deleted = self.api.delete_product(1)
        self.assertTrue(deleted)
        mock_execute.assert_called_once()

    @patch("your_module.DatabaseProxy.execute")  # Replace "your_module" with the actual module name
    def test_delete_product_failure(self, mock_execute):
        mock_execute.side_effect = sqlite3.Error("Database error")

        with self.assertRaisesRegex(Exception, "Failed to delete product"):
            self.api.delete_product(1)

        mock_execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()