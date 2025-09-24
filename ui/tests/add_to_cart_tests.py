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

    def test_add_product_to_cart_and_verify_in_cart(self, setup_ui, product_details_page, cart_page):
        """Test adding product to cart and verifying it appears in cart"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Navigate to first product details page
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Get product details
        product_name = product_details_page.get_product_name()
        product_price = product_details_page.get_product_price()

        # Set up alert handler
        def handle_dialog(dialog):
            dialog.accept()

        product_details_page.page.on("dialog", handle_dialog)

        # Add product to cart
        product_details_page.click_add_to_cart()
        product_details_page.page.wait_for_timeout(1000)

        # Navigate to cart page
        product_details_page.click_cart()
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

        # Verify product appears in cart
        cart_page.validate_cart_item(product_name, product_price)

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

    def test_maintain_cart_state_across_navigation(self, setup_ui, product_details_page, cart_page):
        """Test that cart state is maintained across page navigation"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Add first product to cart
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        product_name = product_details_page.get_product_name()
        product_price = product_details_page.get_product_price()

        # Set up alert handler
        def handle_dialog(dialog):
            dialog.accept()

        product_details_page.page.on("dialog", handle_dialog)

        product_details_page.click_add_to_cart()
        product_details_page.page.wait_for_timeout(1000)

        # Go back to home page
        product_details_page.click_back()
        assert home_page.is_page_loaded(), "Did not return to home page"

        # Navigate to cart to verify product is there
        home_page.click_cart()
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

        # Verify product is in cart
        cart_page.validate_cart_item(product_name, product_price)

        # Go back to home page
        cart_page.page.go_back()
        assert home_page.is_page_loaded(), "Did not return to home page"

        # Add another product
        home_page.click_product(1)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        second_product_name = product_details_page.get_product_name()
        second_product_price = product_details_page.get_product_price()

        product_details_page.page.on("dialog", handle_dialog)

        product_details_page.click_add_to_cart()
        product_details_page.page.wait_for_timeout(1000)

        # Go to cart and verify both products are there
        product_details_page.click_cart()
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

        cart_item_count = cart_page.get_cart_item_count()
        assert cart_item_count == 2, f"Expected 2 items, got {cart_item_count}"

        cart_page.validate_cart_item(product_name, product_price)
        cart_page.validate_cart_item(second_product_name, second_product_price)

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

    def test_cart_total_updates_correctly(self, setup_ui, product_details_page, cart_page):
        """Test that cart total updates correctly when adding products"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Add first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        first_product_price = product_details_page.get_product_price()

        def handle_dialog(dialog):
            dialog.accept()

        product_details_page.page.on("dialog", handle_dialog)

        product_details_page.click_add_to_cart()
        product_details_page.page.wait_for_timeout(1000)

        # Go to cart and check total
        product_details_page.click_cart()
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

        first_total = cart_page.get_cart_total()
        assert first_total, "Cart total is empty"

        # Go back and add another product
        cart_page.page.go_back()
        assert home_page.is_page_loaded(), "Did not return to home page"

        home_page.click_product(1)
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        second_product_price = product_details_page.get_product_price()

        product_details_page.page.on("dialog", handle_dialog)

        product_details_page.click_add_to_cart()
        product_details_page.page.wait_for_timeout(1000)

        # Go to cart and verify total has updated
        product_details_page.click_cart()
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

        second_total = cart_page.get_cart_total()
        assert second_total, "Cart total is empty"
        assert second_total != first_total, "Cart total did not update"

    @pytest.mark.slow
    def test_add_to_cart_performance(self, setup_ui, product_details_page):
        """Test add to cart performance"""

        home_page = setup_ui

        # Wait for products to load
        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        # Navigate to product details page
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name)

        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Set up alert handler
        def handle_dialog(dialog):
            dialog.accept()

        product_details_page.page.on("dialog", handle_dialog)

        # Measure add to cart time
        start_time = time.time()
        product_details_page.click_add_to_cart()
        product_details_page.page.wait_for_timeout(1000)
        end_time = time.time()

        add_to_cart_time = end_time - start_time

        # Add to cart should complete within 5 seconds
        assert add_to_cart_time < 5, f"Add to cart took too long: {add_to_cart_time:.2f} seconds"
