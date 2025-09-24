import pytest
from playwright.sync_api import expect
from ui.helpers import helpers as test_helpers

@pytest.mark.details
@pytest.mark.smoke
class TestProductDetails:

    def test_navigate_to_product_details_page(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)

        home_page.wait_for_element(home_page.product_cards)

        # Get first product details from home page
        home_product = home_page.get_product_details(0)
        expected_name = home_product["name"]
        expected_price = home_product["price"]
        test_helpers.get_product_by_inex(0)
        product_details_page.wait_for_element(product_details_page.product_name)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate product details match what we clicked
        actual_name = product_details_page.get_product_name()
        actual_price = product_details_page.get_product_price()

        assert actual_name == expected_name, f"Product name mismatch: expected {expected_name}, got {actual_name}"

        expected_price_normalized = expected_price.split()[0]  # Get just the price part
        actual_price_normalized = actual_price.split()[0]  # Get just the price part
        assert actual_price_normalized == expected_price_normalized, f"Product price mismatch: expected {expected_price_normalized}, got {actual_price_normalized}"



    def test_display_correct_product_details(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
        test_helpers.get_product_by_inex(0)
        product_details_page.wait_for_element(product_details_page.product_name)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate all product details are present and correct
        product_details_page.validate_product_details()

    def test_display_product_image_on_details_page(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
        test_helpers.get_product_by_inex(0)
        product_details_page.wait_for_element(product_details_page.product_name)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate product image is visible and has proper dimensions
        product_image = product_details_page.get_product_image()
        expect(product_image).to_be_visible()

        image_box = product_image.bounding_box()
        assert image_box is not None, "Product image has no bounding box"
        assert image_box["width"] > 0, "Product image has zero width"
        assert image_box["height"] > 0, "Product image has zero height"

    def test_add_to_cart_button_on_details_page(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
        test_helpers.get_product_by_inex(0)
        product_details_page.wait_for_element(product_details_page.product_name)

        add_to_cart_button = product_details_page.add_to_cart_button
        expect(add_to_cart_button).to_be_visible()
        expect(add_to_cart_button).to_be_enabled()
        button_text = product_details_page.get_add_to_cart_button_text()
        assert "Add to cart" in button_text, f"Unexpected button text: {button_text}"

    def test_product_description_is_present(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
        test_helpers.get_product_by_inex(0)
        product_details_page.wait_for_element(product_details_page.product_name)
        description = product_details_page.get_product_description()

        # Validate description exists and is not empty
        assert description, "Product description is empty"
        assert len(description) > 0, "Product description is empty"
        assert len(description.strip()) > 0, "Product description contains only whitespace"

    def test_product_price_format_on_details_page(self, setup_ui, product_details_page):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
        test_helpers.get_product_by_inex(0)
        product_details_page.wait_for_element(product_details_page.product_name)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"
        price = product_details_page.get_product_price()

        # Validate price format
        assert price, "Product price is empty"
        assert "$" in price, f"Product price doesn't contain $: {price}"
        self.price_assertion(price)


# can be moved to other class, but since its assertion function its can stay on the test class
    def price_assertion(self, price):
        price_value = price.split()[0].replace("$", "").replace(",", "")
        try:
            float(price_value)
        except ValueError:
            pytest.fail(f"Product price is not numeric: {price}")


