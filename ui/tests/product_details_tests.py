import pytest
from playwright.sync_api import expect


@pytest.mark.details
@pytest.mark.smoke
class TestProductDetails:
    """Test class for product details navigation functionality"""

    def test_navigate_to_product_details_page(self, setup_ui, product_details_page):
        """Test navigation to product details page when clicking a product"""
        home_page = setup_ui

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Get first product details from home page
        home_product = home_page.get_product_details(0)
        expected_name = home_product["name"]
        expected_price = home_product["price"]

        # Click on the product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify we're on the product details page
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate product details match what we clicked
        actual_name = product_details_page.get_product_name()
        actual_price = product_details_page.get_product_price()

        assert actual_name == expected_name, f"Product name mismatch: expected {expected_name}, got {actual_name}"

        # Normalize prices for comparison (details page includes tax info)
        expected_price_normalized = expected_price.split()[0]  # Get just the price part
        actual_price_normalized = actual_price.split()[0]  # Get just the price part
        assert actual_price_normalized == expected_price_normalized, f"Product price mismatch: expected {expected_price_normalized}, got {actual_price_normalized}"

    def test_display_correct_product_details(self, setup_demoblaze, product_details_page):
        """Test that product details page displays correct information"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate all product details are present and correct
        product_details_page.validate_product_details()

    def test_working_back_button(self, setup_demoblaze, product_details_page):
        """Test that back button works correctly"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify we're on product details page
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Click back button
        product_details_page.click_back()

        # Verify we're back on home page
        assert home_page.is_page_loaded(), "Did not return to home page"

    def test_navigate_to_different_products(self, setup_demoblaze, product_details_page):
        """Test navigation to different products correctly"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        product_count = home_page.get_product_count()
        products_to_test = min(3, product_count)  # Test first 3 products

        for i in range(products_to_test):
            # Get product details from home page
            home_product = home_page.get_product_details(i)
            expected_name = home_product["name"]
            expected_price = home_product["price"]

            # Click on the product
            home_page.click_product(i)

            # Wait for product details page to load
            # Wait for product details page to load using proper wait strategy
            product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

            # Verify we're on the correct product details page
            assert product_details_page.is_page_loaded(), f"Product details page did not load for product {i}"

            # Validate product details match
            actual_name = product_details_page.get_product_name()
            actual_price = product_details_page.get_product_price()

            assert actual_name == expected_name, f"Product {i} name mismatch: expected {expected_name}, got {actual_name}"

            # Normalize prices for comparison
            expected_price_normalized = expected_price.split()[0]
            actual_price_normalized = actual_price.split()[0]
            assert actual_price_normalized == expected_price_normalized, f"Product {i} price mismatch: expected {expected_price_normalized}, got {actual_price_normalized}"

            # Go back to home page for next iteration
            product_details_page.click_back()
            # Wait for navigation to complete using proper wait strategy
            home_page.wait_for_element(home_page.product_cards, timeout=10000)
            assert home_page.is_page_loaded(), f"Did not return to home page after product {i}"

    def test_display_product_image_on_details_page(self, setup_demoblaze, product_details_page):
        """Test that product image is displayed on details page"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate product image is visible and has proper dimensions
        product_image = product_details_page.get_product_image()
        expect(product_image).to_be_visible()

        image_box = product_image.bounding_box()
        assert image_box is not None, "Product image has no bounding box"
        assert image_box["width"] > 0, "Product image has zero width"
        assert image_box["height"] > 0, "Product image has zero height"

    def test_add_to_cart_button_on_details_page(self, setup_demoblaze, product_details_page):
        """Test that add to cart button is present and functional on details page"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Validate add to cart button is present and enabled
        add_to_cart_button = product_details_page.page.locator(".btn-success")
        expect(add_to_cart_button).to_be_visible()
        expect(add_to_cart_button).to_be_enabled()

        # Verify button text
        button_text = product_details_page.get_add_to_cart_button_text()
        assert "Add to cart" in button_text, f"Unexpected button text: {button_text}"

    def test_product_description_is_present(self, setup_demoblaze, product_details_page):
        """Test that product description is present on details page"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Get product description
        description = product_details_page.get_product_description()

        # Validate description exists and is not empty
        assert description, "Product description is empty"
        assert len(description) > 0, "Product description is empty"
        assert len(description.strip()) > 0, "Product description contains only whitespace"

    def test_product_price_format_on_details_page(self, setup_demoblaze, product_details_page):
        """Test that product price is in correct format on details page"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Get product price
        price = product_details_page.get_product_price()

        # Validate price format
        assert price, "Product price is empty"
        assert "$" in price, f"Product price doesn't contain $: {price}"

        # Check if price is numeric (remove $ and try to convert, handle tax text)
        price_value = price.split()[0].replace("$", "").replace(",", "")
        try:
            float(price_value)
        except ValueError:
            pytest.fail(f"Product price is not numeric: {price}")

    def test_cart_link_navigation_from_details_page(self, setup_demoblaze, product_details_page, cart_page):
        """Test navigation to cart from product details page"""
        home_page = setup_demoblaze

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Click on first product
        home_page.click_product(0)

        # Wait for product details page to load using proper wait strategy
        product_details_page.wait_for_element(product_details_page.product_name, timeout=10000)

        # Verify page is loaded
        assert product_details_page.is_page_loaded(), "Product details page did not load properly"

        # Click cart link
        product_details_page.click_cart()

        # Verify we're on cart page
        assert cart_page.is_page_loaded(), "Cart page did not load properly"

    @pytest.mark.slow
    def test_multiple_product_navigation_performance(self, setup_demoblaze, product_details_page):
        """Test performance when navigating between multiple products"""

        home_page = setup_demoblaze
        product_count = home_page.get_product_count()
        products_to_test = min(5, product_count)  # Test first 5 products

        start_time = time.time()

        for i in range(products_to_test):
            # Navigate to product
            home_page.click_product(i)
            assert product_details_page.is_page_loaded(), f"Product details page did not load for product {i}"

            # Go back
            product_details_page.click_back()
            assert home_page.is_page_loaded(), f"Did not return to home page after product {i}"

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete within reasonable time (30 seconds for 5 products)
        assert total_time < 30, f"Navigation took too long: {total_time:.2f} seconds"
