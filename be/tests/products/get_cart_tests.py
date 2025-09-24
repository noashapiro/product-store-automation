import pytest
import requests as request
from http import HTTPStatus

class TestGetCart:
    def test_get_cart(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert isinstance(data, list)
        assert len(data) > 0