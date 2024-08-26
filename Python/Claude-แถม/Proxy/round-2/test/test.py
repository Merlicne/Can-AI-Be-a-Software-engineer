import pytest
from unittest.mock import Mock, patch
from your_module import DatabaseInterface, RealDatabase, DatabaseProxy, DatabaseStrategy

# Test fixtures
@pytest.fixture
def mock_db_strategy():
    strategy = Mock(spec=DatabaseStrategy)
    strategy.connect.return_value = Mock()
    return strategy

@pytest.fixture
def real_db(mock_db_strategy):
    return RealDatabase(mock_db_strategy, db_name="test.db")

@pytest.fixture
def db_proxy(real_db):
    return DatabaseProxy(real_db)

# Test Subject interface implementation
def test_database_interface():
    assert hasattr(RealDatabase, 'create')
    assert hasattr(RealDatabase, 'read')
    assert hasattr(RealDatabase, 'update')
    assert hasattr(RealDatabase, 'delete')

    assert hasattr(DatabaseProxy, 'create')
    assert hasattr(DatabaseProxy, 'read')
    assert hasattr(DatabaseProxy, 'update')
    assert hasattr(DatabaseProxy, 'delete')

# Test RealSubject (RealDatabase)
def test_real_database_create(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.lastrowid = 1
        result = real_db.create({"name": "John", "email": "john@example.com"})
        assert result == 1
        mock_execute.assert_called_once()

def test_real_database_read(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.fetchone.return_value = (1, "John", "john@example.com")
        result = real_db.read(1)
        assert result == {"id": 1, "name": "John", "email": "john@example.com"}
        mock_execute.assert_called_once()

def test_real_database_update(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.rowcount = 1
        result = real_db.update(1, {"name": "Jane"})
        assert result == True
        mock_execute.assert_called_once()

def test_real_database_delete(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.rowcount = 1
        result = real_db.delete(1)
        assert result == True
        mock_execute.assert_called_once()

# Test Proxy
def test_proxy_create(db_proxy):
    with patch.object(db_proxy.real_db, 'create') as mock_create:
        mock_create.return_value = 1
        result = db_proxy.create({"name": "John", "email": "john@example.com"})
        assert result == 1
        mock_create.assert_called_once()
        assert 1 in db_proxy.cache

def test_proxy_read_cache(db_proxy):
    db_proxy.cache[1] = {"id": 1, "name": "John", "email": "john@example.com"}
    result = db_proxy.read(1)
    assert result == {"id": 1, "name": "John", "email": "john@example.com"}

def test_proxy_read_db(db_proxy):
    with patch.object(db_proxy.real_db, 'read') as mock_read:
        mock_read.return_value = {"id": 1, "name": "John", "email": "john@example.com"}
        result = db_proxy.read(1)
        assert result == {"id": 1, "name": "John", "email": "john@example.com"}
        mock_read.assert_called_once()
        assert 1 in db_proxy.cache

def test_proxy_update(db_proxy):
    with patch.object(db_proxy.real_db, 'update') as mock_update:
        mock_update.return_value = True
        db_proxy.cache[1] = {"id": 1, "name": "John", "email": "john@example.com"}
        result = db_proxy.update(1, {"name": "Jane"})
        assert result == True
        mock_update.assert_called_once()
        assert db_proxy.cache[1]["name"] == "Jane"

def test_proxy_delete(db_proxy):
    with patch.object(db_proxy.real_db, 'delete') as mock_delete:
        mock_delete.return_value = True
        db_proxy.cache[1] = {"id": 1, "name": "John", "email": "john@example.com"}
        result = db_proxy.delete(1)
        assert result == True
        mock_delete.assert_called_once()
        assert 1 not in db_proxy.cache

# Negative test cases
def test_real_database_read_not_found(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.fetchone.return_value = None
        result = real_db.read(999)
        assert result == {}

def test_real_database_update_not_found(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.rowcount = 0
        result = real_db.update(999, {"name": "Jane"})
        assert result == False

def test_real_database_delete_not_found(real_db):
    with patch.object(real_db.strategy, 'execute') as mock_execute:
        mock_execute.return_value.rowcount = 0
        result = real_db.delete(999)
        assert result == False

# Edge cases
def test_proxy_create_invalid_data(db_proxy):
    with pytest.raises(ValueError):
        db_proxy.create({})

def test_proxy_read_invalid_id(db_proxy):
    with pytest.raises(ValueError):
        db_proxy.read(-1)

# Test database strategy
def test_database_strategy():
    strategy = DatabaseStrategy()
    with pytest.raises(NotImplementedError):
        strategy.connect()
    with pytest.raises(NotImplementedError):
        strategy.execute(None, "SELECT * FROM users")

# Test specific database strategies
def test_sqlite_strategy():
    with patch('sqlite3.connect') as mock_connect:
        strategy = SQLiteStrategy()
        conn = strategy.connect(db_name="test.db")
        mock_connect.assert_called_once_with("test.db")

def test_mysql_strategy():
    with patch('mysql.connector.connect') as mock_connect:
        strategy = MySQLStrategy()
        conn = strategy.connect(host="localhost", user="root", password="password", database="testdb")
        mock_connect.assert_called_once_with(
            host="localhost", user="root", password="password", database="testdb"
        )

def test_postgresql_strategy():
    with patch('psycopg2.connect') as mock_connect:
        strategy = PostgreSQLStrategy()
        conn = strategy.connect(host="localhost", user="postgres", password="password", dbname="testdb")
        mock_connect.assert_called_once_with(
            host="localhost", user="postgres", password="password", dbname="testdb"
        )

if __name__ == "__main__":
    pytest.main(["-v", "--cov=your_module", "--cov-report=term-missing"])