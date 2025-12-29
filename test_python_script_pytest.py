#!/usr/bin/env python3
"""
Selenium script to open Google, search for 'selenium', print the first five result URLs.
Includes assertions, error handling, headless Chrome options for CI, comments, and proper cleanup.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
import time
import sys

def main():
    # Configure Chrome options for headless execution (suitable for GitHub CI)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    driver = None
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(15)

        # Step 1: Open Google
        driver.get('https://www.google.com')
        assert 'Google' in driver.title, "Google homepage did not load properly."
        print("[INFO] Google homepage loaded successfully.")

        # Step 2: Search for 'selenium'
        try:
            search_box = driver.find_element(By.NAME, 'q')
        except NoSuchElementException:
            raise AssertionError("Search box not found on Google homepage.")
        search_box.clear()
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)
        print("[INFO] Search for 'selenium' submitted.")

        # Step 3: Wait for results to load
        time.sleep(2)  # Simple wait; for production, use WebDriverWait
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        assert len(results) > 0, "No search results found."
        print(f"[INFO] Found {len(results)} search results.")

        # Step 4: Print the first five result URLs
        print("First five result URLs:")
        for i, result in enumerate(results[:5], 1):
            url = result.get_attribute('href')
            print(f"{i}: {url}")

    except (AssertionError, WebDriverException, TimeoutException) as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    finally:
        # Step 5: Cleanup
        if driver:
            driver.quit()
        print("[INFO] WebDriver closed.")

if __name__ == "__main__":
    main()
