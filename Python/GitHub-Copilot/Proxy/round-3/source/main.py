# Import necessary modules
from flask import Flask, request, jsonify
import sqlite3
import logging

# Initialize Flask app
app = Flask(__name__)

# Real Subject Class
class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, data TEXT)''')
        self.conn.commit()

    def add_record(self, data):
        self.cursor.execute('INSERT INTO records (data) VALUES (?)', (data,))
        self.conn.commit()

    def fetch_records(self):
        self.cursor.execute('SELECT * FROM records')
        return self.cursor.fetchall()

    def update_record(self, record_id, data):
        self.cursor.execute('UPDATE records SET data = ? WHERE id = ?', (data, record_id))
        self.conn.commit()

    def delete_record(self, record_id):
        self.cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

# Proxy Class
class DatabaseProxy:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)
        logging.basicConfig(level=logging.INFO)

    def connect(self):
        logging.info("Connecting to database")
        self.db_manager.connect()

    def create(self, data):
        logging.info(f"Creating record: {data}")
        self.db_manager.add_record(data)

    def read(self):
        logging.info("Reading records")
        return self.db_manager.fetch_records()

    def update(self, record_id, data):
        logging.info(f"Updating record {record_id} with data: {data}")
        self.db_manager.update_record(record_id, data)

    def delete(self, record_id):
        logging.info(f"Deleting record {record_id}")
        self.db_manager.delete_record(record_id)

    def close(self):
        logging.info("Closing database connection")
        self.db_manager.close()

# Initialize DatabaseProxy
db_proxy = DatabaseProxy('test.db')
db_proxy.connect()
db_proxy.db_manager.create_table()

# Flask Routes
@app.route('/create', methods=['POST'])
def create():
    data = request.json['data']
    db_proxy.create(data)
    return jsonify({"message": "Record created"}), 201

@app.route('/read', methods=['GET'])
def read():
    records = db_proxy.read()
    return jsonify(records), 200

@app.route('/update', methods=['PUT'])
def update():
    record_id = request.json['id']
    data = request.json['data']
    db_proxy.update(record_id, data)
    return jsonify({"message": "Record updated"}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    record_id = request.json['id']
    db_proxy.delete(record_id)
    return jsonify({"message": "Record deleted"}), 200

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)