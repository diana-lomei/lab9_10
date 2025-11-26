from src.database.models.user_model import User
import sqlite3

class UserRepository:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                age INTEGER
            )
        """)
        self.conn.commit()

    def create(self, name, age):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        self.conn.commit()
        return User(cursor.lastrowid, name, age).to_dict()

    def get(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(*row).to_dict()
        return None

    def update(self, user_id, name, age):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (name, age, user_id))
        self.conn.commit()
        return self.get(user_id)

    def delete(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
