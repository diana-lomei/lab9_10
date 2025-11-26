from playwright.sync_api import sync_playwright

def test_user_journey():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # Відкриваємо локальну HTML сторінку
            page.goto("file:///C:/Users/Diana/Downloads/my-app/index.html")
            # Реєстрація
            page.fill("#username", "testuser")
            page.fill("#password", "Password123")
            page.click("#register-btn")
            page.wait_for_selector("#registration-success", timeout=5000)
            assert "Registration successful" in page.inner_text("#registration-success")
            # Логін
            page.fill("#login-username", "testuser")
            page.fill("#login-password", "Password123")
            page.click("#login-btn")
            page.wait_for_selector("#welcome-message", timeout=5000)
            assert "Welcome, testuser" in page.inner_text("#welcome-message")
        except Exception:
            page.screenshot(path="error_screenshot.png")
            raise
        finally:
            browser.close()
