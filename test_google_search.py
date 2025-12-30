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
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()

@pytest.mark.usefixtures("driver")
def test_google_homepage_title(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title

@pytest.mark.usefixtures("driver")
def test_google_search_box_present(driver):
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    assert search_box is not None

@pytest.mark.usefixtures("driver")
def test_google_search_results(driver):
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    search_box.submit()
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yuRUbf > a"))
    )
    results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
    assert len(results) > 0
    for idx, result in enumerate(results[:10], 1):
        url = result.get_attribute("href")
        assert url is not None and url.startswith("http")
    assert len(results) >= 10
