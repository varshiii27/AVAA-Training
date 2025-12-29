import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
import time

@pytest.fixture(scope="module")
def driver():
    # Set up Chrome options for headless execution (suitable for GitHub CI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_google_search_selenium(driver):
    try:
        # 1. Open Google
        driver.get("https://www.google.com")
        WebDriverWait(driver, 10).until(
            EC.title_contains("Google")
        )
        # Assertion: Page title contains 'Google'
        assert "Google" in driver.title

        # Accept cookies if the consent form appears (for EU users)
        try:
            consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//div[text()='I agree']] | //button[.//div[text()='Accept all']] | //button[.//span[text()='Accept all']]")
                )
            )
            consent_button.click()
        except (TimeoutException, NoSuchElementException):
            pass  # Consent form not present

        # 2. Search for 'selenium'
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys("selenium")
        search_box.send_keys(Keys.RETURN)

        # 3. Wait for results page and check title
        WebDriverWait(driver, 10).until(
            EC.title_contains("selenium")
        )
        assert "selenium" in driver.title.lower()

        # 4. Get the first ten result URLs
        # Google search results are in <div class="g">, and the link is in <a>
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div#search div.g")
            )
        )

        # Assertion: At least 10 results are present
        assert len(results) >= 10, f"Expected at least 10 results, got {len(results)}"

        urls = []
        count = 0
        for result in results:
            try:
                link = result.find_element(By.CSS_SELECTOR, "a")
                href = link.get_attribute("href")
                if href and href.startswith("http"):
                    urls.append(href)
                    count += 1
                if count == 10:
                    break
            except NoSuchElementException:
                continue

        # Assertion: Exactly 10 URLs collected
        assert len(urls) == 10, f"Expected 10 URLs, got {len(urls)}"

        # 5. Print the first ten result URLs
        print("\nFirst 10 Google search result URLs for 'selenium':")
        for idx, url in enumerate(urls, 1):
            print(f"{idx}: {url}")

    except (NoSuchElementException, TimeoutException) as e:
        pytest.fail(f"Test failed due to exception: {e}")

    finally:
        # 8. Close the browser (handled by fixture teardown)
        pass  # driver.quit() is called by the fixture

# To run this test, save as test_google_search.py and execute:
# pytest -s test_google_search.py
