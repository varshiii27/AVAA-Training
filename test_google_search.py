from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def main():
    # Setup Chrome options for headless execution (for GitHub CI compatibility)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)

        # Step 1: Navigate to Google
        driver.get('https://www.google.com')

        # Assertion: Page title should contain 'Google'
        assert 'Google' in driver.title, f"Page title does not contain 'Google': {driver.title}"

        # Step 2: Find the search box, enter 'selenium', and submit
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
        except TimeoutException:
            print('Search box not found within timeout.', file=sys.stderr)
            return
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)

        # Step 3: Wait for search results to load
        try:
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.yuRUbf > a'))
            )
        except TimeoutException:
            print('Search results not found within timeout.', file=sys.stderr)
            return

        # Assertion: At least 10 results should be present
        assert len(results) >= 10, f"Less than 10 results found: {len(results)}"

        # Step 4: Print the first ten URLs
        print('First ten URLs from Google search results for "selenium":')
        for i, result in enumerate(results[:10], 1):
            try:
                url = result.get_attribute('href')
                print(f"{i}. {url}")
            except Exception as e:
                print(f"Error retrieving URL for result {i}: {e}", file=sys.stderr)

    except AssertionError as ae:
        print(f"Assertion failed: {ae}", file=sys.stderr)
    except NoSuchElementException as ne:
        print(f"Element not found: {ne}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        # Cleanup: Properly close the WebDriver
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
