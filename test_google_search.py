#!/usr/bin/env python3
"""
Selenium script to open Google in headless Chrome, search for 'selenium',
print the first ten result URLs, with assertions, error handling, and comments.
Ready for CI/CD pipeline use.
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)

def main():
    # Configure Chrome options for headless mode (CI/CD compatibility)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = None
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)

        # Step 1: Open Google
        driver.get('https://www.google.com')
        assert 'Google' in driver.title, f"Unexpected page title: {driver.title}"
        print("Opened Google homepage successfully.")

        # Step 2: Find the search box and enter 'selenium'
        try:
            search_box = driver.find_element(By.NAME, 'q')
        except NoSuchElementException:
            raise AssertionError("Google search box not found!")
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)
        print("Searched for 'selenium'.")

        # Step 3: Wait for results to load
        time.sleep(2)  # Simple wait; in production, use WebDriverWait
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        assert len(results) >= 10, f"Expected at least 10 results, got {len(results)}"
        print(f"Found {len(results)} search results.")

        # Step 4: Print the first ten result URLs
        print("First 10 result URLs:")
        for idx, result in enumerate(results[:10], 1):
            url = result.get_attribute('href')
            print(f"{idx}: {url}")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Selenium error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    except AssertionError as ae:
        print(f"Assertion failed: {ae}", file=sys.stderr)
        sys.exit(2)
    except Exception as ex:
        print(f"Unexpected error: {ex}", file=sys.stderr)
        sys.exit(3)
    finally:
        # Step 5: Clean up and close the browser
        if driver:
            driver.quit()
        print("WebDriver closed.")

if __name__ == '__main__':
    main()
