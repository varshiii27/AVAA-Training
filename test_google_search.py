import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException

def main():
    # Set up Chrome options for headless execution (for CI/CD compatibility)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        assert driver is not None, "WebDriver failed to initialize"

        # Open Google
        driver.get("https://www.google.com")
        assert "Google" in driver.title, "Google homepage did not load properly"

        # Locate the search box, enter 'selenium', and submit
        search_box = driver.find_element(By.NAME, "q")
        assert search_box is not None, "Search box not found"
        search_box.send_keys("selenium")
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load
        time.sleep(2)  # In production, use WebDriverWait for robustness

        # Find search result elements
        results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
        assert len(results) > 0, "No search results found"

        # Print the first ten URLs
        print("Top 10 search result URLs for 'selenium':")
        for idx, result in enumerate(results[:10]):
            url = result.get_attribute("href")
            assert url.startswith("http"), f"Result {idx+1} does not look like a valid URL"
            print(f"{idx+1}: {url}")

    except (NoSuchElementException, AssertionError, WebDriverException) as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure proper cleanup of the WebDriver
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
