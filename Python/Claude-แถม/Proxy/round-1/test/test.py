import pytest
from unittest.mock import Mock, patch
from your_module import DatabaseInterface, RealDatabase, DatabaseProxy, SQLiteFactory

# Mock database for testing
class MockDatabase(DatabaseInterface):
    def __init__(self):
        self.data = {}
        self.last_id = 0

    def create(self, table, data):
        self.last_id += 1
        self.data[f"{table}_{self.last_id}"] = data
        return self.last_id

    def read(self, table, id):
        return self.data.get(f"{table}_{id}", {})

    def update(self, table, id, data):
        key = f"{table}_{id}"
        if key in self.data:
            self.data[key].update(data)
            return True
        return False

    def delete(self, table, id):
        key = f"{table}_{id}"
        if key in self.data:
            del self.data[key]
            return True
        return False

@pytest.fixture
def mock_db():
    return MockDatabase()

@pytest.fixture
def db_proxy(mock_db):
    return DatabaseProxy(mock_db)

# Test Subject interface implementation
def test_database_interface():
    db = MockDatabase()
    assert isinstance(db, DatabaseInterface)
    assert hasattr(db, 'create')
    assert hasattr(db, 'read')
    assert hasattr(db, 'update')
    assert hasattr(db, 'delete')

# Test RealSubject class
@patch('sqlite3.connect')
def test_real_database(mock_connect):
    mock_connection = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 1

    db_factory = SQLiteFactory("test.db")
    db = RealDatabase(db_factory)

    # Test create
    assert db.create("users", {"name": "John", "email": "john@example.com"}) == 1
    mock_cursor.execute.assert_called()
    mock_connection.commit.assert_called()

    # Test read
    mock_cursor.fetchone.return_value = (1, "John", "john@example.com")
    mock_cursor.description = [("id",), ("name",), ("email",)]
    result = db.read("users", 1)
    assert result == {"id": 1, "name": "John", "email": "john@example.com"}

    # Test update
    assert db.update("users", 1, {"name": "Jane"})
    mock_cursor.execute.assert_called()
    mock_connection.commit.assert_called()

    # Test delete
    mock_cursor.rowcount = 1
    assert db.delete("users", 1)
    mock_cursor.execute.assert_called()
    mock_connection.commit.assert_called()

# Test Proxy class
def test_database_proxy_create(db_proxy):
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.create.return_value = 1
        result = db_proxy.create("users", {"name": "John", "email": "john@example.com"})
        assert result == 1
        mock_real_db.create.assert_called_with("users", {"name": "John", "email": "john@example.com"})
        assert db_proxy.cache["users_1"] == {"name": "John", "email": "john@example.com"}

def test_database_proxy_read(db_proxy):
    # Test cache miss
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.read.return_value = {"id": 1, "name": "John", "email": "john@example.com"}
        result = db_proxy.read("users", 1)
        assert result == {"id": 1, "name": "John", "email": "john@example.com"}
        mock_real_db.read.assert_called_with("users", 1)
        assert db_proxy.cache["users_1"] == {"id": 1, "name": "John", "email": "john@example.com"}

    # Test cache hit
    result = db_proxy.read("users", 1)
    assert result == {"id": 1, "name": "John", "email": "john@example.com"}
    mock_real_db.read.assert_called_once()  # Ensure it wasn't called again

def test_database_proxy_update(db_proxy):
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.update.return_value = True
        result = db_proxy.update("users", 1, {"name": "Jane"})
        assert result == True
        mock_real_db.update.assert_called_with("users", 1, {"name": "Jane"})
        assert db_proxy.cache["users_1"] == {"name": "Jane"}

def test_database_proxy_delete(db_proxy):
    db_proxy.cache["users_1"] = {"name": "John"}
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.delete.return_value = True
        result = db_proxy.delete("users", 1)
        assert result == True
        mock_real_db.delete.assert_called_with("users", 1)
        assert "users_1" not in db_proxy.cache

# Test error handling
def test_database_proxy_error_handling(db_proxy):
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.create.side_effect = Exception("Database error")
        with pytest.raises(Exception):
            db_proxy.create("users", {"name": "John"})

# Test edge cases
def test_database_proxy_edge_cases(db_proxy):
    # Test empty data
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.create.return_value = 1
        result = db_proxy.create("users", {})
        assert result == 1
        mock_real_db.create.assert_called_with("users", {})

    # Test non-existent record
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.read.return_value = {}
        result = db_proxy.read("users", 999)
        assert result == {}
        mock_real_db.read.assert_called_with("users", 999)

# Test additional proxy features (e.g., logging)
def test_database_proxy_logging(caplog, db_proxy):
    with patch.object(db_proxy, 'real_database') as mock_real_db:
        mock_real_db.create.return_value = 1
        db_proxy.create("users", {"name": "John"})
        assert "Creating new record in users" in caplog.text

# Test database factory
def test_sqlite_factory():
    factory = SQLiteFactory("test.db")
    with patch('sqlite3.connect') as mock_connect:
        connection = factory.create_connection()
        mock_connect.assert_called_with("test.db")
        assert connection == mock_connect.return_value

if __name__ == "__main__":
    pytest.main(["-v", "--cov=your_module", "test_crud_api.py"])