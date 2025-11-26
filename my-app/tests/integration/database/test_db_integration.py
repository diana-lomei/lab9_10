import sqlite3
import pytest 

@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        age INTEGER
    )
    """)
    conn.commit()
    yield conn
    conn.close()

def test_create_user(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
    db.commit()
    cursor.execute("SELECT * FROM users WHERE name=?", ("Alice",))
    user = cursor.fetchone()
    assert user[1] == "Alice"

def test_unique_constraint(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))
    db.commit()
    import pytest 
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 32))
        db.commit()
