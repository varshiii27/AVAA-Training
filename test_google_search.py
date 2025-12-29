from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time

def main():
    # Setup Chrome options for headless execution (for GitHub CI compatibility)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)

        # Step 1: Open Google
        driver.get('https://www.google.com')
        assert 'Google' in driver.title, "Google homepage did not load properly."

        # Step 2: Find the search box and enter 'selenium'
        search_box = driver.find_element(By.NAME, 'q')
        assert search_box.is_displayed() and search_box.is_enabled(), "Search box is not available."
        search_box.clear()
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)

        # Step 3: Wait for results to load
        time.sleep(2)  # Simple wait; in production, use WebDriverWait

        # Step 4: Collect the first ten URLs from the search results
        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf > a')
        assert len(results) > 0, "No search results found."
        print("First ten URLs from Google search results for 'selenium':")
        for i, result in enumerate(results[:10], start=1):
            url = result.get_attribute('href')
            assert url.startswith('http'), f"Result {i} does not have a valid URL."
            print(f"{i}. {url}")

        # Additional assertion: Ensure we have at least 10 results
        assert len(results) >= 10, "Less than 10 search results found."

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"An error occurred: {e}")
        assert False, f"Test failed due to exception: {e}"
    finally:
        # Proper cleanup: close the browser
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
