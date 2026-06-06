import sqlite3
import json
import time

def init_db():
    with sqlite3.connect("my_database.db") as connection:
        cursor = connection.cursor()

        # create users table
        # completed_courses - JSON string
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            major TEXT NOT NULL,
            catalog_year INTEGER,
            target_graduation INTEGER,
            completed_courses TEXT
        );
        """
        cursor.execute(create_table_query)

        # create sessions table
        # messages - JSON string
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            timestamp INTEGER,
            messages TEXT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()

def get_user(user_id):
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "user_id": row[0],
            "major": row[1],
            "catalog_year": row[2],
            "target_graduation": row[3],
            "completed_courses": json.loads(row[4])
        }

def save_user(user_id, profile):
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users 
            (user_id, major, catalog_year, target_graduation, completed_courses)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            profile["major"],
            profile["catalog_year"],
            profile["target_graduation"],
            json.dumps(profile["completed_courses"])
        ))
        conn.commit()

def save_session(user_id, messages):
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions
            (user_id, timestamp, messages)
            VALUES (?, ?, ?)
        """, (
            user_id,
            int(time.time()),
            json.dumps(messages)
        ))
        conn.commit()

def get_recent_sessions(user_id, limit=3):
    with sqlite3.connect("my_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT messages FROM sessions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        rows = cursor.fetchall()
        return [json.loads(row[0]) for row in rows]

