import sqlite3
from typing import Dict, List, Optional, Union

class Product:
    """Represents a product in the database."""

    def __init__(self, id: int = None, name: str = None, price: float = None):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"

class DatabaseProxy:
    """Proxy class for database interactions."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None
        self.connect()
        self.initialize_database()  # Create table if it does not exist

    def connect(self):
        """Establish a connection to the database."""
        self._conn = sqlite3.connect(self.db_path)

    def close(self):
        """Close the database connection."""
        if self._conn:
            self._conn.commit()
            self._conn.close()
            self._conn = None

    def __enter__(self):
        if not self._conn:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def initialize_database(self):
        """Create the products table if it does not exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        );
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute(create_table_query)
            self._conn.commit()
        except Exception as e:
            raise Exception(f"Error initializing database: {e}")

    def create_product(self, product: Product) -> int:
        """Creates a new product in the database."""
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, price) VALUES (?, ?)",
                (product.name, product.price),
            )
            return cursor.lastrowid
        except Exception as e:
            raise Exception(f"Error creating product: {e}")

    def get_product(self, product_id: int) -> Optional[Product]:
        """Retrieves a product by its ID."""
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT id, name, price FROM products WHERE id = ?", (product_id,)
            )
            row = cursor.fetchone()
            if row:
                return Product(row[0], row[1], row[2])
            else:
                return None
        except Exception as e:
            raise Exception(f"Error getting product: {e}")

    def get_products(self) -> List[Product]:
        """Retrieves all products from the database."""
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT id, name, price FROM products")
            rows = cursor.fetchall()
            return [Product(row[0], row[1], row[2]) for row in rows]
        except Exception as e:
            raise Exception(f"Error getting products: {e}")

    def update_product(self, product: Product) -> None:
        """Updates an existing product in the database."""
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "UPDATE products SET name = ?, price = ? WHERE id = ?",
                (product.name, product.price, product.id),
            )
        except Exception as e:
            raise Exception(f"Error updating product: {e}")

    def delete_product(self, product_id: int) -> None:
        """Deletes a product from the database."""
        try:
            cursor = self._conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        except Exception as e:
            raise Exception(f"Error deleting product: {e}")

class ProductAPI:
    """API for managing product data."""

    def __init__(self, db_path: str):
        self.db = DatabaseProxy(db_path)

    def create(self, product_data: Dict) -> int:
        """Creates a new product."""
        try:
            product = Product(name=product_data["name"], price=product_data["price"])
            return self.db.create_product(product)
        except KeyError as e:
            raise Exception(f"Missing required data: {e}")
        except Exception as e:
            raise Exception(f"Error creating product: {e}")

    def read(self, product_id: Optional[int] = None) -> Union[Product, List[Product]]:
        """Reads a product or all products."""
        if product_id:
            try:
                return self.db.get_product(product_id)
            except Exception as e:
                raise Exception(f"Error reading product: {e}")
        else:
            try:
                return self.db.get_products()
            except Exception as e:
                raise Exception(f"Error reading products: {e}")

    def update(self, product_id: int, product_data: Dict) -> None:
        """Updates an existing product."""
        try:
            product = self.db.get_product(product_id)
            if product:
                product.name = product_data.get("name", product.name)
                product.price = product_data.get("price", product.price)
                self.db.update_product(product)
            else:
                raise Exception(f"Product with ID {product_id} not found.")
        except KeyError as e:
            raise Exception(f"Missing required data: {e}")
        except Exception as e:
            raise Exception(f"Error updating product: {e}")

    def delete(self, product_id: int) -> None:
        """Deletes a product."""
        try:
            self.db.delete_product(product_id)
        except Exception as e:
            raise Exception(f"Error deleting product: {e}")

# Initialize the API with the database path
api = ProductAPI("products.db")

# Example usage
# Create a product
new_product_id = api.create({"name": "Laptop", "price": 1200.00})
print(f"New product created with ID: {new_product_id}")

# Read a product
product = api.read(new_product_id)
print(f"Product details: {product}")

# Update a product
api.update(new_product_id, {"name": "Laptop Pro"})

# Read the updated product
updated_product = api.read(new_product_id)
print(f"Updated product details: {updated_product}")

# Delete a product
api.delete(new_product_id)

# Read all products
products = api.read()
print(f"All products: {products}")
