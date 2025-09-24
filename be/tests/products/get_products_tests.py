import pytest
import requests as request
from http import HTTPStatus
from be.tests.models import Product

class TestGetProduct:
    def test_get_products(self, products_base_url):
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert data[0]["id"] == "1"
        assert data[0]["name"] == "Laptop"

    def test_get_products_returns_list(self, products_base_url):
        """Test that products endpoint returns a list"""
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert isinstance(data, list), f"Expected list, got {type(data)}"

    def test_get_products_has_valid_structure(self, products_base_url):
        """Test that products have expected structure"""
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        assert len(data) > 0, "Products list should not be empty"

        for product in data:
            # Check required fields exist
            assert "id" in product, f"Product missing 'id' field: {product}"
            assert "name" in product, f"Product missing 'name' field: {product}"
            assert "price" in product, f"Product missing 'price' field: {product}"

    def test_get_products_data_types(self, products_base_url):
        """Test that product fields have correct data types"""
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        for product in data:
            # Check data types
            assert isinstance(product["id"], str), f"Expected string id, got {type(product['id'])}"
            assert isinstance(product["name"], str), f"Expected string name, got {type(product['name'])}"
            assert isinstance(product["price"], int), f"Expected int price, got {type(product['price'])}"


    def test_get_products_prices_are_positive(self, products_base_url):
        """Test that all product prices are positive"""
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        for product in data:
            assert product["price"] > 0, f"Price {product['price']} should be positive for product {product['name']}"

    def test_get_products_names_are_not_empty(self, products_base_url):
        """Test that all product names are not empty"""
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        for product in data:
            assert product["name"].strip() != "", f"Product name should not be empty for product ID {product['id']}"
            assert len(product["name"]) > 0, f"Product name should have content for product ID {product['id']}"

    def test_get_products_ids_are_unique(self, products_base_url):
        """Test that all product IDs are unique"""
        resp = request.get(products_base_url)

        assert resp.status_code == HTTPStatus.OK
        data = resp.json()

        product_ids = [product["id"] for product in data]
        unique_ids = set(product_ids)
        
        assert len(product_ids) == len(unique_ids), f"Duplicate product IDs found: {product_ids}"

