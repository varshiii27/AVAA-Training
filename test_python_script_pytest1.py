import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def main():
    # Set up Chrome options for headless execution (CI/CD compatibility)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")

    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
    except WebDriverException as e:
        print(f"Error initializing Chrome WebDriver: {e}")
        sys.exit(1)

    try:
        # Step 1: Open Google
        driver.get("https://www.google.com")
        assert "Google" in driver.title, "Google homepage did not load correctly."

        # Step 2: Find the search box and enter 'selenium'
        search_box = driver.find_element(By.NAME, "q")
        assert search_box.is_displayed() and search_box.is_enabled(), "Search box not available."
        search_box.clear()
        search_box.send_keys("selenium")
        search_box.submit()

        # Step 3: Wait for results to load
        time.sleep(2)  # Simple wait; for production, use WebDriverWait

        # Step 4: Collect the first ten URLs from the search results
        results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
        assert len(results) >= 10, f"Expected at least 10 results, found {len(results)}."

        print("First 10 URLs from Google search results for 'selenium':")
        for i, result in enumerate(results[:10], 1):
            url = result.get_attribute("href")
            assert url.startswith("http"), f"Result {i} does not have a valid URL: {url}"
            print(f"{i}: {url}")

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up and close the browser
        driver.quit()

if __name__ == "__main__":
    main()
