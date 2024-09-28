import sqlite3
import logging
from flask import Flask, request, jsonify

class DatabaseProxy:
    def __init__(self, database_manager):
        self._database_manager = database_manager

    def execute(self, query, params=None):
        logging.info(f"Executing query: {query} | Params: {params}")
        result = self._database_manager.execute(query, params)
        logging.info(f"Query Result: {result}")
        return result

    def fetchall(self, query, params=None):
        logging.info(f"Fetching all records with query: {query} | Params: {params}")
        result = self._database_manager.fetchall(query, params)
        logging.info(f"Fetch All Result: {result}")
        return result

    def fetchone(self, query, params=None):
        logging.info(f"Fetching one record with query: {query} | Params: {params}")
        result = self._database_manager.fetchone(query, params)
        logging.info(f"Fetch One Result: {result}")
        return result


class DatabaseManager:
    def __init__(self, db_name="database.db"):
        self._db_name = db_name

    def connect(self):
        return sqlite3.connect(self._db_name)

    def execute(self, query, params=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid

    def fetchall(self, query, params=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def fetchone(self, query, params=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()


app = Flask(__name__)

# Initialize the DatabaseManager and Proxy
db_manager = DatabaseManager()
db_proxy = DatabaseProxy(db_manager)

def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        value TEXT NOT NULL
    );
    """
    db_proxy.execute(create_table_query)

# Call create_table explicitly before starting the app
create_table()

# POST /create
@app.route('/create', methods=['POST'])
def create_record():
    data = request.json
    query = "INSERT INTO records (name, value) VALUES (?, ?)"
    params = (data['name'], data['value'])
    record_id = db_proxy.execute(query, params)
    return jsonify({"id": record_id}), 201

# GET /read
@app.route('/read', methods=['GET'])
def read_records():
    query = "SELECT * FROM records"
    records = db_proxy.fetchall(query)
    return jsonify(records), 200

# PUT /update/<int:id>
@app.route('/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.json
    query = "UPDATE records SET name = ?, value = ? WHERE id = ?"
    params = (data['name'], data['value'], id)
    db_proxy.execute(query, params)
    return jsonify({"message": "Record updated"}), 200

# DELETE /delete/<int:id>
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    query = "DELETE FROM records WHERE id = ?"
    params = (id,)
    db_proxy.execute(query, params)
    return jsonify({"message": "Record deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
