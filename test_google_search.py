# test_google_search.py
# This script uses Selenium to automate a Google search for 'selenium', prints the first ten result URLs,
# includes assertions and error handling, and is ready for GitHub CI (headless Chrome).

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def main():
    # Setup Chrome options for headless execution (suitable for CI/CD)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')

    # Initialize WebDriver
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"[ERROR] Failed to initialize Chrome WebDriver: {e}")
        sys.exit(1)

    try:
        # Step 1: Open Google
        driver.get('https://www.google.com')
        time.sleep(2)  # Wait for page to load

        # Assertion: Page title contains 'Google'
        assert 'Google' in driver.title, f"[ASSERTION FAILED] Page title does not contain 'Google': {driver.title}"

        # Step 2: Locate the search box and search for 'selenium'
        try:
            search_box = driver.find_element(By.NAME, 'q')
        except NoSuchElementException:
            print("[ERROR] Search box not found on Google home page.")
            sys.exit(1)

        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for results to load

        # Step 3: Get the first ten result URLs
        try:
            results = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
            # Filter out only unique, visible result links
            urls = []
            for r in results:
                href = r.get_attribute('href')
                if href and href.startswith('http') and href not in urls:
                    urls.append(href)
                if len(urls) == 10:
                    break
        except NoSuchElementException:
            print("[ERROR] Could not find search result links.")
            sys.exit(1)

        # Assertion: At least ten results found
        assert len(urls) == 10, f"[ASSERTION FAILED] Expected 10 results, found {len(urls)}"

        # Step 4: Print the first ten result URLs
        print("First 10 Google search result URLs for 'selenium':")
        for i, url in enumerate(urls, start=1):
            print(f"{i}. {url}")

    except AssertionError as ae:
        print(f"[ASSERTION ERROR] {ae}")
        sys.exit(1)
    except TimeoutException:
        print("[ERROR] Timeout while waiting for page elements.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected exception: {e}")
        sys.exit(1)
    finally:
        # Cleanup: Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
