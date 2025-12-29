from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time
import sys

def main():
    # Set up Chrome options for headless execution (for CI/CD compatibility)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

        # Step 1: Open Google
        driver.get("https://www.google.com")
        assert "Google" in driver.title, "Google homepage did not load correctly."

        # Accept cookies if the consent form appears (for EU users)
        try:
            consent_button = driver.find_element(By.XPATH, "//div[contains(@class, 'VfPpkd-RLmnJb') or @id='L2AGLb']")
            consent_button.click()
            time.sleep(1)  # Wait for the consent dialog to close
        except NoSuchElementException:
            pass  # Consent dialog not present

        # Step 2: Locate the search box and enter 'selenium'
        search_box = driver.find_element(By.NAME, "q")
        assert search_box.is_displayed(), "Search box is not visible."
        search_box.clear()
        search_box.send_keys("selenium")
        search_box.send_keys(Keys.RETURN)

        # Step 3: Wait for the results to load and collect URLs
        time.sleep(2)  # Wait for results page to load

        # Google search results are in <div class="g"> blocks, links are in <a> tags
        results = driver.find_elements(By.XPATH, "//div[@class='g']//div[@class='yuRUbf']/a")
        assert len(results) > 0, "No search results found."

        # Step 4: Print the first ten URLs
        print("Top 10 URLs for 'selenium' Google search:")
        for idx, result in enumerate(results[:10], 1):
            url = result.get_attribute("href")
            assert url.startswith("http"), f"Result {idx} does not have a valid URL."
            print(f"{idx}: {url}")

        # Additional assertion to ensure at least 10 results are present
        assert len(results) >= 10, f"Expected at least 10 results, found {len(results)}."

    except (AssertionError, NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Test failed: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up and close the browser
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
