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
    WebDriverException
)

# Pytest fixture to set up and tear down the WebDriver
@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode for CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_google_search_selenium(driver):
    try:
        # Step 1: Open Google homepage
        driver.get("https://www.google.com")
        assert "Google" in driver.title, "Google homepage did not load properly"

        # Step 2: Accept cookies if the consent form appears (for EU users)
        try:
            consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='I agree']] | //button[.//div[text()='Accept all']]"))
            )
            consent_button.click()
        except TimeoutException:
            # Consent form did not appear, continue
            pass

        # Step 3: Find the search box, enter 'selenium', and submit the search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        assert search_box.is_displayed(), "Search box is not visible"
        search_box.clear()
        search_box.send_keys("selenium")
        search_box.send_keys(Keys.RETURN)

        # Step 4: Wait for search results to load
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#search a"))
        )
        assert len(results) > 0, "No search results found"

        # Step 5: Collect and print the first five result URLs
        urls = []
        count = 0
        for result in results:
            href = result.get_attribute("href")
            if href and href.startswith("http"):
                urls.append(href)
                count += 1
                if count == 5:
                    break
        assert len(urls) == 5, f"Expected 5 URLs, but found {len(urls)}"
        for idx, url in enumerate(urls, 1):
            print(f"Result {idx}: {url}")

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Test failed due to exception: {e}")
        assert False, f"Test failed due to exception: {e}"
