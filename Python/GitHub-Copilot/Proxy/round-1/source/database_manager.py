# database_manager.py
import sqlite3

class DatabaseManager:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                data TEXT NOT NULL)''')
            conn.commit()

    def add_record(self, data):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO records (data) VALUES (?)', (data,))
            conn.commit()

    def fetch_records(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM records')
            return cursor.fetchall()

    def update_record(self, record_id, data):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE records SET data = ? WHERE id = ?', (data, record_id))
            conn.commit()

    def delete_record(self, record_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()