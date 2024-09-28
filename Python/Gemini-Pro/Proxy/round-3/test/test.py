import sqlite3
import pytest

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../source')))
from main import BookAPI, DatabaseProxy  # Replace your_module


@pytest.fixture(scope="function")
def db_proxy_fixture():
    """Fixture to set up and tear down the database for each test function."""
    db_name = "test_books.db"
    proxy = DatabaseProxy(db_name)
    proxy.connect()
    yield proxy
    proxy.disconnect()
    # Clean up the test database file
    import os
    os.remove(db_name)


# -------------- BookAPI tests --------------


def test_create_book_successful(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    result = api.create_book("Test Book", "Test Author", "1234567890")
    assert result == {"message": "Book with ISBN 1234567890 created successfully."}


def test_create_book_duplicate_isbn(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    api.create_book("Test Book", "Test Author", "1234567890")
    with pytest.raises(sqlite3.IntegrityError):
        api.create_book("Another Book", "Another Author", "1234567890")


def test_get_book_existing(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    api.create_book("Test Book", "Test Author", "1234567890")
    result = api.get_book("1234567890")
    assert result == {"isbn": "1234567890", "title": "Test Book", "author": "Test Author"}


def test_get_book_nonexistent(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    result = api.get_book("9876543210")
    assert result == {"message": "Book with ISBN 9876543210 not found."}


def test_update_book_existing(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    api.create_book("Test Book", "Test Author", "1234567890")
    result = api.update_book("1234567890", title="Updated Title", author="Updated Author")
    assert result == {"message": "Book with ISBN 1234567890 updated successfully."}
    updated_book = api.get_book("1234567890")
    assert updated_book == {"isbn": "1234567890", "title": "Updated Title", "author": "Updated Author"}


def test_update_book_nonexistent(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    result = api.update_book("9876543210", title="Updated Title")
    assert result == {"message": "Book with ISBN 9876543210 updated successfully."}


def test_delete_book_existing(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    api.create_book("Test Book", "Test Author", "1234567890")
    result = api.delete_book("1234567890")
    assert result == {"message": "Book with ISBN 1234567890 deleted successfully."}
    assert api.get_book("1234567890") == {"message": "Book with ISBN 1234567890 not found."}


def test_delete_book_nonexistent(db_proxy_fixture):
    api = BookAPI(db_proxy_fixture)
    result = api.delete_book("9876543210")
    assert result == {"message": "Book with ISBN 9876543210 deleted successfully."}


# -------------- DatabaseProxy tests --------------


def test_database_proxy_connection(db_proxy_fixture):
    assert db_proxy_fixture.connection is not None


def test_database_proxy_disconnection(db_proxy_fixture):
    db_proxy_fixture.disconnect()
    assert db_proxy_fixture.connection is None


def test_execute_query_with_params(db_proxy_fixture):
    db_proxy_fixture.execute_query(
        "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
        ("978-0123456789", "Test Title", "Test Author"),
    )
    result = db_proxy_fixture.execute_query("SELECT * FROM books WHERE isbn = ?", ("978-0123456789",))
    assert result[0][1] == "Test Title"  # Check if the book title matches


def test_execute_query_no_params(db_proxy_fixture):
    db_proxy_fixture.execute_query(
        "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
        ("978-0123456789", "Test Title", "Test Author"),
    )
    result = db_proxy_fixture.execute_query("SELECT * FROM books")
    assert len(result) > 0