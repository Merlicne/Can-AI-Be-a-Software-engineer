import pytest
from unittest.mock import MagicMock
from database_proxy import DatabaseProxy
from database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    return MagicMock(DatabaseManager)

@pytest.fixture
def db_proxy(db_manager):
    return DatabaseProxy(db_manager)

def test_proxy_create_table(db_proxy, db_manager):
    db_proxy.create_table()
    db_manager.create_table.assert_called_once()

def test_proxy_add_record(db_proxy, db_manager):
    db_proxy.add_record('test data')
    db_manager.add_record.assert_called_once_with('test data')

def test_proxy_fetch_records(db_proxy, db_manager):
    db_manager.fetch_records.return_value = [('test data',)]
    records = db_proxy.fetch_records()
    db_manager.fetch_records.assert_called_once()
    assert records == [('test data',)]

def test_proxy_update_record(db_proxy, db_manager):
    db_proxy.update_record(1, 'updated data')
    db_manager.update_record.assert_called_once_with(1, 'updated data')

def test_proxy_delete_record(db_proxy, db_manager):
    db_proxy.delete_record(1)
    db_manager.delete_record.assert_called_once_with(1)