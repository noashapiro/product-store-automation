import pytest
from playwright.sync_api import expect
from ui.helpers import helpers as test_helpers

@pytest.mark.catalog
class TestProductCatalog:

    def test_products_have_name_price_and_image(self, setup_ui):
        home_page = test_helpers.home_page_displayed(setup_ui)
        product_count = home_page.get_product_count()
        products_to_check = min(5, product_count)  # Check first 5 products
        for i in range(products_to_check):
            product = home_page.get_product_details(i)
            assert product["name"] is not None, f"Product {i} name is empty"
            assert product["price"] is not None, f"Product {i} price is empty"
            expect(product["image"]).to_be_visible()
            # Validate product link is clickable
            expect(product["link"]).to_be_enabled()

    def test_load_all_product_images_successfully(self, setup_ui):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
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

    def test_product_count_is_reasonable(self, setup_ui):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)
        product_count = home_page.get_product_count()

        # Should have at least 1 product and not more than 100 (reasonable upper limit)
        assert product_count >= 1, "No products found on the page"
        assert product_count <= 100, f"Too many products found: {product_count}"

    def test_all_product_names_are_unique(self, setup_ui):
        home_page = test_helpers.home_page_displayed(setup_ui)
        home_page.wait_for_element(home_page.product_cards)

        product_names = home_page.get_all_product_names()
        unique_names = set(product_names)
        assert len(unique_names) == len(product_names), "Duplicate product names found"


