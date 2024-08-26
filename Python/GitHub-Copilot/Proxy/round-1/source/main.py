# app.py
from flask import Flask, request, jsonify
from database_proxy import DatabaseProxy
from database_manager import DatabaseManager

app = Flask(__name__)
db_manager = DatabaseManager()
db_proxy = DatabaseProxy(db_manager)

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
    db_proxy.create_table()
    app.run(debug=True)