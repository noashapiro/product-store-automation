import requests as request
from http import HTTPStatus
from be.infrastructure.responsesDTO.responses import ProductResponseDTO


class TestGetProduct:
    def test_get_products(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK

        products = get_products_from_response(resp)
        assert len(products) > 0
        assert products[0].name == "Laptop"


    def test_get_products_has_valid_structure(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK

        products = get_products_from_response(resp)
        assert len(products) > 0, "Products list should not be empty"

        for product in products:
            assert product.id is not None, f"Product missing 'id' field"
            assert product.name is not None, f"Product missing 'name' field"
            assert product.price is not None, f"Product missing 'price' field"

    def test_get_products_data_types(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK

        products = get_products_from_response(resp)

        for product in products:
            assert isinstance(product.id, str), f"Expected string id, got {type(product.id)}"
            assert isinstance(product.name, str), f"Expected string name, got {type(product.name)}"
            assert isinstance(product.price, int), f"Expected int price, got {type(product.price)}"


    def test_get_products_prices_are_positive(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK

        products = get_products_from_response(resp)

        for product in products:
            assert product.price > 0, f"Price {product.price} should be positive for product {product.name}"



def get_products_from_response(resp):
    return [ProductResponseDTO(**p) for p in resp.json()]
