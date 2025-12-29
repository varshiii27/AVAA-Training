import pytest
import allure
from pages.google_search_page import GoogleSearchPage

@allure.feature("Google Search")
@allure.story("Search for 'selenium' and verify results")
def test_google_search_results(browser):
    page = GoogleSearchPage(browser)
    with allure.step("Open Google and perform search"):
        page.open()
        page.search("selenium")

    with allure.step("Collect and assert search results"):
        urls = page.get_results(min_results=10)
        allure.attach("\n".join(urls), name="Search Result URLs", attachment_type=allure.attachment_type.TEXT)
        assert len(urls) >= 10, f"Expected at least 10 results, got {len(urls)}"
