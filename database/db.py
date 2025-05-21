import sqlite3
from datetime import datetime

DB_NAME = 'database/shinnik.db'

def create_table():
    try:
        with sqlite3.connect(DB_NAME) as con:
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    user_name TEXT,
                    phone TEXT,
                    vehicle_type TEXT,
                    model TEXT,
                    created_at TEXT
                )
            """)
            con.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")

def insert_order(user_id, user_name, phone, vehicle_type, model):
    try:
        with sqlite3.connect(DB_NAME) as con:
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO orders (user_id, user_name, phone, vehicle_type, model, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, user_name, phone, vehicle_type, model, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            con.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении заказа: {e}")