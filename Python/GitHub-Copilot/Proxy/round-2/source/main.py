# app.py
from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)

# Real Subject Class
class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS records
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              data TEXT NOT NULL);''')

    def close(self):
        if self.conn:
            self.conn.close()

    def add_record(self, data):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO records (data) VALUES (?)", (data,))
        self.conn.commit()
        return cursor.lastrowid

    def fetch_records(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM records")
        return cursor.fetchall()

    def update_record(self, record_id, data):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE records SET data = ? WHERE id = ?", (data, record_id))
        self.conn.commit()
        return cursor.rowcount

    def delete_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        self.conn.commit()
        return cursor.rowcount

# Proxy Class
class DatabaseProxy:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)
        self.db_manager.connect()
        logging.basicConfig(level=logging.INFO)

    def __del__(self):
        self.db_manager.close()

    def add_record(self, data):
        logging.info(f"Adding record: {data}")
        return self.db_manager.add_record(data)

    def fetch_records(self):
        logging.info("Fetching records")
        return self.db_manager.fetch_records()

    def update_record(self, record_id, data):
        logging.info(f"Updating record {record_id} with data: {data}")
        return self.db_manager.update_record(record_id, data)

    def delete_record(self, record_id):
        logging.info(f"Deleting record {record_id}")
        return self.db_manager.delete_record(record_id)

# Initialize Proxy
db_proxy = DatabaseProxy('test.db')

# Flask Routes
@app.route('/create', methods=['POST'])
def create():
    data = request.json['data']
    record_id = db_proxy.add_record(data)
    return jsonify({'id': record_id}), 201

@app.route('/read', methods=['GET'])
def read():
    records = db_proxy.fetch_records()
    return jsonify(records), 200

@app.route('/update', methods=['PUT'])
def update():
    record_id = request.json['id']
    data = request.json['data']
    rows_updated = db_proxy.update_record(record_id, data)
    return jsonify({'rows_updated': rows_updated}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    record_id = request.json['id']
    rows_deleted = db_proxy.delete_record(record_id)
    return jsonify({'rows_deleted': rows_deleted}), 200

if __name__ == '__main__':
    app.run(debug=True)