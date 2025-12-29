import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def chrome_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    return options

@pytest.fixture(scope="function")
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def open_google(driver):
    driver.get('https://www.google.com')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    return driver

def test_google_homepage_title(open_google):
    driver = open_google
    assert "Google" in driver.title

def test_search_box_visible(open_google):
    driver = open_google
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'q'))
    )
    assert search_box.is_displayed()

def test_google_search_results(driver):
    driver.get('https://www.google.com')
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'q'))
    )
    search_box.clear()
    search_box.send_keys('selenium')
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'search'))
    )
    results = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
    urls = []
    seen = set()
    for elem in results:
        href = elem.get_attribute('href')
        if href and href.startswith('http') and href not in seen:
            urls.append(href)
            seen.add(href)
        if len(urls) == 10:
            break
    assert len(urls) >= 10, f'Expected at least 10 search results, found {len(urls)}.'

def test_first_result_url_is_valid(driver):
    driver.get('https://www.google.com')
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, 'q'))
    )
    search_box.clear()
    search_box.send_keys('selenium')
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'search'))
    )
    results = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
    urls = []
    seen = set()
    for elem in results:
        href = elem.get_attribute('href')
        if href and href.startswith('http') and href not in seen:
            urls.append(href)
            seen.add(href)
        if len(urls) == 10:
            break
    assert urls[0].startswith('http')
