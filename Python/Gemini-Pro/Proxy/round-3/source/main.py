import sqlite3


class DatabaseProxy:
    """
    Proxy class for managing database connections and interactions.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Establishes a database connection if one doesn't exist."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_name)
            self.create_table()

    def disconnect(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_table(self):
        """Creates the 'books' table if it doesn't exist."""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def execute_query(self, query, params=None):
        """Executes a given SQL query with optional parameters."""
        self.connect()
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor.fetchall()


class BookAPI:
    """
    Provides a CRUD API for managing book data through the DatabaseProxy.
    """

    def __init__(self, db_proxy):
        self.db_proxy = db_proxy

    def create_book(self, title, author, isbn):
        """Creates a new book entry in the database."""
        query = "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)"
        self.db_proxy.execute_query(query, (isbn, title, author))
        return {"message": f"Book with ISBN {isbn} created successfully."}

    def get_book(self, isbn):
        """Retrieves a book entry by its ISBN."""
        query = "SELECT * FROM books WHERE isbn = ?"
        result = self.db_proxy.execute_query(query, (isbn,))
        if result:
            book = {"isbn": result[0][0], "title": result[0][1], "author": result[0][2]}
            return book
        else:
            return {"message": f"Book with ISBN {isbn} not found."}

    def update_book(self, isbn, title=None, author=None):
        """Updates a book entry by its ISBN."""
        query = "UPDATE books SET "
        params = []
        if title:
            query += "title = ?,"
            params.append(title)
        if author:
            query += "author = ?,"
            params.append(author)
        query = query[:-1] + " WHERE isbn = ?"
        params.append(isbn)
        self.db_proxy.execute_query(query, tuple(params))
        return {"message": f"Book with ISBN {isbn} updated successfully."}

    def delete_book(self, isbn):
        """Deletes a book entry by its ISBN."""
        query = "DELETE FROM books WHERE isbn = ?"
        self.db_proxy.execute_query(query, (isbn,))
        return {"message": f"Book with ISBN {isbn} deleted successfully."}


# Create the database proxy
db_proxy = DatabaseProxy("books.db")

# Create the BookAPI instance using the proxy
book_api = BookAPI(db_proxy)

# API Usage Examples:
print(book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803"))
print(book_api.get_book("978-0345391803"))
print(book_api.update_book("978-0345391803", author="Douglas Noel Adams"))
print(book_api.get_book("978-0345391803"))
print(book_api.delete_book("978-0345391803"))
print(book_api.get_book("978-0345391803"))

# Close the database connection
db_proxy.disconnect()