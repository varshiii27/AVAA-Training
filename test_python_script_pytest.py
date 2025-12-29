import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Set up Chrome options for headless execution (required for CI/CD)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Open Google
        driver.get("https://www.google.com")
        assert "Google" in driver.title, "Page title does not contain 'Google'"

        # 2. Search for 'selenium'
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.send_keys("selenium")
        search_box.submit()

        # 3. Wait for results and print the first ten result URLs
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yuRUbf > a")))
        assert len(results) > 0, "No search results found"

        print("Top 10 Google search results for 'selenium':")
        for i, result in enumerate(results[:10], 1):
            url = result.get_attribute("href")
            print(f"{i}. {url}")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {e.__class__.__name__} - {e}")
    except AssertionError as ae:
        print(f"Assertion failed: {ae}")
    finally:
        # 7. Properly close the browser
        driver.quit()

if __name__ == "__main__":
    main()
