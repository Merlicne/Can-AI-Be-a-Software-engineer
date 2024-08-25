from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'products.db'


# Database Proxy class
class DatabaseProxy:
    def __init__(self, db_name):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def get_all_products(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            return products

    def get_product_by_id(self, product_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
            product = cursor.fetchone()
            return product

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


# Initialize DatabaseProxy
db_proxy = DatabaseProxy(DATABASE)


# Create the products table if it doesn't exist
def create_table():
    with db_proxy._connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')


create_table()


# API Endpoints
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = db_proxy.get_all_products()
        return jsonify([{'id': p[0], 'name': p[1], 'price': p[2]} for p in products])

    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        product_id = db_proxy.add_product(name, price)
        return jsonify({'message': 'Product added successfully', 'id': product_id}), 201


@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    if request.method == 'GET':
        product = db_proxy.get_product_by_id(product_id)
        if product:
            return jsonify({'id': product[0], 'name': product[1], 'price': product[2]})
        else:
            return jsonify({'message': 'Product not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        updated = db_proxy.update_product(product_id, name, price)
        if updated:
            return jsonify({'message': 'Product updated successfully'})
        else:
            return jsonify({'message': 'Product not found'}), 404

    if request.method == 'DELETE':
        deleted = db_proxy.delete_product(product_id)
        if deleted:
            return jsonify({'message': 'Product deleted successfully'})
        else:
            return jsonify({'message': 'Product not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)