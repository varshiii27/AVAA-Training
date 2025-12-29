import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture(scope="session")
def chrome_options():
    """Set up Chrome options for headless execution (CI-friendly)."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options


@pytest.fixture(scope="function")
def driver(chrome_options):
    """Initialize and quit Chrome WebDriver."""
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def open_google(driver):
    """Open Google homepage and return driver."""
    driver.get("https://www.google.com")
    return driver


# ---------------------------
# Helper Functions
# ---------------------------
def accept_cookies_if_present(driver):
    """Click 'I agree' or 'Accept all' button if cookie consent popup appears."""
    try:
        consent_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all')]")
            )
        )
        consent_button.click()
    except Exception:
        pass


# ---------------------------
# Tests
# ---------------------------
def test_google_homepage_title(open_google):
    """Verify Google homepage loads correctly."""
    driver = open_google
    accept_cookies_if_present(driver)
    assert "Google" in driver.title


def test_google_search_box_visible(open_google):
    """Verify the search box is visible on Google homepage."""
    driver = open_google
    accept_cookies_if_present(driver)
    search_box = driver.find_element(By.NAME, "q")
    assert search_box.is_displayed()


def test_google_search_results(open_google):
    """Perform a search and verify the first 10 results URLs."""
    driver = open_google
    accept_cookies_if_present(driver)

    # Enter search term
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    search_box.submit()

    # Wait for results page title
    WebDriverWait(driver, 20).until(EC.title_contains("selenium"))
    assert "selenium" in driver.title.lower()

    # Collect first 10 result URLs
    results = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "div.yuRUbf > a, div#search a")
        )
    )

    urls = []
    for result in results:
        href = result.get_attribute("href")
        if href and href.startswith("http") and href not in urls:
            urls.append(href)
        if len(urls) == 10:
            break

    assert len(urls) == 10
    for url in urls:
        assert url.startswith("http")
