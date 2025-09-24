from playwright.sync_api import Page, expect
import sys
sys.path.append('..')
from configuration import BASE_URL, UI_DEFAULT_TIMEOUT as DEFAULT_TIMEOUT

class BasePage:

    def __init__(self, page: Page):
        self.page = page
        self.base_url = BASE_URL

    #navigate to url
    def navigate(self, url: str = ""):
        full_url = f"{self.base_url}{url}" if url else self.base_url
        self.page.goto(full_url)

    def wait_for_element(self, selector: str, timeout: int = DEFAULT_TIMEOUT):
        self.page.wait_for_selector(selector, timeout=timeout)

    def click_element(self, selector: str):
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector)

    def is_visible(self, selector: str) -> bool:
        return self.page.is_visible(selector)

    def is_enabled(self, selector: str) -> bool:
        return self.page.is_enabled(selector)

    def get_attribute(self, selector: str, attribute: str) -> str:
        return self.page.get_attribute(selector, attribute)


