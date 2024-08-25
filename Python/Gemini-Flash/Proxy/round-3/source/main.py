import sqlite3
from typing import Dict, List, Tuple

class Product:
    """Represents a product entity."""

    def __init__(self, product_id: int, name: str, price: float, description: str = None):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description

    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.name}', price={self.price}, description='{self.description}')"

class DatabaseProxy:
    """Proxy class for database interactions."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    def execute(self, query: str, parameters: Tuple = None):
        """Executes a SQL query with optional parameters."""
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database query error: {e}")

    def commit(self):
        """Commits changes to the database."""
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database commit error: {e}")

    def fetchall(self) -> List[Tuple]:
        """Fetches all rows from the cursor."""
        try:
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database fetch error: {e}")

class ProductAPI:
    """API for managing product data."""

    def __init__(self, db_path: str):
        self.db = DatabaseProxy(db_path)
        self.db.connect()

        # Create table if it doesn't exist
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT
            )
        """)

    def create(self, product: Product) -> int:
        """Creates a new product in the database."""
        try:
            query = "INSERT INTO products (name, price, description) VALUES (?, ?, ?)"
            self.db.execute(query, (product.name, product.price, product.description))
            self.db.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error creating product: {e}")
            return None

    def read(self, product_id: int = None) -> List[Product] or Product:
        """Reads product(s) from the database."""
        try:
            if product_id:
                query = "SELECT * FROM products WHERE product_id = ?"
                self.db.execute(query, (product_id,))
                row = self.db.fetchall()
                if row:
                    return Product(row[0][0], row[0][1], row[0][2], row[0][3])
                else:
                    return None
            else:
                query = "SELECT * FROM products"
                self.db.execute(query)
                products = [
                    Product(row[0], row[1], row[2], row[3]) for row in self.db.fetchall()
                ]
                return products
        except Exception as e:
            print(f"Error reading product(s): {e}")
            return None

    def update(self, product: Product) -> bool:
        """Updates an existing product in the database."""
        try:
            query = "UPDATE products SET name=?, price=?, description=? WHERE product_id=?"
            self.db.execute(query, (product.name, product.price, product.description, product.product_id))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def delete(self, product_id: int) -> bool:
        """Deletes a product from the database."""
        try:
            query = "DELETE FROM products WHERE product_id = ?"
            self.db.execute(query, (product_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    def close(self):
        """Closes the database connection."""
        self.db.close()

# Example usage
if __name__ == "__main__":
    api = ProductAPI("products.db")

    # Create new products
    product1 = Product(None, "Laptop", 1200.00, "Powerful laptop")
    product2 = Product(None, "Keyboard", 50.00, "Mechanical keyboard")

    api.create(product1)
    api.create(product2)

    # Read products
    print("All Products:")
    for product in api.read():
        print(product)

    print("\nProduct with ID 1:")
    product = api.read(1)
    print(product)

    # Update product
    product.name = "Gaming Laptop"
    api.update(product)

    print("\nUpdated Product:")
    print(api.read(1))

    # Delete product
    api.delete(2)

    # Close the connection
    api.close()