import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and teardown headless Chrome WebDriver.
    Ensures compatibility with GitHub CI environments.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()  # Ensure WebDriver is properly closed after test

def test_google_search_selenium(driver):
    """
    Test case to:
    1. Open Google in headless Chrome.
    2. Search for 'selenium'.
    3. Print the first ten result URLs.
    4. Assert page title, search results presence, and handle errors.
    """

    try:
        # Step 1: Open Google homepage
        driver.get("https://www.google.com")
        # Assert that the page title contains 'Google'
        assert "Google" in driver.title, f"Page title does not contain 'Google': {driver.title}"

        # Step 2: Locate the search box and enter 'selenium'
        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
        except TimeoutException:
            pytest.fail("Search box not found within timeout.")

        search_box.clear()
        search_box.send_keys("selenium")
        search_box.send_keys(Keys.RETURN)

        # Step 3: Wait for search results to load
        try:
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g"))
            )
        except TimeoutException:
            pytest.fail("Search results not found within timeout.")

        # Assert that at least one search result is present
        assert len(results) > 0, "No search results found."

        # Step 4: Extract and print the first ten result URLs
        printed_count = 0
        for result in results:
            try:
                # Google search results URLs are typically in <a> tags within div.g
                link = result.find_element(By.CSS_SELECTOR, "a")
                url = link.get_attribute("href")
                if url and url.startswith("http"):
                    print(url)
                    printed_count += 1
                if printed_count >= 10:
                    break
            except NoSuchElementException:
                # If no link is found in this result, skip it
                continue

        # Assert that at least 10 URLs were printed
        assert printed_count == 10, f"Expected 10 result URLs, found {printed_count}."

    except Exception as e:
        pytest.fail(f"Test failed due to unexpected error: {e}")

# To run this test, use: pytest <script_name>.py
