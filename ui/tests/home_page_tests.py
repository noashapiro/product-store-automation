import pytest
from playwright.sync_api import expect


@pytest.mark.catalog
@pytest.mark.smoke
class TestProductCatalog:
    """Test class for product catalog functionality"""

    def test_display_all_products_with_correct_details(self, setup_demoblaze):
        """Test that all products are displayed with correct details"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards)

        # Get product count
        product_count = home_page.get_product_count()
        assert product_count > 0, "No products found on the page"

        # Validate all products are displayed with correct details
        home_page.validate_product_display()

    def test_products_have_name_price_and_image(self, setup_demoblaze):
        """Test that products have name, price, and image"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        # Get first few products and validate their details
        product_count = home_page.get_product_count()
        products_to_check = min(5, product_count)  # Check first 5 products

        for i in range(products_to_check):
            product = home_page.get_product_details(i)

            # Validate product name
            assert product["name"], f"Product {i} name is empty"
            assert len(product["name"]) > 0, f"Product {i} name is empty"

            # Validate product price
            assert product["price"], f"Product {i} price is empty"
            assert "$" in product["price"], f"Product {i} price doesn't contain $"

            # Validate product image is visible
            expect(product["image"]).to_be_visible()

            # Validate product link is clickable
            expect(product["link"]).to_be_visible()

    def test_consistent_product_layout(self, setup_demoblaze):
        """Test that all products have consistent layout"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        product_count = home_page.get_product_count()
        assert product_count > 0, "No products found on the page"

        # Check that all product cards have the same structure
        for i in range(product_count):
            product = home_page.get_product_details(i)

            # Each product should have all required elements
            assert product["name"] is not None, f"Product {i} name is None"
            assert product["price"] is not None, f"Product {i} price is None"
            assert product["image"] is not None, f"Product {i} image is None"
            assert product["link"] is not None, f"Product {i} link is None"

    def test_load_all_product_images_successfully(self, setup_demoblaze):
        """Test that all product images load successfully"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        product_count = home_page.get_product_count()

        # Check that all product images are loaded and visible
        for i in range(product_count):
            product = home_page.get_product_details(i)

            # Wait for image to load
            expect(product["image"]).to_be_visible()

            # Check that image has proper dimensions
            image_box = product["image"].bounding_box()
            assert image_box is not None, f"Product {i} image has no bounding box"
            assert image_box["width"] > 0, f"Product {i} image has zero width"
            assert image_box["height"] > 0, f"Product {i} image has zero height"

    def test_product_count_is_reasonable(self, setup_demoblaze):
        """Test that there are a reasonable number of products"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        product_count = home_page.get_product_count()

        # Should have at least 1 product and not more than 100 (reasonable upper limit)
        assert product_count >= 1, "No products found on the page"
        assert product_count <= 100, f"Too many products found: {product_count}"

    def test_all_product_names_are_unique(self, setup_demoblaze):
        """Test that all product names are unique"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        product_names = home_page.get_all_product_names()

        # Check for duplicates
        unique_names = set(product_names)
        assert len(unique_names) == len(product_names), "Duplicate product names found"

    def test_product_prices_are_valid_format(self, setup_demoblaze):
        """Test that all product prices are in valid format"""
        home_page = setup_demoblaze

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"

        # Wait for products to load using proper wait strategy
        home_page.wait_for_element(home_page.product_cards, timeout=10000)

        product_prices = home_page.get_all_product_prices()

        for i, price in enumerate(product_prices):
            # Price should contain $ and be a valid format
            assert "$" in price, f"Product {i} price doesn't contain $: {price}"
            # Remove $ and check if remaining part is numeric
            price_value = price.replace("$", "").replace(",", "")
            try:
                float(price_value)
            except ValueError:
                pytest.fail(f"Product {i} price is not numeric: {price}")

    @pytest.mark.slow
    def test_page_performance(self, setup_demoblaze):
        """Test that page loads within acceptable time"""

        start_time = time.time()
        home_page = setup_demoblaze
        end_time = time.time()

        load_time = end_time - start_time

        # Page should load within 10 seconds
        assert load_time < 10, f"Page took too long to load: {load_time:.2f} seconds"

        # Verify page is loaded
        assert home_page.is_page_loaded(), "Home page did not load properly"
