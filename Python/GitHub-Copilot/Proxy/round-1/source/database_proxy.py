# database_proxy.py
import sqlite3
import logging

class DatabaseProxy:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        logging.basicConfig(level=logging.INFO)

    def create_table(self):
        logging.info("Creating table...")
        self.db_manager.create_table()

    def add_record(self, data):
        logging.info(f"Adding record: {data}")
        self.db_manager.add_record(data)

    def fetch_records(self):
        logging.info("Fetching records...")
        return self.db_manager.fetch_records()

    def update_record(self, record_id, data):
        logging.info(f"Updating record {record_id} with data: {data}")
        self.db_manager.update_record(record_id, data)

    def delete_record(self, record_id):
        logging.info(f"Deleting record {record_id}")
        self.db_manager.delete_record(record_id)