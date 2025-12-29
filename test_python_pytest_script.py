# test_google_search.py

import logging
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_TERM = "selenium"
RESULTS_SELECTOR = "div#search a"
COOKIE_CONSENT_XPATH = "//div[contains(@class, 'VfPpkd-RLmnJb') or @id='L2AGLb'] | //button[contains(., 'I agree') or contains(., 'Accept all')]"

@pytest.fixture(scope="function")
def driver():
    """Fixture to initialize and quit Chrome WebDriver with headless options."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configure logging for all tests."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

def handle_cookie_consent(driver):
    """Handle Google cookie consent dialog if present."""
    try:
        consent_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, COOKIE_CONSENT_XPATH))
        )
        consent_btn.click()
        logging.info("Cookie consent accepted.")
    except TimeoutException:
        logging.info("No cookie consent dialog found.")
    except Exception as e:
        logging.warning(f"Unexpected error handling cookie consent: {e}")

@pytest.mark.parametrize("search_term", ["selenium", "pytest", "webdriver"])
def test_google_search_top_10_results(driver, search_term):
    """
    Test Google search for a term and validate the top 10 result URLs.
    - Navigates to Google.
    - Handles cookie consent if present.
    - Searches for the term.
    - Asserts that at least 10 valid result URLs are found.
    """
    logging.info(f"Navigating to Google homepage for search term: '{search_term}'")
    driver.get("https://www.google.com")
    assert "Google" in driver.title, "Google homepage did not load"

    handle_cookie_consent(driver)

    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        assert search_box.is_displayed(), "Search box is not visible"
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        logging.info(f"Performed search for: {search_term}")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Search box interaction failed: {e}")
        pytest.fail(f"Search box not found or not interactable: {e}")

    try:
        # Wait for results to load
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='g']//a"))
        )
        top_10_results = [el.get_attribute("href") for el in results if el.get_attribute("href")]
        logging.info(f"Found {len(top_10_results)} result URLs.")
        assert len(top_10_results) >= 10, f"Less than 10 search results found for '{search_term}'"
        for idx, url in enumerate(top_10_results[:10], 1):
            assert url.startswith("http"), f"Result {idx} does not have a valid URL: {url}"
            logging.info(f"{idx}. {url}")
    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Results extraction failed: {e}")
        pytest.fail(f"Could not extract top 10 results: {e}")

# Hooks for pytest-html screenshot on failure (optional, for pytest-html plugin)
def pytest_runtest_makereport(item, call):
    # Attach screenshot to pytest-html on failure
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            try:
                screenshot = driver.get_screenshot_as_base64()
                extra = getattr(rep, "extra", [])
                from pytest_html import extras
                extra.append(extras.image(screenshot, mime_type="image/png"))
                rep.extra = extra
            except Exception as e:
                logging.warning(f"Could not capture screenshot: {e}")

# Note:
# - Run with: pytest --html=report.html --self-contained-html -n auto
# - Ensure requirements: selenium, pytest, pytest-html, pytest-xdist
# - Logging and error messages are included for debugging and reporting.
# - Test is parameterized for multiple search terms.
# - All code follows PEP 8 and pytest best practices.
