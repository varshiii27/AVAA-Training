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
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.mark.usefixtures("driver")
def test_google_homepage_title(driver):
    driver.get("https://www.google.com")
    WebDriverWait(driver, 10).until(EC.title_contains("Google"))
    assert "Google" in driver.title

@pytest.mark.usefixtures("driver")
def test_google_search_box_presence(driver):
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    assert search_box.is_displayed()

@pytest.mark.usefixtures("driver")
def test_google_search_results(driver):
    driver.get("https://www.google.com")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.clear()
    search_box.send_keys("selenium")
    search_box.submit()
    results_locator = (By.CSS_SELECTOR, "div#search .g")
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(results_locator)
    )
    results = driver.find_elements(*results_locator)
    assert len(results) >= 10
    urls = []
    count = 0
    for result in results:
        try:
            link = result.find_element(By.TAG_NAME, "a")
            url = link.get_attribute("href")
            if url:
                urls.append(url)
                count += 1
            if count == 10:
                break
        except Exception:
            continue
    assert len(urls) == 10
    for url in urls:
        assert url.startswith("http")
