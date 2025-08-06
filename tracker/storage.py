import sqlite3
import os
from datetime import datetime

DB_PATH = "storage/activity_logs.db"

class Storage:
    def __init__(self):
        # Create tracker directory if it doesn't exist
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                app_name TEXT,
                idle_time INTEGER,
                mouse_activity INTEGER,
                keyboard_activity INTEGER,
                predicted_label TEXT
            )
        ''')
        self.conn.commit()

    def insert_record(self, record):
        self.conn.execute('''
            INSERT INTO activity_log (
                timestamp, app_name, idle_time,
                mouse_activity, keyboard_activity, predicted_label
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            record['timestamp'], record['app_name'], record['idle_time'],
            int(record['mouse_activity']), int(record['keyboard_activity']),
            record['predicted_label']
        ))
        self.conn.commit()

    def get_all_records(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM activity_log")
        return cur.fetchall()
