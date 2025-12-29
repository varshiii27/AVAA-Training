from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time

def main():
    # Setup Chrome options for headless execution (suitable for CI/CD)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # Implicit wait for elements

    try:
        # Step 1: Navigate to Google
        driver.get('https://www.google.com/')
        assert 'Google' in driver.title, "Google homepage did not load properly."

        # Step 2: Locate the search box and assert its presence
        try:
            search_box = driver.find_element(By.NAME, 'q')
        except NoSuchElementException:
            raise AssertionError("Search box not found on Google homepage.")
        assert search_box.is_displayed(), "Search box is not visible."

        # Step 3: Enter search term and submit
        search_box.clear()
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)

        # Step 4: Wait for search results to load
        time.sleep(2)  # Simple wait; in production, use WebDriverWait

        # Step 5: Find search result links
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        assert len(results) >= 10, f"Expected at least 10 results, found {len(results)}."

        # Step 6: Print the first ten URLs
        print("First 10 Google search result URLs for 'selenium':")
        for idx, result in enumerate(results[:10], 1):
            url = result.get_attribute('href')
            print(f"{idx}. {url}")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Selenium error occurred: {e}")
    except AssertionError as ae:
        print(f"Assertion failed: {ae}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")
    finally:
        # Step 7: Properly close the driver
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
