from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'products.db'


# Database Proxy Class
class DatabaseProxy:
    def __init__(self, db_name):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def get_products(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            return [{'id': row[0], 'name': row[1], 'price': row[2]} for row in rows]

    def get_product(self, product_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
            row = cursor.fetchone()
            if row:
                return {'id': row[0], 'name': row[1], 'price': row[2]}
            return None

    def add_product(self, name, price):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            conn.commit()
            return cursor.lastrowid

    def update_product(self, product_id, name, price):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name=?, price=? WHERE id=?", (name, price, product_id))
            conn.commit()
            return cursor.rowcount

    def delete_product(self, product_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            return cursor.rowcount


# Create an instance of the DatabaseProxy
db_proxy = DatabaseProxy(DATABASE)

# Create the database table if it doesn't exist
with db_proxy._connect() as conn:
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        '''
    )


# API Endpoints
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = db_proxy.get_products()
        return jsonify(products)

    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        if name and price:
            product_id = db_proxy.add_product(name, price)
            return jsonify({'message': 'Product added successfully', 'id': product_id}), 201
        return jsonify({'error': 'Invalid data'}), 400


@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    if request.method == 'GET':
        product = db_proxy.get_product(product_id)
        if product:
            return jsonify(product)
        return jsonify({'error': 'Product not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        if name and price:
            rows_updated = db_proxy.update_product(product_id, name, price)
            if rows_updated > 0:
                return jsonify({'message': 'Product updated successfully'})
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'error': 'Invalid data'}), 400

    if request.method == 'DELETE':
        rows_deleted = db_proxy.delete_product(product_id)
        if rows_deleted > 0:
            return jsonify({'message': 'Product deleted successfully'})
        return jsonify({'error': 'Product not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)