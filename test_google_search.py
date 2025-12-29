#!/usr/bin/env python3
"""
Selenium Google Search Script
Opens Google, searches for 'selenium', prints the first ten URLs from the search results.
Includes assertions, headless Chrome setup, error handling, and proper cleanup for CI compatibility.
"""
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def main():
    # Setup Chrome options for headless execution (CI compatibility)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

        # Open Google
        driver.get('https://www.google.com')
        assert 'Google' in driver.title, "Google homepage did not load properly."

        # Accept cookies if the consent form appears
        try:
            consent_button = driver.find_element(By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all') or contains(., 'Accept')]")
            consent_button.click()
            time.sleep(1)  # Wait for the dialog to close
        except NoSuchElementException:
            pass  # Consent dialog did not appear

        # Locate the search box, enter 'selenium', and submit
        search_box = driver.find_element(By.NAME, 'q')
        assert search_box.is_displayed(), "Search box is not visible."
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load
        time.sleep(2)

        # Find search result URLs
        results = driver.find_elements(By.XPATH, "//div[@id='search']//a")
        urls = []
        for elem in results:
            href = elem.get_attribute('href')
            if href and href.startswith('http') and 'google.' not in href:
                urls.append(href)
            if len(urls) >= 10:
                break

        assert len(urls) == 10, f"Expected 10 URLs, found {len(urls)}."

        print("First 10 search result URLs for 'selenium':")
        for i, url in enumerate(urls, 1):
            print(f"{i}: {url}")

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


if __name__ == "__main__":
    main()
