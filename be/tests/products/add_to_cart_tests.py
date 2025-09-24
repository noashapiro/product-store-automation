import requests as request
from http import HTTPStatus
from be.infrastructure.responsesDTO.responses import CartResponseDTO
from be.infrastructure.requestsDTO.requests import AddToCartRequestDTO


def get_cart_from_response(resp):
    """Helper function to convert API response to CartResponseDTO object"""
    return CartResponseDTO(**resp.json())


class TestAddCart:

    def test_add_to_cart(self, cart_base_url):
        add_to_cart_request = AddToCartRequestDTO(product_id=2, quantity=1)

        resp = request.post(cart_base_url, json=add_to_cart_request.model_dump())

        assert resp.status_code == HTTPStatus.CREATED
        
        cart_response = get_cart_from_response(resp)
        assert cart_response.product_id == add_to_cart_request.product_id
        assert cart_response.quantity == add_to_cart_request.quantity

    def test_add_different_product_to_cart(self, cart_base_url):
        add_to_cart_request = AddToCartRequestDTO(product_id=1, quantity=3)

        resp = request.post(cart_base_url, json=add_to_cart_request.model_dump())

        assert resp.status_code == HTTPStatus.CREATED
        
        cart_response = get_cart_from_response(resp)
        assert cart_response.product_id == add_to_cart_request.product_id
        assert cart_response.quantity == add_to_cart_request.quantity
