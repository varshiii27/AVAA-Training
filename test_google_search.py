# test_google_search.py
# This script uses Selenium to automate Google search, print the first ten result URLs, and includes assertions and error handling.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time


def main():
    # Configure Chrome options for headless execution (for CI/CD compatibility)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = None
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)

        # Step 1: Open Google
        driver.get('https://www.google.com')
        time.sleep(2)  # Wait for the page to load

        # Step 2: Assert that the search box is present
        try:
            search_box = driver.find_element(By.NAME, 'q')
        except NoSuchElementException:
            raise AssertionError('Search box not found on Google homepage.')
        assert search_box.is_displayed(), 'Search box is not visible.'

        # Step 3: Search for 'selenium'
        search_box.clear()
        search_box.send_keys('selenium')
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for results to load

        # Step 4: Find search results and assert at least 10 are present
        results = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
        # Filter only unique hrefs and skip non-result links
        urls = []
        seen = set()
        for elem in results:
            href = elem.get_attribute('href')
            if href and href.startswith('http') and href not in seen:
                urls.append(href)
                seen.add(href)
            if len(urls) == 10:
                break

        assert len(urls) >= 10, f'Expected at least 10 search results, found {len(urls)}.'

        # Step 5: Print the first ten URLs
        print('First ten URLs from Google search results for "selenium":')
        for i, url in enumerate(urls, 1):
            print(f'{i}: {url}')

    except (AssertionError, NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f'Error occurred: {e}')
    finally:
        # Properly close the WebDriver
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
