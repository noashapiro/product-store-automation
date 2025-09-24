import requests as request
from http import HTTPStatus
from be.infrastructure.responsesDTO.responses import CartResponseDTO


def get_cart_from_response(resp):
    return [CartResponseDTO(**c) for c in resp.json()]

class TestGetCart:
    def test_get_cart(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK
        cart = get_cart_from_response(resp)

        assert len(cart) > 0


    def test_get_cart_has_valid_structure(self, cart_base_url):
        resp = request.get(cart_base_url)

        assert resp.status_code == HTTPStatus.OK

        cart = get_cart_from_response(resp)

        for cart_item_data in cart:
            assert cart_item_data.id is not None, "Cart item missing 'id' field"
            assert cart_item_data.product_id is not None, "Cart item missing 'product_id' field"
            assert cart_item_data.quantity is not None, "Cart item missing 'quantity' field"

