# tests/test_in_memory_storage.py

import pytest
from storage.in_memory_storage import InMemoryStorage

@pytest.fixture
def storage():
    return InMemoryStorage()

def test_set_and_get(storage):
    storage.set("key1", "value1")
    assert storage.get("key1") == "value1"

def test_get_nonexistent_key(storage):
    assert storage.get("nonexistent") is None

def test_exists(storage):
    storage.set("key1", "value1")
    assert storage.exists("key1") == True
    assert storage.exists("nonexistent") == False

def test_remove(storage):
    storage.set("key1", "value1")
    storage.remove("key1")
    assert storage.exists("key1") == False

def test_remove_nonexistent_key(storage):
    storage.remove("nonexistent")  # Should not raise an exception

def test_clear(storage):
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    storage.clear()
    assert storage.exists("key1") == False
    assert storage.exists("key2") == False