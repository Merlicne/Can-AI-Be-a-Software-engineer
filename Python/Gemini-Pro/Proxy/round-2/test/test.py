import pytest
import sqlite3
from your_module import BookAPI, DatabaseProxy  # Replace 'your_module' with the actual module name

@pytest.fixture
def db_file():
    """Fixture to manage the test database file."""
    db_file = "test_books.db"
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
    yield db_file
    # Delete the test database after tests
    try:
        os.remove(db_file)
    except FileNotFoundError:
        pass

def test_create_book(db_file):
    """Test successful book creation with valid data."""
    book_api = BookAPI(db_file)
    result = book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802")
    assert result is not None

def test_create_book_duplicate_isbn(db_file):
    """Test handling of duplicate ISBN errors."""
    book_api = BookAPI(db_file)
    book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802")
    with pytest.raises(sqlite3.IntegrityError):
        book_api.create_book("The Restaurant at the End of the Universe", "Douglas Adams", "0345391802")

def test_get_book(db_file):
    """Test retrieving an existing book with a valid ISBN."""
    book_api = BookAPI(db_file)
    book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802")
    result = book_api.get_book("0345391802")
    assert result is not None
    assert len(result) == 1
    assert result[0][1] == "The Hitchhiker's Guide to the Galaxy"

def test_get_book_non_existent(db_file):
    """Test behavior when trying to retrieve a non-existent book."""
    book_api = BookAPI(db_file)
    result = book_api.get_book("1234567890")
    assert result is None

def test_update_book(db_file):
    """Test updating an existing book with valid data."""
    book_api = BookAPI(db_file)
    book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802")
    result = book_api.update_book("0345391802", "The Restaurant at the End of the Universe", "Douglas Adams")
    assert result is not None

def test_update_book_non_existent(db_file):
    """Test handling of updates for non-existent books."""
    book_api = BookAPI(db_file)
    result = book_api.update_book("1234567890", "The Restaurant at the End of the Universe", "Douglas Adams")
    assert result is None

def test_delete_book(db_file):
    """Test deleting an existing book with a valid ISBN."""
    book_api = BookAPI(db_file)
    book_api.create_book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802")
    result = book_api.delete_book("0345391802")
    assert result is not None

def test_delete_book_non_existent(db_file):
    """Test handling of deletions for non-existent books."""
    book_api = BookAPI(db_file)
    result = book_api.delete_book("1234567890")
    assert result is None

def test_database_proxy_connection(db_file):
    """Test successful connection and disconnection to the database."""
    db_proxy = DatabaseProxy(db_file)
    with db_proxy as db:
        assert db.conn is not None
    assert db.conn is None

def test_database_proxy_execute_valid_query(db_file):
    """Test successful execution of a valid query."""
    db_proxy = DatabaseProxy(db_file)
    with db_proxy as db:
        query = "SELECT * FROM books"
        result = db.execute(query)
        assert result is not None

def test_database_proxy_execute_invalid_query(db_file):
    """Test handling of invalid SQL queries."""
    db_proxy = DatabaseProxy(db_file)
    with db_proxy as db:
        query = "INVALID SQL"
        with pytest.raises(sqlite3.OperationalError):
            db.execute(query)

def test_database_proxy_validate_insert(db_file):
    """Test data validation for INSERT queries."""
    db_proxy = DatabaseProxy(db_file)
    with db_proxy as db:
        # Test valid data
        db.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", 
                   ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "0345391802"))
        # Test invalid data (missing ISBN)
        with pytest.raises(Exception):
            db.execute("INSERT INTO books (title, author) VALUES (?, ?)", 
                       ("The Restaurant at the End of the Universe", "Douglas Adams"))

def test_database_proxy_error_handling(db_file):
    """Test error handling mechanisms for database interactions."""
    db_proxy = DatabaseProxy(db_file)
    with db_proxy as db:
        # Test non-existent table
        with pytest.raises(sqlite3.OperationalError):
            db.execute("SELECT * FROM non_existent_table")
        # Test invalid query syntax
        with pytest.raises(sqlite3.OperationalError):
            db.execute("SELECT * FROM books WHERE")