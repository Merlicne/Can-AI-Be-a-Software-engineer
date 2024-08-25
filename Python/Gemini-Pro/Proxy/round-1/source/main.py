import sqlite3

class DatabaseProxy:
    """
    Proxy class for managing database connections and interactions.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Establishes a connection to the database.
        """
        self.connection = sqlite3.connect(self.db_name)
        print(f"Connected to database: {self.db_name}")

    def disconnect(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            print(f"Disconnected from database: {self.db_name}")

    def execute_query(self, query, params=None):
        """
        Executes a given SQL query with optional parameters.
        """
        if self.connection:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.fetchall()

class BookAPI:
    """
    Main interface for interacting with book data through the Proxy.
    """
    def __init__(self, db_proxy):
        self.db_proxy = db_proxy

    def create_book(self, title, author, isbn):
        """
        Creates a new book entry in the database.
        """
        query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
        params = (title, author, isbn)
        self.db_proxy.execute_query(query, params)
        print(f"Book '{title}' by {author} added successfully.")

    def get_book(self, isbn):
        """
        Retrieves a book entry from the database based on ISBN.
        """
        query = "SELECT * FROM books WHERE isbn = ?"
        params = (isbn,)
        result = self.db_proxy.execute_query(query, params)
        if result:
            book = result[0]
            print(f"Book details: Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}")
        else:
            print(f"No book found with ISBN: {isbn}")

    def update_book(self, isbn, title=None, author=None):
        """
        Updates a book's information in the database.
        """
        query = "UPDATE books SET "
        params = []
        if title:
            query += "title = ?, "
            params.append(title)
        if author:
            query += "author = ?, "
            params.append(author)
        query = query.rstrip(", ") + " WHERE isbn = ?"
        params.append(isbn)
        self.db_proxy.execute_query(query, params)
        print(f"Book with ISBN: {isbn} updated successfully.")

    def delete_book(self, isbn):
        """
        Deletes a book entry from the database based on ISBN.
        """
        query = "DELETE FROM books WHERE isbn = ?"
        params = (isbn,)
        self.db_proxy.execute_query(query, params)
        print(f"Book with ISBN: {isbn} deleted successfully.")

# Example usage:
if __name__ == "__main__":
    db_proxy = DatabaseProxy("books.db") # Create the Proxy object
    book_api = BookAPI(db_proxy) # Inject the Proxy into the API

    with db_proxy: # Connect to the database using the Proxy
        book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803")
        book_api.get_book("978-0345391803")
        book_api.update_book("978-0345391803", author="Douglas Noel Adams")
        book_api.get_book("978-0345391803")
        book_api.delete_book("978-0345391803")