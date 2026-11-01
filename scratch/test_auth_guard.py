from playwright.sync_api import sync_playwright

def test_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Test 1: Open dashboard.html directly with fresh context (no session)
        print("=== Test 1: Direct access to dashboard.html without session ===")
        context1 = browser.new_context()
        page1 = context1.new_page()
        page1.goto("http://localhost:8080/dashboard.html", wait_until="networkidle")
        print("Final URL:", page1.url)
        assert "index.html" in page1.url, f"Expected redirect to index.html, got {page1.url}"
        print("PASSED: Unauthenticated user was redirected to index.html!")
        context1.close()

        # Test 2: Login via index.html
        print("\n=== Test 2: Login via index.html ===")
        context2 = browser.new_context()
        page2 = context2.new_page()
        page2.goto("http://localhost:8080/index.html", wait_until="networkidle")
        
        # Fill login form for admin
        page2.fill("#username", "admin@ku.th")
        page2.fill("#password", "Admin@1234")
        page2.click("#btn-login-submit")
        page2.wait_for_url("**/dashboard.html", timeout=5000)
        print("URL after login:", page2.url)
        assert "dashboard.html" in page2.url
        print("PASSED: Admin successfully logged in and entered dashboard.html!")
        
        # Test 3: Reload within the same session
        print("\n=== Test 3: Page refresh within the active session ===")
        page2.reload(wait_until="networkidle")
        print("URL after refresh:", page2.url)
        assert "dashboard.html" in page2.url
        print("PASSED: Active session maintained across page reload!")

        # Test 4: New browser context (simulating closing browser and clicking dashboard link again)
        print("\n=== Test 4: New browser window clicking dashboard.html ===")
        context3 = browser.new_context()
        page3 = context3.new_page()
        page3.goto("http://localhost:8080/dashboard.html", wait_until="networkidle")
        print("Final URL in new context:", page3.url)
        assert "index.html" in page3.url
        print("PASSED: New session requires logging in again, redirected to index.html!")
        context3.close()

        # Test 5: Dev/testing parameter ?user=student
        print("\n=== Test 5: Testing param ?user=student ===")
        context4 = browser.new_context()
        page4 = context4.new_page()
        page4.goto("http://localhost:8080/dashboard.html?user=student", wait_until="networkidle")
        print("Final URL for ?user=student:", page4.url)
        assert "dashboard.html?user=student" in page4.url
        print("PASSED: Test parameters still function for automated tests!")
        context4.close()

        browser.close()
        print("\nALL 5 AUTH GUARD TESTS PASSED 100%!")

if __name__ == '__main__':
    test_auth()
