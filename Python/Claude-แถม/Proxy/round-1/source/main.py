import sqlite3
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Step 2: Create the main interface (Subject) for basic CRUD operations
class DatabaseInterface(ABC):
    @abstractmethod
    def create(self, table: str, data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def read(self, table: str, id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, table: str, id: int, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self, table: str, id: int) -> bool:
        pass

# Step 3: Implement a RealSubject class
class RealDatabase(DatabaseInterface):
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create(self, table: str, data: Dict[str, Any]) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, list(data.values()))
        conn.commit()
        return cursor.lastrowid

    def read(self, table: str, id: int) -> Dict[str, Any]:
        conn = self.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table} WHERE id = ?"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return {}

    def update(self, table: str, id: int, data: Dict[str, Any]) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        values = list(data.values()) + [id]
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount > 0

    def delete(self, table: str, id: int) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        query = f"DELETE FROM {table} WHERE id = ?"
        cursor.execute(query, (id,))
        conn.commit()
        return cursor.rowcount > 0

# Step 4: Develop a Proxy class
class DatabaseProxy(DatabaseInterface):
    def __init__(self, real_database: RealDatabase):
        self.real_database = real_database
        self.cache = {}

    def create(self, table: str, data: Dict[str, Any]) -> int:
        print(f"Logging: Creating new record in {table}")
        id = self.real_database.create(table, data)
        self.cache[f"{table}_{id}"] = data
        return id

    def read(self, table: str, id: int) -> Dict[str, Any]:
        cache_key = f"{table}_{id}"
        if cache_key in self.cache:
            print(f"Logging: Reading from cache for {table} with id {id}")
            return self.cache[cache_key]
        print(f"Logging: Reading from database for {table} with id {id}")
        data = self.real_database.read(table, id)
        self.cache[cache_key] = data
        return data

    def update(self, table: str, id: int, data: Dict[str, Any]) -> bool:
        print(f"Logging: Updating record in {table} with id {id}")
        success = self.real_database.update(table, id, data)
        if success:
            self.cache[f"{table}_{id}"] = data
        return success

    def delete(self, table: str, id: int) -> bool:
        print(f"Logging: Deleting record from {table} with id {id}")
        success = self.real_database.delete(table, id)
        if success:
            self.cache.pop(f"{table}_{id}", None)
        return success

# Example usage
if __name__ == "__main__":
    # Initialize the RealDatabase and DatabaseProxy
    real_db = RealDatabase("example.db")
    db_proxy = DatabaseProxy(real_db)

    # Create a table (this would typically be done separately)
    real_db.connect().execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Create
    user_id = db_proxy.create("users", {"name": "John Doe", "email": "john@example.com"})
    print(f"Created user with ID: {user_id}")

    # Read
    user = db_proxy.read("users", user_id)
    print(f"Read user: {user}")

    # Update
    db_proxy.update("users", user_id, {"name": "Jane Doe", "email": "jane@example.com"})
    updated_user = db_proxy.read("users", user_id)
    print(f"Updated user: {updated_user}")

    # Delete
    deleted = db_proxy.delete("users", user_id)
    print(f"User deleted: {deleted}")

    # Close the database connection
    real_db.close()