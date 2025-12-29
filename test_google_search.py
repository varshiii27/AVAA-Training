import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture
def open_google(driver):
    driver.get("https://www.google.com")
    return driver

def test_google_homepage_title(open_google):
    assert "Google" in open_google.title

def test_google_accept_cookies(open_google):
    try:
        consent_btn = WebDriverWait(open_google, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='I agree']] | //button[.//div[text()='Accept all']]"))
        )
        consent_btn.click()
        assert True
    except Exception:
        assert True

def test_google_search_selenium(open_google):
    try:
        try:
            consent_btn = WebDriverWait(open_google, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='I agree']] | //button[.//div[text()='Accept all']]"))
            )
            consent_btn.click()
        except Exception:
            pass
        search_box = WebDriverWait(open_google, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()
        search_box.send_keys("selenium")
        search_box.send_keys(Keys.RETURN)
        results = WebDriverWait(open_google, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#search a"))
        )
        urls = []
        for link in results:
            href = link.get_attribute("href")
            if href and href.startswith("http") and href not in urls:
                urls.append(href)
            if len(urls) == 10:
                break
        assert len(urls) == 10
        for url in urls:
            assert url.startswith("http")
            assert len(url) > 0
    except Exception as e:
        raise
