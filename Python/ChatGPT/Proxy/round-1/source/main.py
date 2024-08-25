import sqlite3

class DatabaseProxy:
    def __init__(self, db_name):
        self.db_name = db_name
        self._db_manager = DatabaseManager(db_name)

    def connect(self):
        print("Proxy: Connecting to the database...")
        return self._db_manager.connect()

    def create_table(self):
        print("Proxy: Creating a table...")
        return self._db_manager.create_table()

    def add_record(self, data):
        print("Proxy: Adding a record...")
        return self._db_manager.add_record(data)

    def fetch_records(self):
        print("Proxy: Fetching records...")
        return self._db_manager.fetch_records()

    def update_record(self, record_id, data):
        print("Proxy: Updating a record...")
        return self._db_manager.update_record(record_id, data)

    def delete_record(self, record_id):
        print("Proxy: Deleting a record...")
        return self._db_manager.delete_record(record_id)

    def close(self):
        print("Proxy: Closing the database connection...")
        return self._db_manager.close()


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value TEXT
            )
        ''')
        self.connection.commit()

    def add_record(self, data):
        cursor = self.connection.cursor()
        cursor.execute('INSERT INTO records (name, value) VALUES (?, ?)', data)
        self.connection.commit()
        return cursor.lastrowid

    def fetch_records(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM records')
        return cursor.fetchall()

    def update_record(self, record_id, data):
        cursor = self.connection.cursor()
        cursor.execute('UPDATE records SET name = ?, value = ? WHERE id = ?', (data[0], data[1], record_id))
        self.connection.commit()
        return cursor.rowcount

    def delete_record(self, record_id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        self.connection.commit()
        return cursor.rowcount

    def close(self):
        if self.connection:
            self.connection.close()


from flask import Flask, request, jsonify

app = Flask(__name__)
db_proxy = DatabaseProxy('test.db')

@app.route('/create', methods=['POST'])
def create():
    data = request.json
    name = data.get('name')
    value = data.get('value')
    record_id = db_proxy.add_record((name, value))
    return jsonify({"id": record_id}), 201

@app.route('/read', methods=['GET'])
def read():
    records = db_proxy.fetch_records()
    return jsonify(records), 200

@app.route('/update/<int:record_id>', methods=['PUT'])
def update(record_id):
    data = request.json
    name = data.get('name')
    value = data.get('value')
    rows_updated = db_proxy.update_record(record_id, (name, value))
    return jsonify({"rows_updated": rows_updated}), 200

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete(record_id):
    rows_deleted = db_proxy.delete_record(record_id)
    return jsonify({"rows_deleted": rows_deleted}), 200

if __name__ == '__main__':
    db_proxy.connect()
    db_proxy.create_table()
    app.run(debug=True)
