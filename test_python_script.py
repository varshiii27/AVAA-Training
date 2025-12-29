import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)

def test_google_search_box_present(driver, wait):
    driver.get('https://www.google.com')
    search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
    assert search_box is not None
    assert search_box.is_displayed()
    assert driver.title.lower().startswith("google")

def test_google_search_results(driver, wait):
    driver.get('https://www.google.com')
    search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
    search_box.send_keys('selenium')
    search_box.send_keys(Keys.RETURN)
    results_locator = (By.CSS_SELECTOR, 'div#search a')
    wait.until(EC.presence_of_all_elements_located(results_locator))
    result_links = driver.find_elements(*results_locator)
    assert len(result_links) >= 10
    for idx, link in enumerate(result_links[:10], start=1):
        url = link.get_attribute('href')
        assert url is not None
        assert url.startswith('http')
