from playwright.sync_api import sync_playwright

def test_user_journey():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True якщо не хочеш відкривати UI
        page = browser.new_page()
        
        try:
            # --- User Registration ---
            page.goto("file:///C:/Users/Diana/Downloads/lab8-9/index.html")  # локальна сторінка
            page.fill("#username", "testuser")
            page.fill("#password", "Password123")
            page.click("#register-btn")
            
            # Explicit wait
            page.wait_for_selector("#registration-success", timeout=5000)
            assert page.inner_text("#registration-success") == "Registration successful"
            
            # --- User Login ---
            page.fill("#login-username", "testuser")
            page.fill("#login-password", "Password123")
            page.click("#login-btn")
            page.wait_for_selector("#welcome-message", timeout=5000)
            assert "Welcome, testuser" in page.inner_text("#welcome-message")
            
            # --- CRUD: Add Item ---
            page.fill("#new-item", "Test Item")
            page.click("#add-item-btn")
            page.wait_for_selector(".item", timeout=5000)
            assert "Test Item" in page.inner_text(".item")
            
            # --- Edit Item ---
            page.click(".item-edit-btn")
            page.fill(".item-edit-input", "Updated Item")
            page.click(".item-save-btn")
            page.wait_for_selector(".item", timeout=5000)
            assert "Updated Item" in page.inner_text(".item")
            
            # --- Delete Item ---
            page.click(".item-delete-btn")
            page.wait_for_selector(".no-items", timeout=5000)
            assert "No items found" in page.inner_text(".no-items")
            
        except Exception as e:
            # Screenshot при помилці
            page.screenshot(path="error_screenshot.png")
            raise e
        finally:
            browser.close()
