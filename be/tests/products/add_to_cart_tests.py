import pytest
import requests as request
from http import HTTPStatus
from be.tests.models import CartItem


class TestAddCart:
    def test_add_to_cart(self, cart_base_url):
        # Create cart item data using data class
        cart_item = CartItem(product_id=2, quantity=1)
        
        resp = request.post(cart_base_url, json=cart_item.to_dict())

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["product_id"] == cart_item.product_id
        assert data["quantity"] == cart_item.quantity

    def test_add_different_product_to_cart(self, cart_base_url):
        # Easy to change product_id and quantity
        cart_item = CartItem(product_id=1, quantity=3)
        
        resp = request.post(cart_base_url, json=cart_item.to_dict())

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["product_id"] == cart_item.product_id
        assert data["quantity"] == cart_item.quantity

    def test_add_multiple_quantity_to_cart(self, cart_base_url):
        # Easy to test different quantities
        cart_item = CartItem(product_id=2, quantity=5)
        
        resp = request.post(cart_base_url, json=cart_item.to_dict())

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["product_id"] == cart_item.product_id
        assert data["quantity"] == cart_item.quantity