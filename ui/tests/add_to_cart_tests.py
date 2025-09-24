import pytest
from ui.helpers import  helpers as test_helpers

@pytest.mark.cart
class TestAddToCart:
    def test_add_product_to_cart_with_confirmation_popup(self, setup_ui, product_details_page):
        home_page = setup_ui
        home_page.wait_for_element(home_page.product_cards)
        # Navigate to first product details page
        home_page.click_product(0)
        product_details_page.wait_for_element(product_details_page.product_name)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"
        # Set up alert handler before clicking add to cart (the assert of dialog appear is in the setup function)
        test_helpers.setup_alert_handler(product_details_page.page, "Product added")

    def test_add_to_cart_button_text_and_state(self, setup_ui, product_details_page):
        home_page = setup_ui
        home_page.wait_for_element(home_page.product_cards)
        home_page.click_product(0)
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"
        button_text = product_details_page.get_add_to_cart_button_text()
        assert "Add to cart" in button_text, f"Unexpected button text: {button_text}"
        assert product_details_page.is_add_to_cart_button_enabled(), "Add to cart button is not enabled"



