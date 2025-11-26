import sqlite3
import pytest # type: ignore

# --- Fixture: створюємо БД у пам’яті для кожного тесту ---
@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Таблиця користувачів
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        age INTEGER
    )
    """)

    # Таблиця постів
    cursor.execute("""
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    yield conn
    conn.close()

# -----------------------
# 1. Create User
# -----------------------
def test_create_user(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
    db.commit()
    cursor.execute("SELECT * FROM users WHERE name=?", ("Alice",))
    user = cursor.fetchone()
    assert user[1] == "Alice"
    assert user[2] == 25

# -----------------------
# 2. Read User
# -----------------------
def test_read_user(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))
    db.commit()
    cursor.execute("SELECT * FROM users WHERE name=?", ("Bob",))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "Bob"

# -----------------------
# 3. Update User
# -----------------------
def test_update_user(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Charlie", 22))
    db.commit()
    cursor.execute("UPDATE users SET age=? WHERE name=?", (23, "Charlie"))
    db.commit()
    cursor.execute("SELECT age FROM users WHERE name=?", ("Charlie",))
    age = cursor.fetchone()[0]
    assert age == 23

# -----------------------
# 4. Delete User
# -----------------------
def test_delete_user(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Dave", 40))
    db.commit()
    cursor.execute("DELETE FROM users WHERE name=?", ("Dave",))
    db.commit()
    cursor.execute("SELECT * FROM users WHERE name=?", ("Dave",))
    assert cursor.fetchone() is None

# -----------------------
# 5. UNIQUE Constraint
# -----------------------
def test_unique_constraint(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Eve", 28))
    db.commit()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Eve", 30))
        db.commit()

# -----------------------
# 6. NOT NULL Constraint
# -----------------------
def test_not_null_constraint(db):
    cursor = db.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO users (name) VALUES (?)", (None,))
        db.commit()

# -----------------------
# 7. FOREIGN KEY Constraint
# -----------------------
def test_foreign_key_constraint(db):
    cursor = db.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (999, "Invalid Post"))
        db.commit()

# -----------------------
# 8. JOIN query
# -----------------------
def test_join_query(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Frank", 35))
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (user_id, "Frank's Post"))
    db.commit()
    cursor.execute("""
    SELECT users.name, posts.title 
    FROM users JOIN posts ON users.id = posts.user_id
    WHERE users.name=?
    """, ("Frank",))
    result = cursor.fetchone()
    assert result == ("Frank", "Frank's Post")

# -----------------------
# 9. GROUP BY + Aggregation
# -----------------------
def test_group_by(db):
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("George", 20))
    uid1 = cursor.lastrowid
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Helen", 25))
    uid2 = cursor.lastrowid
    cursor.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (uid1, "Post1"))
    cursor.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (uid1, "Post2"))
    cursor.execute("INSERT INTO posts (user_id, title) VALUES (?, ?)", (uid2, "Post3"))
    db.commit()
    cursor.execute("SELECT user_id, COUNT(*) FROM posts GROUP BY user_id")
    results = dict(cursor.fetchall())
    assert results[uid1] == 2
    assert results[uid2] == 1

# -----------------------
# 10. Transaction commit/rollback
# -----------------------
def test_transaction_commit_rollback(db):
    cursor = db.cursor()
    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Ivy", 33))
        db.commit()
        cursor.execute("SELECT * FROM users WHERE name=?", ("Ivy",))
        user = cursor.fetchone()
        assert user[1] == "Ivy"

        # Rollback частина
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Jack", 28))
        raise Exception("Simulate error")
        db.commit()
    except:
        db.rollback()

    cursor.execute("SELECT * FROM users WHERE name=?", ("Jack",))
    assert cursor.fetchone() is None
