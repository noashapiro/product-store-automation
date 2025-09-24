import pytest
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
# from pages.product_details_page import ProductDetailsPage
# from pages.cart_page import CartPage


@pytest.fixture(scope="session")
def browser_context_args():
    """Browser context arguments for all tests"""
    return {
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def page(browser_context_args):
    """Create a new page for each test"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        context = browser.new_context(**browser_context_args)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def home_page(page):
    """Home page fixture"""
    return HomePage(page)


# @pytest.fixture(scope="function")
# def product_details_page(page):
#     """Product details page fixture"""
#     return ProductDetailsPage(page)
#
#
# @pytest.fixture(scope="function")
# def cart_page(page):
#     """Cart page fixture"""
#     return CartPage(page)


@pytest.fixture(scope="function")
def setup_demoblaze(home_page):
    """Setup fixture to navigate to Demoblaze home page"""
    home_page.navigate()
    return home_page



