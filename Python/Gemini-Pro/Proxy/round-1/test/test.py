import sqlite3
import pytest

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))

from main import DatabaseProxy, BookAPI  # Replace your_module

# --- Fixtures (optional) ---
@pytest.fixture
def db_path():
    return "test_books.db"  # Use a separate test database

@pytest.fixture
def db_proxy(db_path):
    with DatabaseProxy(db_path) as proxy:
        yield proxy

@pytest.fixture
def book_api(db_proxy):
    return BookAPI(db_proxy)

# --- Test DatabaseProxy ---
def test_database_proxy_connection(db_path):
    with DatabaseProxy(db_path) as db_proxy:
        assert db_proxy.connection is not None

def test_database_proxy_disconnection(db_path):
    db_proxy = DatabaseProxy(db_path)
    db_proxy.connect()
    db_proxy.disconnect()
    assert db_proxy.connection is None

# Add more tests for data validation and error handling within DatabaseProxy

# --- Test BookAPI ---
def test_create_book_successful(book_api):
    book_api.create_book("The Lord of the Rings", "J.R.R. Tolkien", "978-0618053277")
    assert book_api.get_book("978-0618053277") is not None

def test_create_book_duplicate_isbn(book_api):
    book_api.create_book("The Hobbit", "J.R.R. Tolkien", "978-0618053277")
    with pytest.raises(sqlite3.IntegrityError):
        book_api.create_book("The Hobbit", "J.R.R. Tolkien", "978-0618053277")

def test_get_book_existing(book_api):
    book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "978-0345391803")
    book = book_api.get_book("978-0345391803")
    assert book[1] == "The Hitchhiker's Guide to the Galaxy"

def test_get_book_nonexistent(book_api):
    book = book_api.get_book("978-0000000000")
    assert book is None 

def test_update_book_existing(book_api):
    book_api.create_book("1984", "George Orwell", "978-0451524935")
    book_api.update_book("978-0451524935", title="Nineteen Eighty-Four")
    book = book_api.get_book("978-0451524935")
    assert book[1] == "Nineteen Eighty-Four"

def test_update_book_nonexistent(book_api):
    # No need for assert, just checking for no errors
    book_api.update_book("978-1111111111", title="Test") 

def test_delete_book_existing(book_api):
    book_api.create_book("Pride and Prejudice", "Jane Austen", "978-0141439518")
    book_api.delete_book("978-0141439518")
    assert book_api.get_book("978-0141439518") is None 

def test_delete_book_nonexistent(book_api):
     # No need for assert, just checking for no errors
    book_api.delete_book("978-2222222222")

# --- Run Tests ---
if __name__ == "__main__":
    pytest.main()