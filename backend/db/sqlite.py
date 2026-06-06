import sqlite3

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
    with sqlite3.connect("my_database.db") as connection:
        cursor = connection.cursor()

        query = """
        
        """


def save_user(user_id, profile)