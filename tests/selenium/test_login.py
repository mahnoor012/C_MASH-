import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==== CONFIG ====
CHROMEDRIVER = r"C:\Users\HP\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
BASE_URL = "http://127.0.0.1:8000/"  # তোমার Django সার্ভারের URL


# ======================== Helper Functions ========================

def wait_for_server(url, timeout=30):
    """Wait until local server responds (avoid net::ERR_CONNECTION_REFUSED)."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                if 200 <= r.status < 400:
                    print("✅ Server is live.")
                    return True
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError(f"❌ Server not reachable at {url} within {timeout}s.")


def log(ok, msg):
    print(("✅ " if ok else "❌ ") + msg)


def open_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    service = Service(CHROMEDRIVER)
    return webdriver.Chrome(service=service, options=opts)


# ======================== Main Test ========================

def test_login_page():
    print("\n🔹 Login Page Test Started")
    wait_for_server(BASE_URL, timeout=30)

    driver = open_driver(headless=False)
    try:
        # Load Landing Page
        t0 = time.time()
        driver.get(BASE_URL)
        load_time = time.time() - t0
        log(True, f"Page loaded in {load_time:.2f} seconds")
        time.sleep(1)

        # 1) Click Log In Button
        print("Clicking Log In Button...")
        login_button = driver.find_element(By.LINK_TEXT, "Log In")
        login_button.click()
        time.sleep(2)  # Allow time for the page to load
        assert "Log In" in driver.title, "Log In page did not load"
        log(True, "Navigated to Log In page")

        # 2) Fill Login Form with valid data
        print("Filling in login form with valid credentials...")
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys("esha")  # Use valid username
        password_input.send_keys("Bismillah123")  # Use valid password

        # Attempting to locate the login button using CSS Selector or XPath
        try:
            login_button = driver.find_element(By.CSS_SELECTOR,
                                               "button[type='submit']")  # CSS selector for submit button
        except Exception as e:
            print(f"Error: {e}")
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")  # Fallback to XPath

        login_button.click()
        time.sleep(3)  # Allow redirection

        # Print the current URL to check where it redirects
        print(f"Current URL after login attempt: {driver.current_url}")

        # Wait for redirection and check if it's redirected to dashboard
        WebDriverWait(driver, 20).until(EC.url_contains("dashboard"))
        print(f"Redirected to: {driver.current_url}")  # Debugging: Print redirected URL

        assert "dashboard" in driver.current_url, f"Login failed, did not redirect to dashboard. Current URL: {driver.current_url}"
        log(True, "Valid login test passed, redirected to dashboard")

        print("✅ Log In Page Test PASSED\n")
    finally:
        driver.quit()
        print("🔹 Test finished.\n")


if __name__ == "__main__":
    test_login_page()
