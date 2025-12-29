import allure
from pages.google_search_page import GoogleSearchPage

@allure.feature("Google Search")
@allure.story("Search for 'selenium' and validate results")
def test_google_search(browser):
    page = GoogleSearchPage()

    with allure.step("Open Google and accept cookies"):
        page.open(browser)
        page.accept_cookies(browser)

    with allure.step("Search for 'selenium'"):
        page.search(browser, "selenium")

    with allure.step("Extract first 10 result URLs"):
        urls = page.get_result_urls(browser, count=10)

    with allure.step("Assert at least 10 results and print them"):
        assert len(urls) >= 10, f"Expected at least 10 results, got {len(urls)}"
        for i, url in enumerate(urls, 1):
            allure.attach(url, name=f"Result {i}", attachment_type=allure.attachment_type.TEXT)
