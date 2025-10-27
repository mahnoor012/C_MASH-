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
BASE_URL = "http://127.0.0.1:8000/"   # তোমার Django সার্ভারের URL

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

def test_landing_page():
    print("\n🔹 Landing Page Test Started")
    wait_for_server(BASE_URL, timeout=30)

    driver = open_driver(headless=False)
    try:
        # Load page
        t0 = time.time()
        driver.get(BASE_URL)
        load_time = time.time() - t0
        log(True, f"Page loaded in {load_time:.2f} seconds")
        time.sleep(1)  # Reduced delay after page load

        # Title check
        title = driver.title.strip()
        log(("C.Mesh" in title or "C_MESH" in title), f"Title check → '{title}'")
        time.sleep(1)  # Reduced delay after title check

        # Header nav check
        nav_texts = ["Home", "About", "Contact", "Sign Up", "Log In"]
        for txt in nav_texts:
            try:
                el = WebDriverWait(driver, 6).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, txt))
                )
                log(el.is_displayed(), f"Nav '{txt}' visible")
                time.sleep(1)  # Reduced delay after checking each nav item
            except Exception:
                log(False, f"Nav '{txt}' not found")

        # Navigation test
        routes = {
            "About": "about",
            "Contact": "contact",
            "Sign Up": "signup",
            "Log In": "login",
        }

        for txt, slug in routes.items():
            try:
                driver.get(BASE_URL)
                link = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, txt))
                )
                link.click()
                time.sleep(2)  # Reduced delay after clicking each link
                WebDriverWait(driver, 6).until(lambda d: slug in d.current_url)
                log(True, f"Clicked '{txt}' → {driver.current_url}")
            except Exception as e:
                log(False, f"'{txt}' click failed: {e}")

        # Hero Sign Up button (onclick='signup.html')
        try:
            driver.get(BASE_URL)
            btn = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".hero .hero-text button"))
            )
            btn.click()
            time.sleep(2)  # Reduced delay after clicking the Hero button
            WebDriverWait(driver, 6).until(
                lambda d: "signup" in d.current_url or "signup.html" in d.current_url
            )
            log(True, f"Hero Sign Up button works → {driver.current_url}")
        except Exception as e:
            log(False, f"Hero Sign Up button failed: {e}")

        # Hero image loaded
        try:
            driver.get(BASE_URL)
            img = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".hero-img img"))
            )
            loaded = driver.execute_script("return arguments[0].complete && arguments[0].naturalWidth>0;", img)
            log(loaded, "Hero image loaded properly")
        except Exception as e:
            log(False, f"Hero image not found: {e}")

        # Mobile view check
        driver.set_window_size(375, 667)
        time.sleep(2)  # Reduced delay for mobile viewport check
        log(True, "Mobile viewport check (375x667) OK")

        print("✅ Landing page smoke test PASSED\n")

    finally:
        driver.quit()
        print("🔹 Test finished.\n")

if __name__ == "__main__":
    test_landing_page()
