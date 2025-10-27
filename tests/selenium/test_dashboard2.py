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
    """Open Chrome driver with specific options."""
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    service = Service(CHROMEDRIVER)
    return webdriver.Chrome(service=service, options=opts)


# ======================== Main Test ========================

def test_dashboard_page():
    print("\n🔹 Dashboard Page Test Started")
    wait_for_server(BASE_URL, timeout=30)

    driver = open_driver(headless=False)
    try:
        # 1) Landing Page Load
        driver.get(BASE_URL)
        time.sleep(1)

        # Check the title of the page (update with your page title)
        assert "C.Mesh" in driver.title, "Landing Page not loaded properly"
        log(True, "Landing page loaded successfully")

        # 2) Click Log In Button
        print("Clicking Log In Button...")
        login_button = driver.find_element(By.LINK_TEXT, "Log In")
        login_button.click()
        time.sleep(2)
        assert "Log In" in driver.title, "Log In page did not load"
        log(True, "Navigated to Log In page")

        # 3) Fill Login Form with valid data
        print("Filling in login form with valid credentials...")
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys("tusar79")  # Use valid username
        password_input.send_keys("Bismillah123")  # Use valid password

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        time.sleep(3)  # Allow redirection

        # 4) Check redirection to Dashboard page
        WebDriverWait(driver, 20).until(EC.url_contains("dashboard"))
        print(f"Current URL: {driver.current_url}")  # Debug: print current URL
        assert "dashboard" in driver.current_url, f"Login failed, did not redirect to dashboard. Current URL: {driver.current_url}"
        log(True, "Valid login test passed, redirected to dashboard")

        # 5) Dashboard Sidebar Check (Calendar and CpArena)
        print("Checking Calendar button...")
        calendar_button = driver.find_element(By.LINK_TEXT, "Calendar")
        calendar_button.click()
        time.sleep(2)  # Allow time for the page to load
        print(f"Redirected to: {driver.current_url}")
        assert "calendar" in driver.current_url, "Failed to navigate to Calendar page"
        log(True, "Calendar page loaded successfully")

        # Go back to Dashboard after Calendar
        driver.back()
        time.sleep(2)  # Wait for the page to load
        assert "dashboard" in driver.current_url, "Failed to return to Dashboard after Calendar"
        log(True, "Returned to Dashboard from Calendar")

        print("Checking CpArena button...")
        cp_arena_button = driver.find_element(By.LINK_TEXT, "CpArena")
        cp_arena_button.click()
        time.sleep(2)  # Allow time for the page to load
        print(f"Redirected to: {driver.current_url}")
        assert "dashboard" in driver.current_url, "Failed to navigate to CpArena page"
        log(True, "CpArena page loaded successfully")

        # Go back to Dashboard after CpArena
        driver.back()
        time.sleep(2)  # Wait for the page to load
        assert "dashboard" in driver.current_url, "Failed to return to Dashboard after CpArena"
        log(True, "Returned to Dashboard from CpArena")

        # 6) Check for header logout button
        print("Testing logout functionality...")
        logout_button = driver.find_element(By.LINK_TEXT, "Logout")
        logout_button.click()
        time.sleep(3)

        # Check if the logout was successful and we are redirected to login page
        assert "login" in driver.current_url, "Logout failed, did not redirect to login page"
        log(True, "Logout test passed, redirected to login page")







    # 5) Dashboard Sidebar Check (To Do, In Progress, Completed Buttons)
        print("Checking Dashboard buttons...")

# Check To Do button
        todo_button = driver.find_element(By.LINK_TEXT, "To Do")
        todo_button.click()
        time.sleep(2)  # Wait for page load
        assert "todo" in driver.current_url, "Failed to navigate to To Do tasks"
        log(True, "To Do section loaded successfully")

# Go back to Dashboard
        driver.back()
        time.sleep(2)

# Check In Progress button
        in_progress_button = driver.find_element(By.LINK_TEXT, "In Progress")
        in_progress_button.click()
        time.sleep(2)  # Wait for page load
        assert "in_progress" in driver.current_url, "Failed to navigate to In Progress tasks"
        log(True, "In Progress section loaded successfully")

# Go back to Dashboard
        driver.back()
        time.sleep(2)

# Check Completed button
        completed_button = driver.find_element(By.LINK_TEXT, "Completed")
        completed_button.click()
        time.sleep(2)  # Wait for page load
        assert "completed" in driver.current_url, "Failed to navigate to Completed tasks"
        log(True, "Completed section loaded successfully")

# Go back to Dashboard
        driver.back()
        time.sleep(2)

# 6) Check Floating Add Task Button
        add_task_button = driver.find_element(By.CSS_SELECTOR, ".add-task-icon")
        add_task_button.click()
        time.sleep(2)
        add_task_form = driver.find_element(By.CSS_SELECTOR, ".add-task-form")
        log(add_task_form.is_displayed(), "Add Task form is displayed")

# 7) Add Task - Filling form and submitting
        print("Adding a new task...")
        task_title_input = driver.find_element(By.ID, "title")
        task_description_input = driver.find_element(By.ID, "description")
        task_status_select = driver.find_element(By.ID, "status")

        task_title_input.send_keys("New Task")
        task_description_input.send_keys("This is a new task.")
        task_status_select.send_keys("todo")

        add_task_button_submit = driver.find_element(By.CSS_SELECTOR, ".add-task-form button")
        add_task_button_submit.click()
        time.sleep(3)

# 8) Verify task is added (we'll need to check if the task appears in the "To Do" section)
        todo_section = driver.find_element(By.LINK_TEXT, "To Do")
        todo_section.click()
        time.sleep(2)
        tasks_in_todo = driver.find_elements(By.CSS_SELECTOR, ".task-section ul li")
        task_titles = [task.text for task in tasks_in_todo]
        log("New Task" in task_titles, "New Task added successfully to To Do section")

# 9) Delete Task
        delete_button = driver.find_element(By.CSS_SELECTOR, ".task-section ul li button")  # Delete button for first task
        delete_button.click()
        time.sleep(2)

# Verify if the task is deleted
        tasks_after_deletion = driver.find_elements(By.CSS_SELECTOR, ".task-section ul li")
        task_titles_after_deletion = [task.text for task in tasks_after_deletion]
        log("New Task" not in task_titles_after_deletion, "Task deleted successfully")


    finally:
        driver.quit()
        print("🔹 Test finished.\n")

    if __name__ == "__main__":
        test_dashboard_page()



        ////
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
            """Open Chrome driver with specific options."""
            opts = Options()
            if headless:
                opts.add_argument("--headless=new")
            opts.add_argument("--start-maximized")
            service = Service(CHROMEDRIVER)
            return webdriver.Chrome(service=service, options=opts)

        # ======================== Main Test ========================

        def test_dashboard_page():
            print("\n🔹 Dashboard Page Test Started")
            wait_for_server(BASE_URL, timeout=30)

            driver = open_driver(headless=False)
            try:
                # 1) Landing Page Load
                driver.get(BASE_URL)
                time.sleep(1)

                # Check the title of the page (update with your page title)
                assert "C.Mesh" in driver.title, "Landing Page not loaded properly"
                log(True, "Landing page loaded successfully")

                # 2) Click Log In Button
                print("Clicking Log In Button...")
                login_button = driver.find_element(By.LINK_TEXT, "Log In")
                login_button.click()
                time.sleep(2)
                assert "Log In" in driver.title, "Log In page did not load"
                log(True, "Navigated to Log In page")

                # 3) Fill Login Form with valid data
                print("Filling in login form with valid credentials...")
                username_input = driver.find_element(By.NAME, "username")
                password_input = driver.find_element(By.NAME, "password")

                username_input.send_keys("tusar79")  # Use valid username
                password_input.send_keys("Bismillah123")  # Use valid password

                login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()
                time.sleep(3)  # Allow redirection

                # 4) Check redirection to Dashboard page
                WebDriverWait(driver, 20).until(EC.url_contains("dashboard"))
                print(f"Current URL: {driver.current_url}")  # Debug: print current URL
                assert "dashboard" in driver.current_url, f"Login failed, did not redirect to dashboard. Current URL: {driver.current_url}"
                log(True, "Valid login test passed, redirected to dashboard")

                # 5) Dashboard Sidebar Check (Calendar and CpArena)
                print("Checking Calendar button...")
                calendar_button = driver.find_element(By.LINK_TEXT, "Calendar")
                calendar_button.click()
                time.sleep(2)  # Allow time for the page to load
                print(f"Redirected to: {driver.current_url}")
                assert "calendar" in driver.current_url, "Failed to navigate to Calendar page"
                log(True, "Calendar page loaded successfully")

                # Go back to Dashboard after Calendar
                driver.back()
                time.sleep(2)  # Wait for the page to load
                assert "dashboard" in driver.current_url, "Failed to return to Dashboard after Calendar"
                log(True, "Returned to Dashboard from Calendar")

                print("Checking CpArena button...")
                cp_arena_button = driver.find_element(By.LINK_TEXT, "CpArena")
                cp_arena_button.click()
                time.sleep(2)  # Allow time for the page to load
                print(f"Redirected to: {driver.current_url}")
                assert "dashboard" in driver.current_url, "Failed to navigate to CpArena page"
                log(True, "CpArena page loaded successfully")

                # Go back to Dashboard after CpArena
                driver.back()
                time.sleep(2)  # Wait for the page to load
                assert "dashboard" in driver.current_url, "Failed to return to Dashboard after CpArena"
                log(True, "Returned to Dashboard from CpArena")

                # 6) Check for header logout button
                print("Testing logout functionality...")
                logout_button = driver.find_element(By.LINK_TEXT, "Logout")
                logout_button.click()
                time.sleep(3)

                # Check if the logout was successful and we are redirected to login page
                assert "login" in driver.current_url, "Logout failed, did not redirect to login page"
                log(True, "Logout test passed, redirected to login page")

                print("✅ Dashboard page test PASSED\n")

            finally:
                driver.quit()
                print("🔹 Test finished.\n")

        if __name__ == "__main__":
            test_dashboard_page()
