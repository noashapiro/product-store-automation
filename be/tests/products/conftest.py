import pytest
from be.infrastructure.endpoints.endpoints import get_url


@pytest.fixture(scope='module')
def products_base_url():
    return get_url("/products")


@pytest.fixture(scope='module')
def cart_base_url():
    return get_url("/cart")

