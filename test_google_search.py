#!/usr/bin/env python3
"""
Selenium script to search Google for 'selenium', print the first ten result URLs, with assertions, error handling, headless Chrome setup for CI, and proper cleanup.
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def main():
    # Configure Chrome options for headless execution (suitable for GitHub CI)
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
        driver.set_page_load_timeout(30)

        # Open Google
        driver.get('https://www.google.com')
        assert 'Google' in driver.title, "Google homepage did not load properly."

        # Accept cookies if prompted (for EU users)
        try:
            consent_button = driver.find_element(By.XPATH, '//button[contains(text(), "I agree") or contains(text(), "Accept all")]')
            consent_button.click()
            time.sleep(1)
        except NoSuchElementException:
            pass  # Consent dialog not present

        # Find the search box, enter 'selenium', and submit
        search_box = driver.find_element(By.NAME, 'q')
        assert search_box.is_displayed() and search_box.is_enabled(), "Search box is not available."
        search_box.clear()
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load
        time.sleep(2)
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        assert len(results) >= 10, f"Expected at least 10 results, got {len(results)}."

        print("First 10 Google search result URLs for 'selenium':")
        for i, result in enumerate(results[:10], 1):
            url = result.get_attribute('href')
            assert url.startswith('http'), f"Result {i} does not have a valid URL: {url}"
            print(f"{i}. {url}")

    except AssertionError as ae:
        print(f"Assertion failed: {ae}", file=sys.stderr)
        sys.exit(1)
    except WebDriverException as we:
        print(f"WebDriver error: {we}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(3)
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
