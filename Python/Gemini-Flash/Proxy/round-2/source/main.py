import sqlite3
from typing import Dict, List, Optional


class DatabaseProxy:
    """
    A Proxy class for handling database connection, transaction management, and authorization.
    """

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        """
        if not self.conn:
            print("Connecting to database...")
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row  # Enable dictionary-like row access
        else:
            print("Already connected to database.")

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            print("Closing database connection...")
            self.conn.close()
            self.conn = None
        else:
            print("Connection already closed.")

    def execute(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Executes a SQL query and returns the result as a list of dictionaries.
        """
        self.connect()  # Ensure connection is open
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def __enter__(self):
        print("Entering context: opening connection.")
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting context: closing connection.")
        self.close()


class ProductAPI:
    """
    A simple CRUD API for managing product data.
    """

    def __init__(self, db_file: str):
        self.db_proxy = DatabaseProxy(db_file)

    def create_product(self, product_data: Dict) -> Dict:
        """
        Creates a new product in the database.

        Args:
            product_data: A dictionary containing product information.

        Returns:
            The created product data.

        Raises:
            Exception: If an error occurs during the creation process.
        """
        with self.db_proxy as db:
            try:
                query = """
                    INSERT INTO products (name, description, price, quantity)
                    VALUES (?, ?, ?, ?)
                """
                params = (
                    product_data['name'],
                    product_data['description'],
                    product_data['price'],
                    product_data['quantity'],
                )
                cursor = db.conn.cursor()
                cursor.execute(query, params)
                db.conn.commit()
                product_data['id'] = cursor.lastrowid  # Accessing lastrowid from the cursor
                return product_data
            except Exception as e:
                raise Exception("Failed to create product: {}".format(e))

    def get_products(self) -> List[Dict]:
        """
        Retrieves all products from the database.

        Returns:
            A list of product dictionaries.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        with self.db_proxy as db:
            try:
                query = """
                    SELECT * FROM products
                """
                return db.execute(query)
            except Exception as e:
                raise Exception("Failed to retrieve products: {}".format(e))

    def get_product(self, product_id: int) -> Optional[Dict]:
        """
        Retrieves a product by its ID.

        Args:
            product_id: The ID of the product to retrieve.

        Returns:
            The product dictionary, or None if the product is not found.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        with self.db_proxy as db:
            try:
                query = """
                    SELECT * FROM products WHERE id = ?
                """
                products = db.execute(query, (product_id,))
                return products[0] if products else None
            except Exception as e:
                raise Exception("Failed to retrieve product: {}".format(e))

    def update_product(self, product_id: int, product_data: Dict) -> Optional[Dict]:
        """
        Updates an existing product in the database.

        Args:
            product_id: The ID of the product to update.
            product_data: A dictionary containing the updated product information.

        Returns:
            The updated product data, or None if the product is not found.

        Raises:
            Exception: If an error occurs during the update process.
        """
        with self.db_proxy as db:
            try:
                existing_product = self.get_product(product_id)
                if not existing_product:
                    return None

                updated_data = {
                    'name': product_data.get('name', existing_product['name']),
                    'description': product_data.get('description', existing_product['description']),
                    'price': product_data.get('price', existing_product['price']),
                    'quantity': product_data.get('quantity', existing_product['quantity']),
                }

                query = """
                    UPDATE products
                    SET name = ?, description = ?, price = ?, quantity = ?
                    WHERE id = ?
                """
                params = (
                    updated_data['name'],
                    updated_data['description'],
                    updated_data['price'],
                    updated_data['quantity'],
                    product_id,
                )
                db.execute(query, params)
                return updated_data
            except Exception as e:
                raise Exception(f"Failed to update product: {e}")

    def delete_product(self, product_id: int) -> bool:
        """
        Deletes a product from the database.

        Args:
            product_id: The ID of the product to delete.

        Returns:
            True if the product was deleted successfully, False otherwise.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        with self.db_proxy as db:
            try:
                query = """
                    DELETE FROM products WHERE id = ?
                """
                db.execute(query, (product_id,))
                return True
            except Exception as e:
                raise Exception("Failed to delete product: {}".format(e))


# Initialize the database and create a table if it doesn't exist
def initialize_database(db_file: str):
    """
    Creates the products table if it doesn't exist.
    """
    with sqlite3.connect(db_file) as conn:
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


# Example usage
if __name__ == "__main__":
    db_file = "products.db"
    initialize_database(db_file)

    api = ProductAPI(db_file)

    # Create a new product
    new_product = api.create_product(
        {
            "name": "Laptop",
            "description": "A powerful laptop for work and play.",
            "price": 1200.00,
            "quantity": 5,
        }
    )
    print("Created product:", new_product)

    # Get all products
    products = api.get_products()
    print("All products:", products)

    # Get a product by ID
    product = api.get_product(1)
    print("Product with ID 1:", product)

    # Update a product
    updated_product = api.update_product(
        1, {"name": "Laptop Pro", "description": "An even more powerful laptop."}
    )
    print("Updated product:", updated_product)

    # Delete a product
    deleted = api.delete_product(1)
    print("Deleted product:", deleted)