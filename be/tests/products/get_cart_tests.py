import requests as request
from http import HTTPStatus
import pytest
from be.tests import helpers as helper

@pytest.mark.cart
class TestGetCart:
    def test_get_cart(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        cart = helper.get_cart_from_response_list(resp)

        assert len(cart) > 0


    def test_get_cart_has_valid_structure(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK

        cart = helper.get_cart_from_response_list(resp)

        for cart_item_data in cart:
            assert cart_item_data.id is not None, "Cart item missing 'id' field"
            assert cart_item_data.product_id is not None, "Cart item missing 'product_id' field"
            assert cart_item_data.quantity is not None, "Cart item missing 'quantity' field"

