import pytest
from playwright.sync_api import expect


@pytest.mark.cart
@pytest.mark.smoke
class TestAddToCart:
    """Test class for add to cart functionality"""

    def test_add_product_to_cart_with_confirmation_popup(self, setup_ui, product_details_page):
        """Test adding product to cart and showing confirmation popup"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Navigate to first product details page
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Get product details before adding to cart
        product_name = product_details_page.get_product_name()
        product_price = product_details_page.get_product_price()

        # Set up alert handler before clicking add to cart
        alert_message = ""

        def handle_dialog(dialog):
            nonlocal alert_message
            alert_message = dialog.message
            dialog.accept()

        product_details_page.page.on("dialog", handle_dialog)

        # Click add to cart button
        product_details_page.click_add_to_cart()

        # Wait a moment for the alert to appear
        product_details_page.page.wait_for_timeout(1000)

        # Verify confirmation popup appeared with correct message
        assert "Product added" in alert_message, f"Unexpected alert message: {alert_message}"

    def test_add_multiple_products_to_cart(self, setup_ui, product_details_page, cart_page):
        """Test adding multiple products to cart"""
        home_page = setup_ui
        product_count = home_page.get_product_count()
        products_to_add = min(3, product_count)
        added_products = []

        for i in range(products_to_add):
            # Navigate to product details page
            home_page.click_product(i)
            assert product_details_page.is_page_loaded(), f"Product details page did not load for product {i}"

            # Get product details
            product_name = product_details_page.get_product_name()
            product_price = product_details_page.get_product_price()
            added_products.append({"name": product_name, "price": product_price})

            # Set up alert handler
            def handle_dialog(dialog):
                dialog.accept()

            product_details_page.page.on("dialog", handle_dialog)

            # Add product to cart
            product_details_page.click_add_to_cart()
            product_details_page.page.wait_for_timeout(1000)

            # Go back to home page for next product
            product_details_page.click_back()
            assert home_page.is_page_loaded(), f"Did not return to home page after product {i}"

        # Navigate to cart page
        home_page.click_cart()
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

        # Verify all products are in cart
        cart_item_count = cart_page.get_cart_item_count()
        assert cart_item_count == products_to_add, f"Expected {products_to_add} items, got {cart_item_count}"

        # Verify each product details
        for product in added_products:
            cart_page.validate_cart_item(product["name"], product["price"])

    def test_handle_add_to_cart_button_click_without_errors(self, setup_ui, product_details_page):
        """Test that add to cart button click doesn't cause errors"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Navigate to product details page
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Verify add to cart button is clickable
        add_to_cart_button = product_details_page.page.locator(".btn-success")
        expect(add_to_cart_button).to_be_visible()
        expect(add_to_cart_button).to_be_enabled()

        # Set up alert handler
        def handle_dialog(dialog):
            assert dialog.type == "alert", f"Unexpected dialog type: {dialog.type}"
            dialog.accept()

        product_details_page.page.on("dialog", handle_dialog)

        # Click add to cart button
        add_to_cart_button.click()

        # Wait for alert to be handled
        product_details_page.page.wait_for_timeout(1000)

        # Verify no errors occurred (page should still be functional)
        expect(add_to_cart_button).to_be_visible()

    def test_show_confirmation_popup_for_each_product(self, setup_ui, product_details_page):
        """Test that confirmation popup appears for each product added"""
        home_page = setup_ui
        product_count = home_page.get_product_count()
        products_to_test = min(2, product_count)
        alert_count = 0

        for i in range(products_to_test):
            # Navigate to product details page
            home_page.click_product(i)
            assert product_details_page.is_page_loaded(), f"Product details page did not load for product {i}"

            # Set up alert handler
            def handle_dialog(dialog):
                nonlocal alert_count
                alert_count += 1
                assert "Product added" in dialog.message, f"Unexpected alert message: {dialog.message}"
                dialog.accept()

            product_details_page.page.on("dialog", handle_dialog)

            # Add product to cart
            product_details_page.click_add_to_cart()
            product_details_page.page.wait_for_timeout(1000)

            # Go back to home page for next product
            product_details_page.click_back()
            assert home_page.is_page_loaded(), f"Did not return to home page after product {i}"

        # Verify we got confirmation popup for each product
        assert alert_count == products_to_test, f"Expected {products_to_test} alerts, got {alert_count}"

    def test_add_to_cart_button_text_and_state(self, setup_ui, product_details_page):
        """Test add to cart button text and state"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Navigate to product details page
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Verify button text
        button_text = product_details_page.get_add_to_cart_button_text()
        assert "Add to cart" in button_text, f"Unexpected button text: {button_text}"

        # Verify button is enabled
        assert product_details_page.is_add_to_cart_button_enabled(), "Add to cart button is not enabled"
