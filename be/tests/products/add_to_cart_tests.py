import pytest
import requests as request
from http import HTTPStatus

class TestAddCart:
    def test_add_to_cart(self, cart_base_url):
        resp = request.post(cart_base_url, json={"product_id": 2, "quantity": 1})

        assert resp.status_code == HTTPStatus.CREATED
        data = resp.json()

        assert data["product_id"] == 2
        assert data["quantity"] == 1