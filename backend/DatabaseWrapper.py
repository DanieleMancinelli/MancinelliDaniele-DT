import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseWrapper:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME"),
            'port': int(os.getenv("DB_PORT")),
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.create_table()

    def connect(self):
        # Metodo per stabilire la connessione
        return pymysql.connect(**self.db_config)

    def execute_query(self, query, params=()):
        # Per operazioni di scrittura (INSERT, UPDATE, DELETE, CREATE)
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            conn.close()

    def fetch_query(self, query, params=()):
        # Per operazioni di lettura (SELECT)
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def create_table(self):
        # Query di creazione tabella come richiesto dalla traccia
        query = '''
        CREATE TABLE IF NOT EXISTS deliveries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tracking_code VARCHAR(100) NOT NULL UNIQUE,
            recipient VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            time_slot VARCHAR(100) NOT NULL,
            status VARCHAR(50) DEFAULT 'READY',
            priority VARCHAR(50) DEFAULT 'MEDIUM'
        )
        '''
        self.execute_query(query)

    # Inseriamo già i metodi che serviranno per il Commit 3, 
    # così app.py non dovrà contenere SQL.
    
    def get_all_deliveries(self):
        return self.fetch_query("SELECT * FROM deliveries")

    def add_delivery(self, tracking, recipient, address, time_slot, priority):
        query = """
            INSERT INTO deliveries (tracking_code, recipient, address, time_slot, priority)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (tracking, recipient, address, time_slot, priority)
        self.execute_query(query, params)

    def update_delivery_status(self, delivery_id, new_status):
        query = "UPDATE deliveries SET status = %s WHERE id = %s"
        params = (new_status, delivery_id)
        self.execute_query(query, params)