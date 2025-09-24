import pytest
import requests as request
from http import HTTPStatus
from be.tests.models import CartItem

class TestGetCart:
    def test_get_cart(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_cart_returns_list(self, cart_base_url):
        """Test that cart endpoint returns a list"""
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert isinstance(data, list), f"Expected list, got {type(data)}"

    def test_get_cart_has_valid_structure(self, cart_base_url):
        """Test that cart items have expected structure"""
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        if len(data) > 0:
            cart_item = data[0]
            # Check required fields exist
            assert "id" in cart_item, "Cart item missing 'id' field"
            assert "product_id" in cart_item, "Cart item missing 'product_id' field"
            assert "quantity" in cart_item, "Cart item missing 'quantity' field"

    def test_get_cart_item_data_types(self, cart_base_url):
        """Test that cart item fields have correct data types"""
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        if len(data) > 0:
            cart_item = data[0]
            # Check data types
            assert isinstance(cart_item["id"], str), f"Expected string id, got {type(cart_item['id'])}"
            assert isinstance(cart_item["product_id"], int), f"Expected int product_id, got {type(cart_item['product_id'])}"
            assert isinstance(cart_item["quantity"], int), f"Expected int quantity, got {type(cart_item['quantity'])}"

    def test_get_cart_response_time(self, cart_base_url):
        """Test that cart endpoint responds within reasonable time"""
        import time
        
        start_time = time.time()
        resp = request.get(cart_base_url)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert resp.status_code == HTTPStatus.OK
        assert response_time < 5.0, f"Response time {response_time:.2f}s exceeds 5 seconds"

    def test_get_cart_with_different_products(self, cart_base_url):
        """Test that cart can contain different products"""
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        if len(data) > 1:
            # Check that we have different product_ids
            product_ids = [item["product_id"] for item in data]
            unique_product_ids = set(product_ids)
            assert len(unique_product_ids) > 1, "Cart should contain different products"

    def test_get_cart_quantities_are_positive(self, cart_base_url):
        """Test that all cart item quantities are positive"""
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        for item in data:
            assert item["quantity"] > 0, f"Quantity {item['quantity']} should be positive"

    def test_get_cart_product_ids_are_valid(self, cart_base_url):
        """Test that product_ids in cart are valid (positive integers)"""
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        for item in data:
            assert item["product_id"] > 0, f"Product ID {item['product_id']} should be positive"
            assert isinstance(item["product_id"], int), f"Product ID should be integer, got {type(item['product_id'])}"