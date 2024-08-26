import sqlite3
import logging

class DatabaseProxy:
    def __init__(self, real_subject):
        self._real_subject = real_subject
        self._cache = {}

    def create_table(self):
        self._log("Creating table")
        return self._real_subject.create_table()

    def add_record(self, data):
        self._log(f"Adding record: {data}")
        return self._real_subject.add_record(data)

    def fetch_records(self):
        self._log("Fetching records")
        if "fetch_records" in self._cache:
            self._log("Returning cached records")
            return self._cache["fetch_records"]

        records = self._real_subject.fetch_records()
        self._cache["fetch_records"] = records
        return records

    def update_record(self, record_id, data):
        self._log(f"Updating record with ID {record_id}: {data}")
        if "fetch_records" in self._cache:
            del self._cache["fetch_records"]
        return self._real_subject.update_record(record_id, data)

    def delete_record(self, record_id):
        self._log(f"Deleting record with ID {record_id}")
        if "fetch_records" in self._cache:
            del self._cache["fetch_records"]
        return self._real_subject.delete_record(record_id)

    def _log(self, message):
        logging.info(f"DatabaseProxy: {message}")

class DatabaseManager:
    def __init__(self, db_name):
        self._db_name = db_name

    def _connect(self):
        return sqlite3.connect(self._db_name)

    def create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY,
                    data TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_record(self, data):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO records (data) VALUES (?)', (data,))
            conn.commit()

    def fetch_records(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records')
            return cursor.fetchall()

    def update_record(self, record_id, data):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE records SET data = ? WHERE id = ?', (data, record_id))
            conn.commit()

    def delete_record(self, record_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()


from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize DatabaseManager and DatabaseProxy
db_manager = DatabaseManager('example.db')
db_proxy = DatabaseProxy(db_manager)

# Ensure the table exists
db_proxy.create_table()

@app.route('/create', methods=['POST'])
def create():
    data = request.json.get('data')
    db_proxy.add_record(data)
    return jsonify({"message": "Record added"}), 201

@app.route('/read', methods=['GET'])
def read():
    records = db_proxy.fetch_records()
    return jsonify(records), 200

@app.route('/update/<int:record_id>', methods=['PUT'])
def update(record_id):
    data = request.json.get('data')
    db_proxy.update_record(record_id, data)
    return jsonify({"message": "Record updated"}), 200

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete(record_id):
    db_proxy.delete_record(record_id)
    return jsonify({"message": "Record deleted"}), 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
