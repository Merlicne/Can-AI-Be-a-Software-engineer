from abc import ABC, abstractmethod
import sqlite3
import mysql.connector
import psycopg2

class DatabaseStrategy(ABC):
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def execute(self, query, params=None):
        pass

class SQLiteStrategy(DatabaseStrategy):
    def connect(self, **kwargs):
        return sqlite3.connect(kwargs['db_name'])

    def execute(self, connection, query, params=None):
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        return cursor

class MySQLStrategy(DatabaseStrategy):
    def connect(self, **kwargs):
        return mysql.connector.connect(**kwargs)

    def execute(self, connection, query, params=None):
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        return cursor

class PostgreSQLStrategy(DatabaseStrategy):
    def connect(self, **kwargs):
        return psycopg2.connect(**kwargs)

    def execute(self, connection, query, params=None):
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        return cursor

class RealDatabase(DatabaseInterface):
    def __init__(self, strategy: DatabaseStrategy, **kwargs):
        self.strategy = strategy
        self.connection_params = kwargs
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = self.strategy.connect(**self.connection_params)
        return self.connection

    # Implement CRUD methods using self.strategy.execute()
    # ...

# Usage
sqlite_db = RealDatabase(SQLiteStrategy(), db_name="users.db")
mysql_db = RealDatabase(MySQLStrategy(), host="localhost", user="root", password="password", database="users")
postgres_db = RealDatabase(PostgreSQLStrategy(), host="localhost", user="postgres", password="password", dbname="users")

proxy_sqlite = DatabaseProxy(sqlite_db)
proxy_mysql = DatabaseProxy(mysql_db)
proxy_postgres = DatabaseProxy(postgres_db)