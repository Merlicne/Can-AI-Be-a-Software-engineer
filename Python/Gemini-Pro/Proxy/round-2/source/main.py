from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = 'products.db'


# Database Proxy class
class DatabaseProxy:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=None):
        with self.connect() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor

    # Database operations using the Proxy methods

    def get_products(self):
        cursor = self.execute_query("SELECT * FROM products")
        products = [{'id': row[0], 'name': row[1], 'price': row[2]} for row in cursor.fetchall()]
        return products

    def get_product(self, product_id):
        cursor = self.execute_query("SELECT * FROM products WHERE id=?", (product_id,))
        row = cursor.fetchone()
        if row:
            return {'id': row[0], 'name': row[1], 'price': row[2]}
        return None

    def add_product(self, name, price):
        self.execute_query("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        return self.get_products()[-1]  # Return the newly added product

    def update_product(self, product_id, name, price):
        self.execute_query("UPDATE products SET name=?, price=? WHERE id=?", (name, price, product_id))
        return self.get_product(product_id)

    def delete_product(self, product_id):
        self.execute_query("DELETE FROM products WHERE id=?", (product_id,))
        return {'message': f'Product with id {product_id} deleted successfully'}


# Create an instance of the DatabaseProxy
db_proxy = DatabaseProxy(DATABASE)


# Create the database table if it doesn't exist
def create_table():
    with db_proxy.connect() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')


# Create the table on application startup
create_table()


# API endpoints
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        return jsonify(db_proxy.get_products())
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        new_product = db_proxy.add_product(name, price)
        return jsonify(new_product), 201


@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product(product_id):
    if request.method == 'GET':
        product = db_proxy.get_product(product_id)
        if product:
            return jsonify(product)
        return jsonify({'message': 'Product not found'}), 404
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        updated_product = db_proxy.update_product(product_id, name, price)
        return jsonify(updated_product)
    if request.method == 'DELETE':
        return jsonify(db_proxy.delete_product(product_id))


if __name__ == '__main__':
    app.run(debug=True)