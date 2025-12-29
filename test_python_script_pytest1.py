# test_python_script_pytest1.py
# Selenium script to search 'selenium' on Google and print first five result URLs
# Compatible with GitHub CI (headless Chrome)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


def main():
    # Setup Chrome options for headless execution (suitable for CI)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)

        # 1. Open Google
        driver.get('https://www.google.com')
        assert 'Google' in driver.title, f"Unexpected page title: {driver.title}"

        # Accept cookies if the consent form appears (for EU users)
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all') or contains(., 'Accept')]")
            )
            consent_button.click()
        except TimeoutException:
            pass  # Consent form did not appear

        # 2. Search for 'selenium'
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        assert search_box.is_displayed(), "Search box is not displayed"
        search_box.clear()
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)

        # 3. Wait for results and print first five URLs
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#search a'))
        )
        assert len(results) > 0, "No search results found"
        print("First five result URLs:")
        count = 0
        for result in results:
            href = result.get_attribute('href')
            if href and href.startswith('http'):
                print(href)
                count += 1
                if count == 5:
                    break
        assert count == 5, f"Expected 5 results, found {count}"

    except NoSuchElementException as e:
        print(f"Element not found: {e}", file=sys.stderr)
        sys.exit(1)
    except TimeoutException as e:
        print(f"Timeout waiting for element: {e}", file=sys.stderr)
        sys.exit(1)
    except AssertionError as e:
        print(f"Assertion failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # 8. Properly close the browser
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
