import pytest
import requests as request
from http import HTTPStatus

class TestGetProduct:
    def test_get_products(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert data[0]["id"] == "1"
        assert data[0]["name"] == "Laptop"