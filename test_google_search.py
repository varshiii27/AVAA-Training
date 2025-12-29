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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.mark.usefixtures("driver")
def test_google_homepage_title(driver):
    driver.get('https://www.google.com')
    WebDriverWait(driver, 10).until(EC.title_contains('Google'))
    assert 'Google' in driver.title

@pytest.mark.usefixtures("driver")
def test_google_search_box_present(driver):
    driver.get('https://www.google.com')
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    assert search_box.is_displayed()

@pytest.mark.usefixtures("driver")
def test_google_search_results(driver):
    driver.get('https://www.google.com')
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_box.clear()
    search_box.send_keys('selenium')
    search_box.send_keys(Keys.RETURN)
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#search a'))
    )
    urls = []
    seen = set()
    for result in results:
        href = result.get_attribute('href')
        if href and href.startswith('http') and href not in seen:
            urls.append(href)
            seen.add(href)
        if len(urls) == 10:
            break
    assert len(urls) == 10
    for url in urls:
        assert url.startswith('http')
