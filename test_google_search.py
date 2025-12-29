import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def chrome_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def open_google(driver):
    driver.get("https://www.google.com")
    return driver

def test_google_homepage_title(open_google):
    driver = open_google
    assert "Google" in driver.title

def test_google_search_functionality(open_google):
    driver = open_google
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    search_box.submit()
    WebDriverWait(driver, 10).until(
        EC.title_contains("selenium")
    )
    assert "selenium" in driver.title.lower()

def test_google_search_results_urls(open_google):
    driver = open_google
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    search_box.submit()
    WebDriverWait(driver, 10).until(
        EC.title_contains("selenium")
    )
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#search a"))
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
