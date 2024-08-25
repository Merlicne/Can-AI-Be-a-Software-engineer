import sqlite3

class DatabaseProxy:
    """
    Proxy class for database connections, managing connections and validating data.
    """

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def execute(self, query, args=None):
        """
        Executes an SQL query with data validation.
        """
        # Basic data validation
        if query.lower().startswith('insert'):
            self._validate_insert(args)
        # ... other validation rules ...

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, args)
            return cursor.fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def _validate_insert(self, args):
        """
        Validates data for INSERT queries.
        """
        # ... implementation for validation ...

class BookAPI:
    """
    API for managing Book data using the Proxy Pattern.
    """

    def __init__(self, db_file):
        self.db_proxy = DatabaseProxy(db_file)

    def create_book(self, title, author, isbn):
        """
        Creates a new book entry in the database.
        """
        with self.db_proxy as db:
            query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
            result = db.execute(query, (title, author, isbn))
            return result

    def get_book(self, isbn):
        """
        Retrieves a book by its ISBN.
        """
        with self.db_proxy as db:
            query = "SELECT * FROM books WHERE isbn = ?"
            result = db.execute(query, (isbn,))
            return result

    def update_book(self, isbn, title, author):
        """
        Updates an existing book's title and author.
        """
        with self.db_proxy as db:
            query = "UPDATE books SET title = ?, author = ? WHERE isbn = ?"
            result = db.execute(query, (title, author, isbn))
            return result

    def delete_book(self, isbn):
        """
        Deletes a book from the database.
        """
        with self.db_proxy as db:
            query = "DELETE FROM books WHERE isbn = ?"
            result = db.execute(query, (isbn,))
            return result

# Example usage:

# Create database table if it doesn't exist
def initialize_database(db_file):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE
            )
        """)

if __name__ == "__main__":
    db_file = "books.db"
    initialize_database(db_file)
    book_api = BookAPI(db_file)

    # Create a new book
    book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802")
    print("Book created successfully.")

    # Retrieve a book
    book = book_api.get_book("0345391802")
    print(f"Book found: {book}")

    # Update a book
    book_api.update_book("0345391802", "The Restaurant at the End of the Universe", "Douglas Adams")
    print("Book updated successfully.")

    # Delete a book
    book_api.delete_book("0345391802")
    print("Book deleted successfully.")