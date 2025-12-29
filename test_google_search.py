@pytest.fixture(scope="session")
def chrome_options():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    return options

@pytest.fixture
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def open_google(driver):
    driver.get("https://www.google.com")
    return driver

def accept_cookies_if_present(driver):
    try:
        consent_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'I agree') or contains(., 'Accept all')]"))
        )
        consent_button.click()
    except Exception:
        pass

def test_google_homepage_title(open_google):
    driver = open_google
    accept_cookies_if_present(driver)
    assert "Google" in driver.title

def test_google_search_box_visible(open_google):
    driver = open_google
    accept_cookies_if_present(driver)
    search_box = driver.find_element(By.NAME, "q")
    assert search_box.is_displayed()

def test_google_search_results(driver):
    driver.get("https://www.google.com")
    accept_cookies_if_present(driver)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("selenium")
    search_box.submit()
    WebDriverWait(driver, 10).until(EC.title_contains("selenium"))
    assert "selenium" in driver.title.lower()
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yuRUbf > a"))
    )
    assert len(results) >= 10
    for i, result in enumerate(results[:10], start=1):
        url = result.get_attribute("href")
        assert url.startswith("http")