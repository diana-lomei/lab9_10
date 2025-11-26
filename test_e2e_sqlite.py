import sqlite3
from playwright.sync_api import sync_playwright

# --- SQLite база ---
conn = sqlite3.connect("test_db.sqlite")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")
cursor.execute("INSERT INTO users (name) VALUES (?)", ("Diana",))
conn.commit()
cursor.execute("SELECT * FROM users")
print("Users from DB:", cursor.fetchall())
conn.close()

# --- Playwright тест ---
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    print("Page title:", page.title())
    browser.close()
