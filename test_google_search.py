import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def chrome_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def google_home(driver):
    driver.get("https://www.google.com")
    WebDriverWait(driver, 10).until(EC.title_contains("Google"))
    return driver

def test_google_homepage_title(google_home):
    assert "Google" in google_home.title

def test_google_search_box_visible_and_enabled(google_home):
    search_box = WebDriverWait(google_home, 10).until(
        EC.visibility_of_element_located((By.NAME, "q"))
    )
    assert search_box.is_displayed()
    assert search_box.is_enabled()

def test_google_search_results(google_home):
    search_box = WebDriverWait(google_home, 10).until(
        EC.visibility_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(google_home, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yuRUbf > a"))
    )
    results = google_home.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
    assert len(results) > 0
    assert len(results) >= 10
    for idx, result in enumerate(results[:10], 1):
        url = result.get_attribute("href")
        assert url.startswith("http")
