import pytest
from playwright.sync_api import expect
from ui.helpers import helpers as test_helpers


@pytest.mark.details
class TestProductDetails:

    def test_navigate_to_product_details_page(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)

        home_page.wait_for_element(home_page.product_cards)

        home_product = home_page.get_product_details(0)
        expected_name = home_product["name"]
        expected_price = home_product["price"]

        home_page.click_product(0)
        product_details_page.wait_for_element(product_details_page.product_name)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        actual_name = product_details_page.get_product_name()
        actual_price = product_details_page.get_product_price()

        assert actual_name == expected_name, f"Product name mismatch: expected {expected_name}, got {actual_name}"

        expected_price_normalized = expected_price.split()[0]  # Get just the price part
        actual_price_normalized = actual_price.split()[0]  # Get just the price part
        assert actual_price_normalized == expected_price_normalized, f"Product price mismatch: expected {expected_price_normalized}, got {actual_price_normalized}"

    def test_display_correct_product_details(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)

        home_page.wait_for_element(home_page.product_cards)
        home_page.click_product(0)
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        product_details_page.validate_product_details()

    def test_display_product_image_on_details_page(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)

        home_page.wait_for_element(home_page.product_cards)
        home_page.click_product(0)
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        product_image = product_details_page.get_product_image()
        expect(product_image).to_be_visible()

        image_box = product_image.bounding_box()
        assert image_box is not None, "Product image has no bounding box"
        assert image_box["width"] > 0, "Product image has zero width"
        assert image_box["height"] > 0, "Product image has zero height"

    def test_product_description_is_present(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)

        home_page.wait_for_element(home_page.product_cards)
        home_page.click_product(0)
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        description = product_details_page.get_product_description()

        # Validate description exists and is not empty
        assert description, "Product description is empty"
        assert len(description) > 0, "Product description is empty"
        assert len(description.strip()) > 0, "Product description contains only whitespace"
