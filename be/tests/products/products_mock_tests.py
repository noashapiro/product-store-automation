import pytest
import requests as request
from http import HTTPStatus


class TestProductsMock:
    def test_get_products(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert data[0]["id"] == "1"
        assert data[0]["name"] == "Laptop"

    def test_add_to_cart(self, cart_base_url):
        resp = request.post(cart_base_url, json={"product_id": 2, "quantity": 1})

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["product_id"] == 2
        assert data["quantity"] == 1

    def test_get_cart(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert isinstance(data, list)
        assert len(data) > 0
