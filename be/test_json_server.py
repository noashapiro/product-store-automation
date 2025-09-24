import requests

BASE_URL = "http://localhost:3000"

def test_get_products():
    resp = requests.get(f"{BASE_URL}/products")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Laptop"

def test_add_to_cart():
    resp = requests.post(f"{BASE_URL}/cart", json={"product_id": 2, "quantity": 1})
    assert resp.status_code == 201
    data = resp.json()
    assert data["product_id"] == 2
    assert data["quantity"] == 1

def test_get_cart():
    resp = requests.get(f"{BASE_URL}/cart")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
